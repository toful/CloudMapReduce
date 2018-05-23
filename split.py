import boto3
import botocore
import os
import codecs


# aquesta funcio rep com a parametre la funcio a executar [WC|CW], el nombre de mappers i el nom del fitxer a tractar.
# Llegeix de Input_Files/event.nomfitxer, divideix el fitxer en event.nummapers i guarda cada tros a la carpeta Treated_Chunks_event.funcio/numfitxer.txt
# aixo causara l'activacio de les funcions mapper corresponents en escriure a la carpeta concreta.
# TODO obtenir informacio del event per a parametritzar.

def lambda_handler(event, context):
    # Obtenim host client
    s3_client = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')

    # Download the file from S3
    s3_client.download_file('mapreducesd', 'Input_Files/'+event.get("filename"), '/tmp/input.txt')

    # Count lines
    num_lines = sum(1 for line in open("/tmp/input.txt"))

    # Calculate the size of the chunks (adding 1 could be a problem for small files and many mappers, but we need it since it's a non-real operation)
    splitLen = (num_lines / int(event.get("nummappers"))) + 1
    count = 0
    at = 0
    dest = None
    input = open('/tmp/input.txt', 'r+')
    for line in input:
        if count % splitLen == 0:
            if dest: dest.close()
            at += 1
            dest = open('/tmp/'+str(at)+'.txt', 'w+')
        dest.write(line)
        count += 1
    
    dest.close()
    # upload chunks 
    for num in range(1, at + 1):
        s3_client.upload_file('/tmp/'+str(num)+'.txt', 'mapreducesd', 'Split_Files_'+event.get("function")+'/o'+str(num)+'.txt')

    # Now mappers are running
    return 0