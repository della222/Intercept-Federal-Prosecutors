import re
from google.cloud import vision
import os
from dotenv import load_dotenv
import json
from google.cloud import storage
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np


def get_pdf_text(court, pdf_name):  # takes pandas input of two columns

    # get credentials for API
    
    credentials = os.getenv("GOOGLEAPIKEY")
    client = vision.ImageAnnotatorClient.from_service_account_json(credentials)
    
    batch_size=100
    mime_type = 'application/pdf'
    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION
    )

    # GCS source (where pdf is stored on cloud)
    gcs_source_uri = f'gs://intercept/pdfs/{court}/{pdf_name}.pdf'
    gcs_source = vision.GcsSource(uri=gcs_source_uri)

    # set configs for input data
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    # set destination on google cloud
    gcs_destination_uri = f'gs://intercept/texts/{court}/{pdf_name}/'
    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)

    # set configs for output
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client.from_service_account_json(credentials)

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    blob_list = [i for i in blob_list if i.name[-5:] == ".json"]
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json.loads(json_string)
    
    '''
    turn decision json to text and upload text back to cloud if text contains mentions of:
    "posecutorial misconduct"
    "prosecutor"
    "misconduct"
    "prosecutor committed misconduct" 
    '''

    # turn all json texts to string
    decision = ''
    num_pages = len(response['responses'])
    for i in range(num_pages):
        decision += response['responses'][i]['fullTextAnnotation']['text']

    print('\nFull Decision:\n')
    print(decision)

    # upload to google cloud if case contains mentions of misconduct
    if 'prosecutorial misconduct' in decision or 'prosecutorial' in decision or 'misconduct' in decision or 'prosecutor committed misconduct' in decision:
        output_destination = f'texts/{court}/{pdf_name}/'
        decision_blob = bucket.blob(output_destination + f'{pdf_name}.txt')
        decision_blob.upload_from_string(decision)
        print('\nSuccessfully uploaded to cloud!')
        return True
    else:
        print('\nNo mentions of misconduct!')
        return False
    
    

if __name__ == "__main__":
    load_dotenv(override=True)
    cases = pd.read_csv("newCases.csv")
    cases_with_mentions = cases[cases.apply(lambda x: get_pdf_text(x.Court, x.Case_ID), axis=1) == True]  # only add cases where misconduct was true
    cases_with_mentions.to_csv("newCasesWithMentions.csv", index=False)