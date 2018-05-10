import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3', aws_access_key_id='AKIAJOMQJL3QTFKQ33WQ', aws_secret_access_key='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')
    s3.download_file('mapreducesd', 'input', '/tmp/input.txt')
    text = open('/tmp/input.txt', 'r').read()
    result = {}
    
    text = text.translate(None, "-?.!,;:()\"").lower() # deleting trash characters
    for line in text.split("\n"):
        for word in line.strip().split():  
            if word in result:
                result[word] = result.get(word)+1
            else:
                result[word] = 1
    # Save
    with open('/tmp/output.csv', 'w') as f:
        for key, value in result.items():
            f.write('%s:%s\n' % (key, value))
    s3.upload_file('/tmp/output.csv', 'mapreducesd', 'output')
    
    return 0
    