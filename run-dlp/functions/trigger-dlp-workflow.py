from googleapiclient.discovery import build
import json
import sys

from google.oauth2 import service_account
import googleapiclient.discovery

#  Authenticate using Service Account
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = 'security/uri-test-38aacab75c2a.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# ===================================================================

# Local testing
workflow_service = build('workflowexecutions', 'v1', credentials=credentials)
# -------------------------------------------------------------

# Run on GCP
# workflow_service = build('workflowexecutions', 'v1')
# -------------------------------------------------------------


def trigger_gcs_dlp(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # request_json = request.get_json()
    # parent = request_json['parent']
    parent = "projects/uri-test/locations/us-central1/workflows/DlpGcsFile"
    # body = json.dumps(event)

    body = {"argument": json.dumps(event)}

    # body = {"argument": '{"project": "uri-test","zone": "us-east1-b"}'}
    workflow = workflow_service.projects().locations().workflows().executions().create(
        parent=parent, body=body).execute()

    # file = event
    # print(f"Processing file: {file['name']}.")
    # print(f"Processing file: {json.dumps(event)}.")

    return workflow
event = {"bucket":"uri-test-dlp","contentType":"text/plain","crc32c":"2enkOw==","etag":"CIKA5IKE5O4CEAE=","generation":"1613122076475394","id":"uri-test-dlp/keep.txt/1613122076475394","kind":"storage#object","md5Hash":"DpPur/sDZO8mt1t6tQ2B8w==","mediaLink":"https://www.googleapis.com/download/storage/v1/b/uri-test-dlp/o/keep.txt?generation=1613122076475394&alt=media","metageneration":"1","name":"keep.txt","selfLink":"https://www.googleapis.com/storage/v1/b/uri-test-dlp/o/keep.txt","size":"1234","storageClass":"STANDARD","timeCreated":"2021-02-12T09:27:56.485Z","timeStorageClassUpdated":"2021-02-12T09:27:56.485Z","updated":"2021-02-12T09:27:56.485Z"  }
trigger_gcs_dlp(event,'')