import boto3
import json
import os
import time
import sys

# Creating json data with arguments
payload = {
  "filename": sys.argv[1],
  "nummappers": sys.argv[2],
  "function": sys.argv[3]
}

if __name__ == "__main__":

  # Create json file
  payload = json.dumps(payload)
  
  # Create clients
  s3_client = boto3.client('s3')
  lambda_client = boto3.client('lambda')

  # check file available
  fitxers = s3_client.list_objects(Bucket='mapreducesd', Prefix='Input_Files/').get('Contents')
  filenames = []

  for file in fitxers:
    filenames.append(file['Key'].split('/')[1])

  # --> If not exists, abort
  if sys.argv[1] not in filenames:
    print 'Input file is not in the Input folder! Aborting...'
    exit()

  # Get working directory
  wd = os.path.dirname(os.path.realpath(__file__))

  # Clean Output files in local machine
  os.system('rm -f '+wd+'/Out.txt')

  # try to delete output object in server
  try:
    s3_client.delete_object(
      Bucket='mapreducesd',
      Key='Output_Files/out.txt')
  except botocore.exceptions.ClientError: 
    print 'Output folder clean.'

  # measure begin time
  begin = time.time()

  # invoke split function
  response = lambda_client.invoke(
      FunctionName='Split',
      InvocationType='Event',
      LogType='Tail',
      Payload=payload
  )

  # wait until file is available
  numfiles = None
  while numfiles is None:
    numfiles = s3_client.list_objects(Bucket='mapreducesd', Prefix='Output_Files/out.txt').get('Contents')
    print 'Result is not available yet. '+str(time.time()-begin)+' seconds transcurred'

  os.system("clear")
  print 'Result Found!'
  
  # measure end time
  end = time.time()

  # download file
  response = s3_client.download_file(
    'mapreducesd', 
    'Output_Files/out.txt', 
    wd+'/Out.txt')

  # calcule RoundTrip_Time
  RoundTrip_time = end - begin

  # Show results file
  print open( wd+'/Out.txt', 'r').read()

  # show transcurred time
  print 'MapReduce RoundTrip time is '+str(RoundTrip_time)+' segons'

  # Salvem resultats de l'execucio
  os.system('echo \"'+sys.argv[1]+';'+ sys.argv[2]+';'+ sys.argv[3]+';'+str(RoundTrip_time)+'\" >> result.csv')

  # Borrem fitxer Out.txt
  os.system("rm -f "+wd+'/'+'Out.txt')

