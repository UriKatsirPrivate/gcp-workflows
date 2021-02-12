from __future__ import print_function
from googleapiclient.discovery import build
import json
import sys

from google.oauth2 import service_account
import googleapiclient.discovery


import argparse
import os

#  Authenticate using Service Account
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SERVICE_ACCOUNT_FILE = 'security/uri-test-38aacab75c2a.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# ===================================================================

# # Local testing
dlp = build('dlp', 'v2', credentials=credentials)
# # -------------------------------------------------------------

# # Run on GCP
# # dlp = build('dlp', 'v2')
# # -------------------------------------------------------------


# def inspect_gcs_file(project,bucket,filename,info_types,min_likelihood=None,max_findings=None,timeout=300):
def inspect_gcs_file(request):
    """Uses the Data Loss Prevention API to analyze a file on GCS.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        bucket: The name of the GCS bucket containing the file, as a string.
        filename: The name of the file in the bucket, including the path, as a
            string; e.g. 'images/myfile.png'.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
        timeout: The number of seconds to wait for a response from the API.
    Returns:
        None; the response from the API is printed to the terminal.
    """
    # request_json = request.get_json()
    request_json = request
    project = request_json['project']
    bucket = request_json['bucket']
    filename = request_json['filename']
    info_types = request_json['inspectJob']['inspectConfig']['infoTypes']
    min_likelihood = request_json['inspectJob']['inspectConfig']['minLikelihood']
    max_findings = None
    max_findings = None



    if not info_types:
        info_types = ["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"]

    inspect_config = {
        "info_types": info_types,
        "min_likelihood": min_likelihood,
        "limits": {"max_findings_per_request": max_findings},
    }

    # Construct a storage_config containing the file's URL.
    url = "gs://{}/{}".format(bucket, filename)
    storage_config = {"cloud_storage_options": {"file_set": {"url": url}}}

    # Convert the project id into full resource ids.
    parent = f"projects/{project}"

    # Construct the inspect_job, which defines the entire inspect content task.
    inspect_job = {
        "inspectConfig": inspect_config,
        "storageConfig": storage_config
        # "actions": actions,
    }

    body = {"inspectJob": inspect_job}
    # body =  {"inspectJob":{"inspectConfig":{"infoTypes":[{"name":"PHONE_NUMBER"}],"minLikelihood":"LIKELIHOOD_UNSPECIFIED"},"storageConfig":{"cloudStorageOptions":{"fileSet":{"url":"gs://uri-test-dlp/keep.txt"}}}}}

    operation = dlp.projects().dlpJobs().create(
        parent=parent, body=body).execute()

    print("Inspection operation started: {}".format(operation.get("name")))

    return operation


# info_types = [{"name": info_type} for info_type in
#               ["PERSON_NAME", "ORGANIZATION_NAME", "LAST_NAME", "URL", "CREDIT_CARD_NUMBER", "DOMAIN_NAME", "EMAIL_ADDRESS", "ETHNIC_GROUP", "FIRST_NAME", "LAST_NAME", "GCP_CREDENTIALS", "PHONE_NUMBER"]]

# info_types = [{"name": info_type} for info_type in
#               ["PHONE_NUMBER"]]

# inspect_gcs_file("uri-test", "uri-test-dlp", "keep.txt",
#                  info_types, "LIKELIHOOD_UNSPECIFIED", None, 300)

request = '{"project":"uri-test","bucket":"uri-test-dlp","filename":"keep.txt","inspectJob":{"inspectConfig":{"infoTypes":[{"name":"PERSON_NAME"},{"name":"ORGANIZATION_NAME"},{"name":"LAST_NAME"},{"name":"URL"},{"name":"CREDIT_CARD_NUMBER"},{"name":"DOMAIN_NAME"},{"name":"EMAIL_ADDRESS"},{"name":"ETHNIC_GROUP"},{"name":"FIRST_NAME"},{"name":"LAST_NAME"},{"name":"GCP_CREDENTIALS"},{"name":"PHONE_NUMBER"}],"minLikelihood":"LIKELIHOOD_UNSPECIFIED"},"storageConfig":{"cloudStorageOptions":{"fileSet":{"url":"gs://uri-test-dlp/keep.txt"}}}}}'
inspect_gcs_file(json.loads(request))
