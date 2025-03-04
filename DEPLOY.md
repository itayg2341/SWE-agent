
# Deployment Instructions

These instructions assume you have a Docker image built from the api/Dockerfile.

## Generic Cloud Deployment

1. Build the Docker image: `docker build -t swe-agent-api -f api/Dockerfile .`
2. Push the image to your cloud provider's container registry (e.g., AWS ECR, Google Container Registry, Azure Container Registry).
3. Create a deployment configuration for your cloud provider, specifying the image, ports, and any other necessary settings.
4. Deploy the service.

## Example using Google Cloud Run

1. Build the Docker image: `docker build -t swe-agent-api -f api/Dockerfile .`
2. Tag the image for Google Cloud Run: `docker tag swe-agent-api gcr.io/<your-project-id>/swe-agent-api`
3. Push the image to Google Container Registry: `docker push gcr.io/<your-project-id>/swe-agent-api`
4. Deploy to Cloud Run: `gcloud run deploy swe-agent-api --image gcr.io/<your-project-id>/swe-agent-api --platform managed --region <your-region>`

Replace `<your-project-id>` and `<your-region>` with your actual values.