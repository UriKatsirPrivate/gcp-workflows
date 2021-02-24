from googleapiclient.discovery import build
import json
import sys

import googleapiclient.discovery

# Run on GCP
gce_service = build('compute', 'v1')
# -------------------------------------------------------------


def delete_reservation(request):
    request_json = request.get_json()
    project = request_json['project']
    zone = request_json['zone']
    reservation_name = request_json['body']['name']

    try:
        reservation = gce_service.reservations().delete(
            project=project, zone=zone, reservation=reservation_name).execute()
    except Exception as e:
        print(e)
    else:
        return reservation
