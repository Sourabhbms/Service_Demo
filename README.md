# Azurite Azure Blob Storage Demo

This project demonstrates how to interact with **Azure Blob Storage** using Python, with **Azurite** as a local emulator for development and testing. It covers:

- Creating containers in Azure Blob Storage.
- Uploading local files as blobs.
- Generating SAS URLs for secure access (optional).
- Listing blobs in a container.
- Using `.env` for configuration management.

---

## Project Structure

project/
│── scripts/
│ ├── azurite_connector.py # Upload files to Azurite storage
│ ├── list_azurite_container_files.py # List files in a container
│── .env # Environment variables
│── .gitignore


---

## Features

1. **Upload files to Azure Blob (Azurite local emulator)**  
   - Normalizes container names to avoid invalid characters.
   - Handles file upload with overwrite option.
   - Uses SAS tokens securely for blob upload.
   - Prints HTTP status (`201`) after successful upload.

2. **List blobs in a container**  
   - Quickly fetch all blob names in a given container.
   - Helps verify uploads without accessing Azurite’s internal storage files.

3. **Environment-based configuration**  
   - All sensitive credentials and configurations are stored in `.env`.
   - Supports easy migration to actual Azure Blob Storage by updating the `.env`.

---

## Prerequisites

- Python 3.12+
- [Azurite] installed for local testing
- `pip` for Python dependencies

Install required packages:

```bash
pip install -r requirements.txt

Configuration (.env)

Create a .env file in the project root:

AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=<your-key>;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;
AZURE_STORAGE_ACCOUNT_NAME=devstoreaccount1
AZURE_STORAGE_ACCOUNT_KEY=<your-key>
AZURE_STORAGE_CONTAINER=azuritedemocontainer
LOCAL_FILE=/path/to/local_file.txt

Replace <your-key> with your Azurite account key (default for Azurite is provided).

Usage
1. Upload a file
python scripts/main.py


Output example:

Container 'azuritedemocontainer' created.
✅ Upload succeeded: local_file.txt → HTTP 201

2. List files in a container
python scripts/list_blobs.py


Output example:

Blobs in container 'azuritedemocontainer':
 - local_file.txt

Notes

.env file is gitignored to keep credentials safe.

The project uses timezone-aware datetimes to avoid deprecation warnings.

Designed for local development with Azurite but can be pointed to a real Azure Storage account by updating the connection string.

Optional Improvements

Add a download script to fetch blobs locally.

Extend to handle multiple file uploads.

Integrate with Azure Functions or other workflows for automated processing.

License

MIT License