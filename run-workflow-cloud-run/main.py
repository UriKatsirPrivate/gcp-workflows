import os

from flask import Flask

from googleapiclient.discovery import build
import json
import sys

from google.oauth2 import service_account
import googleapiclient.discovery

app = Flask(__name__)

workflow_service = build('workflowexecutions', 'v1')


@app.route("/")
def hello_world():
    parent = "projects/uri-test/locations/us-central1/workflows/CreateMachineImagesInAllZones"
    body = {"argument": '{"project": "uri-test","zone": "us-east1-b"}'}

    workflow = workflow_service.projects().locations().workflows(
    ).executions().create(parent=parent, body=body).execute()

    return workflow


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
