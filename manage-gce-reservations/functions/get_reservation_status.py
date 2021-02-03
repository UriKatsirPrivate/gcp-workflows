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


def get_reservation_status(request):
    # request_json = request.get_json()
    # project = request_json['project']
    project = 'uri-test'
    # zone = request_json['zone']
    zone = 'us-east1-c'
    # reservation_name = request_json['name']
    reservation_name = 'gce2'
    reservation_name = request_json['body']['name']

    reservation = gce_service.reservations().get(
        project=project, zone=zone, reservation=reservation_name).execute()

    return reservation


input1 = ''
get_reservation_status(input1)
