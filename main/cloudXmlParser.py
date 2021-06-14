

from google.cloud import storage
import xml.etree.ElementTree as ET
from xmlParser import parse_managers_from_root


# bucket used to store managers data
manager_bucket = 'mfp-managers'

def parse_xml(event, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       computes managers data from XML file .

    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        managers dataframe is stored in Storage under manager bucket
    """


    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))

    # get bucket with name
    client = storage.Client()
    bucket = client.get_bucket( event["bucket"] )
    # get bucket data as blob
    blob = bucket.get_blob( event["name"] )
    # convert to string
    contents = blob.download_as_string()
    myroot = ET.fromstring(contents)

    #compute managers data
    managers = parse_managers_from_root(myroot)

    #store result in storage
    bucket = client.get_bucket(manager_bucket)
    bucket.blob(event['name'] + '.csv').upload_from_string(managers.to_csv(), 'text/csv')