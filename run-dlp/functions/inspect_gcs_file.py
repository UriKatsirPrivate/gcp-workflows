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
# topic = build('pubsub', 'v1', credentials=credentials)
# # -------------------------------------------------------------

# # Run on GCP
# # dlp = build('dlp', 'v2')
# # -------------------------------------------------------------


def inspect_gcs_file(
    project,
    bucket,
    filename,
    topic_id,
    subscription_id,
    info_types,
    custom_dictionaries=None,
    custom_regexes=None,
    min_likelihood=None,
    max_findings=None,
    timeout=300,
):
    """Uses the Data Loss Prevention API to analyze a file on GCS.
    Args:
        project: The Google Cloud project id to use as a parent resource.
        bucket: The name of the GCS bucket containing the file, as a string.
        filename: The name of the file in the bucket, including the path, as a
            string; e.g. 'images/myfile.png'.
        topic_id: The id of the Cloud Pub/Sub topic to which the API will
            broadcast job completion. The topic must already exist.
        subscription_id: The id of the Cloud Pub/Sub subscription to listen on
            while waiting for job completion. The subscription must already
            exist and be subscribed to the topic.
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

    # import google.cloud.dlp

    # import google.cloud.pubsub

    # Instantiate a client.
    # dlp = google.cloud.dlp_v2.DlpServiceClient()

    # Prepare info_types by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    if not info_types:
        info_types = ["FIRST_NAME", "LAST_NAME", "EMAIL_ADDRESS"]
    info_types = [{"name": info_type} for info_type in info_types]

    # Prepare custom_info_types by parsing the dictionary word lists and
    # regex patterns.
    if custom_dictionaries is None:
        custom_dictionaries = []
    dictionaries = [
        {
            "info_type": {"name": "CUSTOM_DICTIONARY_{}".format(i)},
            "dictionary": {"word_list": {"words": custom_dict.split(",")}},
        }
        for i, custom_dict in enumerate(custom_dictionaries)
    ]
    if custom_regexes is None:
        custom_regexes = []
    regexes = [
        {
            "info_type": {"name": "CUSTOM_REGEX_{}".format(i)},
            "regex": {"pattern": custom_regex},
        }
        for i, custom_regex in enumerate(custom_regexes)
    ]
    custom_info_types = dictionaries + regexes

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        "info_types": info_types,
        "custom_info_types": custom_info_types,
        "min_likelihood": min_likelihood,
        "limits": {"max_findings_per_request": max_findings},
    }

    # Construct a storage_config containing the file's URL.
    url = "gs://{}/{}".format(bucket, filename)
    storage_config = {"cloud_storage_options": {"file_set": {"url": url}}}

    # Convert the project id into full resource ids.
    # topic = google.cloud.pubsub.PublisherClient.topic_path(project, topic_id)
    parent = f"projects/{project}"

    # Tell the API where to send a notification when the job is complete.
    # actions = [{"pub_sub": {"topic": topic}}]

    # Construct the inspect_job, which defines the entire inspect content task.
    inspect_job = {
        "inspectConfig": inspect_config,
        "storageConfig": storage_config,
        # "actions": actions,
    }

    body = {"inspectJob":{"inspectConfig":{"infoTypes":[{"name":"PHONE_NUMBER"}],"minLikelihood":"LIKELIHOOD_UNSPECIFIED"},"storageConfig":{"cloudStorageOptions":{"fileSet":{"url":"gs://uri-test-dlp/keep.txt"}}}}}

    operation = dlp.projects().dlpJobs().create(
        parent= parent, body=body).execute()
    
    # operation = dlp.create_dlp_job(
    #     request={"parent": parent, "inspect_job": inspect_job}
    # )
    print("Inspection operation started: {}".format(operation.get("name")))

    # Create a Pub/Sub client and find the subscription. The subscription is
    # expected to already be listening to the topic.
    # subscriber = google.cloud.pubsub.SubscriberClient()
    # subscription_path = subscriber.subscription_path(project, subscription_id)


info_types = [{"name": info_type} for info_type in
              ["CREDIT_CARD_NUMBER", "AUSTRALIA_TAX_FILE_NUMBER", "EMAIL_ADDRESS", "ETHNIC_GROUP", "FIRST_NAME", "LAST_NAME", "GCP_CREDENTIALS", "PHONE_NUMBER"]]
# info_types = [{"name": info_type} for info_type in
#               ["PHONE_NUMBER"]]
inspect_gcs_file("uri-test", "uri-test-dlp", "keep.txt",
                 "workflows-demo", "workflows-demo-sub", info_types)

ddd =''