import boto3

s3 = boto3.client('s3')
lambda_client = boto3.client('lambda_client')

s3.upload_file('input.txt', 'distributedsystemsurv', 'input/input')

lambda_client.invoke(
     FunctionName='WordCountMap',
     InvocationType='Event',
     Payload=''
)

s3.download_file('distributedsystemsurv', 'mapper_output/output', 'output.txt')

'''import boto3

iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')

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
