# CloudMapReduce
Playing out with MapReduce in the Cloud

Implementing a simple prototype of the MapReduce paradigm using Cloud Serverless technologies.

We followed this tutorial: https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
Also used: https://github.com/awslabs/lambda-refarch-mapreduce

## Pre-requisites
Set up the AWS configuration
```
import boto3
s3 = boto3.client('s3')
```

## Functioning
Create a new bucket:
```
s3.create_bucket(Bucket='mapreducesd')
```
Upload a file use the following command:
```
s3.upload_file(filename, mapreducesd, input)
```
Run the lambda function
For downloading the results:
```
s3.download_file('mapreducesd', 'output', 'output.txt')
```

## Authors

* **Aleix Mariné Tena** - [AleixMT](https://github.com/AleixMT)
* **Cristòfol Daudén Esmel** - [toful](https://github.com/toful)