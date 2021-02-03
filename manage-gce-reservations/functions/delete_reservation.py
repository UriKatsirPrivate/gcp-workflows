# from google_auth_oauthlib.flow import InstalledAppFlow
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
gce_service = build('compute', 'v1', credentials=credentials)
# -------------------------------------------------------------

# Run on GCP
# gce_service = build('compute', 'v1')
# -------------------------------------------------------------


def delete_reservation(request):
    # request_json = request.get_json()
    # project = request_json['project']
    project = 'uri-test'
    # zone = request_json['zone']
    zone = 'us-central1-a'
    reservation_name = 'gce1'
    # reservation_name = request_json['body']['name']

    try:
        reservation = gce_service.reservations().delete(
            project=project, zone=zone, reservation=reservation_name).execute()
    except Exception as e:
        print(e)
    else:
        return reservation


input1 = {"project": "uri-test"}
delete_reservation(input1)
