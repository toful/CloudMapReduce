# CloudMapReduce
Playing out with MapReduce in the Cloud.

Implementing a simple prototype of the MapReduce paradigm using Cloud Serverless technologies.

We implemented a count-words and a word-count function in this application using [AWS (Amazon Web Service)](https://aws.amazon.com/es/).


## Pre-requisites
To create the same architecture as us you need to follow the next steps:

1. Create your AWS account
2. Create an s3 bucket
3. Create your lambda function(s): In this example we created the next functions:
   - split: Splits the input file filename in n chunks.
   - map: Applies function in a single chunk of data.
   - reduce: Sums up all results.
   We considered the function role inherent to the lambda function; so we have two types of maps: mapCW (count-words) and map WC (word-count). Having this implementation instead of a unique Map lambda that can execute several functions depending on received parameters is totally optional.
4. Create your own IAM role in order to work with S3 and lambda.
5. Create events in order to execute automatically functions when a step is done (synchronization). You can also use other synchronization methods such as RabbitMQ or Amazon MQ for example. If you want to try this approach, you can ignore all step relative to events and synchronization.
6. Give permissions to your lambda function(s) to use s3 and receive events notification from it (if you use event for synchronization).
7. Give permissions to your lambda function(s) to use CloudWatch and be monitored by it. This is very useful since some of our lambdas are not being executed directly, so we will probably need this service if we want to debug or get the output from a lambda execution triggered by an event.
8. Upload your input file(s) into s3.
9. Install boto3 in your machine:
```
pip install boto3
```
10. Configure aws in your local machine. (optional, just for invoking remote lambdas from the tty of your computer) 
11. Create your master program that imports boto3 and execute your desired lambda function. If you used events, probably you just need to invoke the "primary" lambda function and the events will be in charge of invoking the necessary lambdas for the completion of MapReduce process.

## Working with api boto3
To manage all operation with the services of AWS in python we use the boto3 library. 

There are many methods and operations but mainly we used these:

###### For s3:

Import library boto3
```
import boto3 
```
Create a host to s3. You can obtain your user credentials in aws configuration
```
s3 = boto3.client(s3, aws_access_key_id=KEY_ID, aws_secret_access_key=SECRET_KEY) 
```
Download a file. LOCAL_PATH probably will be /tmp/* since any other folder is non-mutable (read-only filesystem)
```
s3.download_file(NAME_OF_S3_BUCKET, S3_PATH, LOCAL_PATH)
```
Upload a file to s3
```
s3.upload_file(LOCAL_PATH, NAME_OF_S3_BUCKET, S3_PATH/NEW_NAME) 
```
Delete a file from s3
```
s3.delete_object(Bucket=NAME_OF_S3_BUCKET, Key=REMOTE_PATH) 
```
###### For lambda:

Create host to lambda
```
lambda = boto3.client(`lambda_client`)
```
Invoke lambda function remotely
```
lambda.invoke( FunctionName=FUNCTION_NAME, InvocationType=[event], Payload=DATA_TO_FUNCTION)
```

###### For CloudWatch

You can use CloudWatch comfortably from the desktop web aplication.

## Functioning

1. Split function is invoked. Split function receives three arguments contained in the argument "event" which can be treated as a dictionary data structure. These are: 
   - Number of mappers (also number of chunks of data)
   - Function to execute. In our example this can be `[WC|CW]`
   - Name of input file (only the name since split function looks for this file in the `Input_File` folder)
2. File is splitted and every chunk is uploaded into `Split_Files_WC` or `Split_Files_CW` depending on the function selected as a parameter.
3. Creation of objects in these folders triggers the invocation of `MapWC` or `MapCW`, depending of the folder the object is created in.
4. A Map function is invoked for every single object created in this folder. Map function receives the notification event as a parameter, which contains the path and name to the file that triggered the invocation.
5. Every map applies function to "its" chunk. Every chunk is uploaded to `Treated_Chunks` folder. Then, its raw data chunk file counterpart is removed from the `Split_Files_FUNCTION` folder. This release space from s3, allows a clean workspace and triggers an invocation of the last function.
6. Every deletion in the `Split_Files_FUNCTION` triggers the invocation of the reducer.
7. Every instance of the reducer will check first if all files in `Split_Files_FUNCTION` are removed. If the folder is empty means that all maps have ended, so we can start reduce step. If not, reducer returns and does nothing.
Note: Step 6 and 7 could have been implemented using as event the creation of every file in `Treated_Chunks` folder. This approach is OK but you need to tell the reduce function how many files must be in the `Treated_Chunks` folder to begin the reduce step. This needs an extra parameter that our approach does not have since we are checking that a folder is empty instead of checking that there are n files in a folder.
8. Reduce function delete all chunks in `Treated_Chunks` for cleaning up and uploads the result into `Output_Folder/out.txt` which will contain the result of the Map-Reduce operation.

## Information sources

We used this tutorials:

[Working with S3](https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html)

[Example of Map-Reduce using Lambda](https://github.com/awslabs/lambda-refarch-mapreduce)

[Lambda Client in Python](http://blog.cesarcd.com/2017/07/sample-aws-lambda-client-written-in.html)
## Authors

* **Aleix Mariné Tena** - [AleixMT](https://github.com/AleixMT)
* **Cristòfol Daudén Esmel** - [toful](https://github.com/toful