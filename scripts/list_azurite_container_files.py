import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Load config from .env
load_dotenv()

CONNECT_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER")

def list_blobs(container_name: str):
    """List all blobs in the specified container."""
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container_client = blob_service_client.get_container_client(container_name)

    print(f"Blobs in container '{container_name}':")
    blobs = container_client.list_blobs()
    for blob in blobs:
        print(" -", blob.name)

if __name__ == "__main__":
    list_blobs(CONTAINER_NAME)
