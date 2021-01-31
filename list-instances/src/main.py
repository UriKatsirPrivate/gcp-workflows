# from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import sys
# import create_machine_image
import os
from flask import Flask

app = Flask(__name__)


#  Authenticate using Service Account
# SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
# SERVICE_ACCOUNT_FILE = 'security/uri-test-38aacab75c2a.json'
# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# ===================================================================


# gce_service = build('compute', 'v1', credentials=credentials)
# gce_service = build('compute', 'v1')

# project_name = 'uri-test'
# zone = 'us-east1-b'


@app.route("/")
# def list_instances(project_name, zone):
def list_instances(request):
    envelope = request.get_json()
    msg = "envelope"
    print(f"envelope = {msg}")
    return f"envelope is: {msg}", 400
    gce_service = build('compute', 'v1')
    project_name = 'uri-test'
    zone = 'us-east1-b'

    # instances = gce_service.instances().list(project='uri-test', zone='us-east1-b').execute()
    instances = gce_service.instances().list(
        project=project_name, zone=zone).execute()
    # for instance in instances['items']:
    #     name = instance['name']
    #     name = (name[:40]) if len(name) > 40 else name
    #     selfLink = instance['selfLink']

    # create_machine_image.Insert_Machine_Image(project_name,instances)

    return instances


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# list_instances(project_name, zone)
