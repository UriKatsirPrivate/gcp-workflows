from googleapiclient.discovery import build
import json
import sys

import googleapiclient.discovery

# Run on GCP
gce_service = build('compute', 'v1')
# -------------------------------------------------------------


def get_reservation_status(request):
    request_json = request.get_json()
    project = request_json['project']
    zone = request_json['zone']
    reservation_name = request_json['body']['name']

    reservation = gce_service.reservations().get(
        project=project, zone=zone, reservation=reservation_name).execute()

    return reservation