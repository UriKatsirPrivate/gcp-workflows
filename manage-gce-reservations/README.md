# manage-gce-reservations
Manages GCE compute reservations

## Main Steps
1. Creates a GCE reservation based on the specification in the input file. see [Sample input file](https://github.com/UriKatsirPrivate/gcp-workflows/blob/main/manage-gce-reservations/supporting-documents/workflow-input.json)
2. The create reservations is an async request so the workflow polls for the status.
3. Once the reservation becomes available, The workflow publishes a message to PubSub.
3. The published message will kick off a compute process that uses the reservation. (Not included in this solution)
4. Once the compute process is done, Publish another message to PubSub, indicating it is OK to delete the reservation.(Not included in this solution)
5. The published message (from step #5 above) will kick off a [workflow that will delete the reservation](https://github.com/UriKatsirPrivate/gcp-workflows/blob/main/manage-gce-reservations/workflow-definitions/DeleteGceReservation.yaml).

## Prerequisites
1. GCP project.
2. Service account with Cloud Functions Invoker, Compute Admin, Pub/Sub Admin, and Workflows Admin permissions.

## Usage
1. Deploy all functions in the 'functions' folder. Use the service account created in the Prerequisites section. 
2. Deploy all workflows in the 'workflow-definitions' folder. Use the service account created in the Prerequisites section. 
3. Create a PubSub topic and subscription.
4. Run the workflows manually or [using Cloud Scheduler](https://cloud.google.com/workflows/docs/schedule-workflow). Use the [workflow-input.json](https://github.com/UriKatsirPrivate/gcp-workflows/blob/main/manage-gce-reservations/supporting-documents/workflow-input.json) as a sample input. (Modify the workflow-input.json file to fit your use case.)

### Supporting References
1. [GCE Reservations REST API](https://cloud.google.com/compute/docs/reference/rest/v1/reservations).
2. [Cron expressions generator](https://www.freeformatter.com/cron-expression-generator-quartz.html) and [Here](https://crontab.cronhub.io/) and [Here](http://www.cronmaker.com/;jsessionid=node01jr1tu19xhphf1oxtzv8emirge173782.node0?0).
3. [Scheduling a workflow using Cloud Scheduler](https://cloud.google.com/workflows/docs/schedule-workflow).