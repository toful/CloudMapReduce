import boto3

lambda_handler({
  "filename": "pg10.txt",
  "nummappers": "30",
  "function": "WC"
}, None)

def lambda_handler(event, context):
    
    # Obtain host
    s3 = boto3.client('s3', aws_access_key_id='AKIAJOMQJL3QTFKQ33WQ', aws_secret_access_key='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')
    
    # Data output structure
    mappers_output = []
    result = {}

    # listing files in the mapper input directory 
    WORKING_DIR = event.get("Records")[0].get("s3").get("object").get("key").split("/")[0]
    
    resp = s3.list_objects(Bucket='mapreducesd', Prefix=WORKING_DIR+'/o')
    filenames = resp.get('Contents')
    
    # if there are any file then mappers havent finished
    if filenames:
        print 'mappers havent finished; going to sleep'
        return 1

    # if not, mappers have finished; so list files in Treated_Chunks/
    
    # if there aren't any files in the mappers input directory (Split_Files_FUNCTION) but there aren't either any files
    # in treated_chunks, then there is a missynchonization due to the lack of consistency

    files = s3.list_objects(Bucket='mapreducesd', Prefix='Treated_Chunks/o').get('Contents')
    filenames = []
    # append filenames
    for file in files:
        print "Reading file "+file
        filenames.append(file['Key'])
        
    # Read and append all results from all mappers:
    for file in filenames:
        s3.download_file('mapreducesd', file, '/tmp/input.txt')
        # Reading a dictionary from a file
        with open('/tmp/input.txt', 'r') as f:
            dict = {}
            text = f.read()
            for line in text.split('\n'):
                values = line.split(':')
                if values[0] != '': 
                    dict[values[0]] = int(values[1:len(values)][0])
            mappers_output.append(dict)

    #Reduce function:
    for hashes in mappers_output:
        for key in hashes.keys():
            if key in result:
                result[key] = result[key]+[hashes[key]]
            else:
                result[key] = [hashes[key]]
    for word in result.keys():
        if len(result[word]):
            result[word] = sum(result[word])
    
    #Saving the result in S3
    with open('/tmp/output.csv', 'w') as f:
        for key, value in result.items():
            f.write('%s:%s\n' % (key, value))
    
    s3.upload_file('/tmp/output.csv', 'mapreducesd', 'Output_Files/out.txt')
    
    # Autoclean
    for file in filenames:
        print file
        s3.delete_object(Bucket='mapreducesd', Key=file)

    return 0
