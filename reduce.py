import boto3

def lambda_handler(event, context):
    
    s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
    
    mappers_output = []
    
    # Getting all files in the output directory 
    resp = s3.list_objects(Bucket='distributedsystemsurv', Prefix='mapper_output/o')
    files = []
    for file in resp['Contents']:
        files.append(file['Key'])
        
    #Fem la comprovació de que ja estàn tots els resultats del maper en el directori mapper_output/
    if False:
        return "not all mappers had finished yet"
    
    # Reading all results from all mappers:
    for file in files:
        s3.download_file('distributedsystemsurv', file, '/tmp/input.txt')
        # Reading a dictionary from a file
        with open('/tmp/input.txt', 'r') as f:
            dict = {}
            for line in text.split('\n'):
                values = line.split(':')
                dict[values[0]] = values[1:len(values)]
            mappers_output.append(dict)

    #Reduce function:
    for hashes in mappers_output:
        for key in hashes.keys():
            if key in result:
                result[key] = result[key]+[hashes[key]]
            else:
                result[key] = [hashes[key]]
    for word in result.keys():
        result[word] = sum(result[word])
    
    #Saving the result in S3
    with open('/tmp/output.csv', 'w') as f:
        for key, value in result.items():
            f.write('%s:%s\n' % (key, value))
    s3.upload_file('/tmp/output.csv', 'distributedsystemsurv', 'reduce_output/output')
    
    return "done"
