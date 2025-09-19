import os
from datetime import datetime, timedelta, timezone
import requests
from azure.storage.blob import (
    BlobSasPermissions,
    BlobServiceClient,
    generate_blob_sas,
)
from dotenv import load_dotenv


def ensure_container(service_client, container_name: str):
    """Create the container if it does not exist."""
    container_name = container_name.lower() 
    container_client = service_client.get_container_client(container_name)
    try:
        container_client.create_container()
        print(f"Container '{container_name}' created.")
    except Exception as e:
        if "ContainerAlreadyExists" in str(e):
            print(f"Container '{container_name}' already exists.")
        else:
            raise
    return container_client


def upload_blob_with_sas(blob_client, account_name, account_key, container_name, blob_name, local_file):
    """Upload a local file to blob storage using a SAS URL and show HTTP status."""
    sas_permissions = BlobSasPermissions(read=True, write=True, create=True)
    sas_start_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    sas_expiry_time = sas_start_time + timedelta(hours=1)

    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=sas_permissions,
        start=sas_start_time,
        expiry=sas_expiry_time,
    )

    upload_url = f"{blob_client.url}?{sas_token}"

    with open(local_file, "rb") as file:
        file_contents = file.read()

    headers = {
        "x-ms-blob-type": "BlockBlob",
        "Content-Type": "application/octet-stream",
    }

    response = requests.put(upload_url, data=file_contents, headers=headers)

    if response.status_code == 201:
        print(f"Upload succeeded: {blob_name} → HTTP {response.status_code}")
    else:
        print(f"Upload failed: HTTP {response.status_code}, Response: {response.text}")


def main():
    load_dotenv()

    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")
    local_file = os.getenv("LOCAL_FILE")

    blob_name = os.path.basename(local_file)

    service_client = BlobServiceClient.from_connection_string(connect_str)

    container_client = ensure_container(service_client, container_name)
    blob_client = service_client.get_blob_client(container=container_name, blob=blob_name)

    upload_blob_with_sas(blob_client, account_name, account_key, container_name, blob_name, local_file)


if __name__ == "__main__":
    main()
