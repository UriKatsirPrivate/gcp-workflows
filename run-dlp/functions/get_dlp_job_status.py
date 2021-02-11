from __future__ import print_function
from googleapiclient.discovery import build
import json
import sys

from google.oauth2 import service_account
import googleapiclient.discovery


import argparse
import os


# Instantiate a client.
# dlp_client = google.cloud.dlp_v2.DlpServiceClient()

#  Authenticate using Service Account
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = 'security/uri-test-38aacab75c2a.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# ===================================================================

# # Local testing
dlp = build('dlp', 'v2', credentials=credentials)
topic = build('pubsub', 'v1', credentials=credentials)
# # -------------------------------------------------------------

# # Run on GCP
# # dlp = build('dlp', 'v2')
# # -------------------------------------------------------------


def get_dlp_job_status(JobName):
    
    operation = dlp.projects().dlpJobs().get(
        name= JobName).execute()
    
    
    print("Inspection operation started: {}".format(operation.get("state")))

    
jobName = "projects/uri-test/dlpJobs/i-demo"
get_dlp_job_status(jobName)