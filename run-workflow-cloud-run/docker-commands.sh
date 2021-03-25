docker build -t gcr.io/uri-test/run-workflow-cloud-run:v1 .
docker push gcr.io/uri-test/run-workflow-cloud-run:v1
gcloud run deploy run-workflow-cloud-run --image gcr.io/uri-test/run-workflow-cloud-run:v1 --platform managed --region us-central1 --allow-unauthenticated
