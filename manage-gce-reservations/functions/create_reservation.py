from googleapiclient.discovery import build
import json
import sys

import googleapiclient.discovery

# Run on GCP
gce_service = build('compute', 'v1')
# -------------------------------------------------------------


def create_reservation(request):
    request_json = request.get_json()
    project = request_json['project']
    zone = request_json['zone']
    body = request_json['body']

    try:
        reservation = gce_service.reservations().insert(
            project=project, zone=zone,body=body).execute()
    except Exception as e:    
        print(e)
    else:
        return reservation