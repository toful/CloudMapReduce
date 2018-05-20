import boto3
import json
import os
import time

# Creating json data with arguments
payload = {
  "filename": "pg10.txt",
  "nummappers": "10",
  "function": "CW"
}
payload = json.dumps(payload)

# Create clients
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

try:
  s3_client.delete_object(
    Bucket='mapreducesd',
    Key='Output_Files/out.txt')
except botocore.exceptions.ClientError: 
  print 'Output folder clean.'

# invoke split function
response = lambda_client.invoke(
    FunctionName='Split',
    InvocationType='Event',
    LogType='Tail',
    Payload=payload
)

# Get working directory
wd = os.path.dirname(os.path.realpath(__file__))

os.system('rm '+wd+'/Out.txt')

# download file
time.sleep(10)
response = s3_client.download_file(
  'mapreducesd', 
  'Output_Files/out.txt', 
  wd+'/Out.txt')

print open( wd+'/Out.txt', 'r').read()

'''
   response = client.invoke(
        FunctionName='my_lambda_function',
        #InvocationType='RequestResponse',
        InvocationType='Event',
        LogType='Tail',
        Payload=payload,

aws lambda invoke \
--invocation-type Event \
--function-name CreateThumbnail \
--region region \
--payload file://file-path/inputfile.txt \
--profile adminuser \
outputfile.txt

env_variables = dict() # Environment Variables

with open('lambda.zip', 'rb') as f:
  zipped_code = f.read()

role = iam_client.get_role(RoleName='LambdaBasicExecution')

lambda_client.create_function(
  FunctionName='myLambdaFunction',
  Runtime='python2.7',
  Role=role['Role']['Arn'],
  Handler='main.handler',
  Code=dict(ZipFile=zipped_code),
  Timeout=300, # Maximum allowable timeout
  Environment=dict(Variables=env_variables),
)'''
