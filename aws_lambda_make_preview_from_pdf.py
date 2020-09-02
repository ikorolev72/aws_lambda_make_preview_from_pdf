import json
import urllib.parse
import boto3
import os
 


print('Loading function')
# Download and read pdf file


s3_client = boto3.client('s3')
bucketOut = "YOURBUCKET-thumbnails"


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    bucketIn = event['Records'][0]['s3']['bucket']['name']
    keyIn = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    downloadPdfPath = '/tmp/file.pdf'
    s3_client.download_file(bucketIn, keyIn, downloadPdfPath)
    for i in ["300", "650"] :
      keyOut=os.path.basename(keyIn)+'_'+i+'.jpg' 
      uploadPdfPath='/tmp/'+keyOut      
      os.system( "/opt/bin/convert -density 600 -thumbnail x"+i+" -background white -alpha remove  -quality 75 -strip "+downloadPdfPath+"[0] "+uploadPdfPath) 
      s3_client.upload_file(uploadPdfPath, bucketOut, keyOut)
    


 
