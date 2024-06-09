# Replace with your project ID and region
project_id = "allm-421908"
region = "us-east1"

# Set the model name
model_name = "gemini-1.5-pro-preview-0409"

# Import libraries
from google.cloud import aiplatform_v1

# 0Create the service object
endpoint = aiplatform_v1.EndpointServiceClient()

# Prepare the input text
text_payload = {"inputs": [{"text": "Hello"}]}

# Send inference request
response = endpoint.get_endpoint(
    endpoint=endpoint.endpoint_path(project=project_id, location=region, endpoint=model_name),
    instances=text_payload,
)

# Access the prediction
predictions = response.predictions

# Print the prediction
print(predictions[0])
