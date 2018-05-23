import boto3
import botocore

# Aquesta funcio te com a trigger la creacio d'un fitxer en la carpeta Split_Files_WC. 
# La funcio rep aquest event com a parametre, que conte la ruta al fitxer que ha causat l'activacio del trigger.
# Aquest mapper executa la funcio WC i salva el resultat a Treated_Chunks
# TODO: parametritzar nom del fitxer causant del trigger

def lambda_handler(event, context):
    # Obtenim host de s3
    s3_client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')

    # Guardem nom en una variable
    REMOTE_PATH = event.get("Records")[0].get("s3").get("object").get("key")
    NUM_FOLDERS = len(REMOTE_PATH.split('/'))
    NAME = REMOTE_PATH.split('/')[NUM_FOLDERS-1]
    
    # Download the file from S3 and obtain plain text 
    s3_client.download_file('mapreducesd', REMOTE_PATH, '/tmp/input.txt')
    text = open('/tmp/input.txt', 'r').read()
    result = {}
    
    #WC
    text = text.translate(None, "-?.!,;:()\"").lower() # deleting trash characters
    for line in text.split("\n"):
        for word in line.strip().split():  
            if word in result:
                result[word] = result.get(word)+1
            else:
                result[word] = 1
    
    # Save result into /Treated_Chunks/$(event.filename())
    with open('/tmp/output.csv', 'w') as f:
        for key, value in result.items():
            f.write('%s:%s\n' % (key, value))
    
    # Upload result into Treated_Chunks folder
    s3_client.upload_file('/tmp/output.csv', 'mapreducesd', 'Treated_Chunks/o'+NAME )

    # Auto-clean
    s3_client.delete_object(Bucket='mapreducesd', Key=REMOTE_PATH)
    
    return 0