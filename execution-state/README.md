# execution-state
Check Workflow execution state prior to running a workflow

## Usage
This workflow checks the state of the latest executions of a given workflow. One use case for this workflow is to ensure that only 
one execution of a given workflow is running at any given time.

## Prerequisites
1. GCP project.
2. Service account with Cloud Functions Invoker, Compute Admin, Pub/Sub Admin, and Workflows Admin permissions.

## Usage
1. Deploy all workflows in the 'workflow-definitions' folder. Use the service account created in the Prerequisites section.
2. Configure the input file. See example in the "supporting-documents" folder

### Supporting References
1. [Workflow Executions API](https://cloud.google.com/workflows/docs/reference/executions/rest).
2. [executions.list method](https://cloud.google.com/workflows/docs/reference/executions/rest/v1/projects.locations.workflows.executions/list).
3. [Workflow State enum](https://cloud.google.com/workflows/docs/reference/executions/rest/v1/projects.locations.workflows.executions#State).