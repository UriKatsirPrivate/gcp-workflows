docker build -t gcr.io/uri-test/list-instances:latest .
docker push gcr.io/uri-test/list-instances:latest

gcloud run deploy list-instances --image gcr.io/uri-test/list-instances:latest --platform managed --region us-central1 --allow-unauthenticated