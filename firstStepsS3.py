import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)

# Upload a new file
data = open('prova.txt', 'rb')
s3.Bucket('mapreducesd').put_object(Key='prova.txt', Body=data)

#---------------------------------------------------

# Create an S3 client
s3 = boto3.client('s3')

# Call S3 to list current buckets
response = s3.list_buckets()
# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]
# Print out the bucket list
print("Bucket List: %s" % buckets)

#Creating a bucket
s3.create_bucket(Bucket='my-bucket')

#Uploading a file
filename = 'file.txt'
bucket_name = 'my-bucket'
# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
s3.upload_file(filename, bucket_name, filename)

#downloading it
s3.download_file(bucket_name, filename, '/tmp/'+filename)