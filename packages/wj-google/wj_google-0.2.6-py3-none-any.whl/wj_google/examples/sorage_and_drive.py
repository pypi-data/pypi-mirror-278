import os

from google_cloud.cloud_connector import GoogleStorage
from google_api.google_api import GoogleApi

from dotenv import load_dotenv

load_dotenv()  # For Windows systems

# Google API config
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
API_NAME = os.getenv("API_NAME")
API_VERSION = os.getenv("API_VERSION")
GOOGLE_DRIVE_SCOPES = os.getenv("GOOGLE_DRIVE_SCOPES")

# Google storage service
GOOGLE_STORAGE_CREDENTIALS = os.getenv("GOOGLE_STORAGE_CREDENTIALS")
STORAGE_SERVICE = "STORAGE"
BIGQUERY = "BIGQUERY"
BUCKET = os.getenv("BUCKET_NAME")


def create_directory_in_drive(directory_name):
    googleApi = GoogleApi(
        client_secret_file=CLIENT_SECRET_FILE,
        api_name=API_NAME,
        api_version=API_VERSION,
        scopes=GOOGLE_DRIVE_SCOPES,
    )
    googleApi.create_directory_drive(directory_name=directory_name)


def upload_files_to_drive(folder_id, file_paths, mime_types):
    googleApi = GoogleApi(
        client_secret_file=CLIENT_SECRET_FILE,
        api_name=API_NAME,
        api_version=API_VERSION,
        scopes=GOOGLE_DRIVE_SCOPES,
    )
    googleApi.upload_files_to_drive(
        folder_id=folder_id, file_paths=file_paths, mime_types=mime_types
    )


def download_file_from_drive(file_ids, file_names, path=None):
    googleApi = GoogleApi(
        client_secret_file=CLIENT_SECRET_FILE,
        api_name=API_NAME,
        api_version=API_VERSION,
        scopes=GOOGLE_DRIVE_SCOPES,
    )
    googleApi.download_files_drive(
        file_ids=file_ids, file_names=file_names, destination_path=path
    )


def upload_file_to_bucket(bucket_name, file_to_upload, file_path):
    googleStorageClient = GoogleStorage(
        service=STORAGE_SERVICE, credentials=GOOGLE_STORAGE_CREDENTIALS
    )
    googleStorageClient.upload_file(
        bucket_name=bucket_name,
        source_file_name=file_to_upload,
        destination_file_name=file_path,
    )


def download_file_from_bucket(bucket_name, file_name, destination):
    googleStorageClient = GoogleStorage(
        service=STORAGE_SERVICE, credentials=GOOGLE_STORAGE_CREDENTIALS
    )
    googleStorageClient.download_file(
        bucket_name=bucket_name,
        file_name=file_name,
        destination_file=destination,
    )


def create_bucket(bucket_name, storage_class="STANDARD", location="us-central1"):
    googleStorageClient = GoogleStorage(
        service=STORAGE_SERVICE, credentials=GOOGLE_STORAGE_CREDENTIALS
    )
    googleStorageClient.create_bucket(bucket_name, storage_class, location)


def list_bucket_files(bucket_name):
    googleStorageClient = GoogleStorage(
        service=STORAGE_SERVICE, credentials=GOOGLE_STORAGE_CREDENTIALS
    )
    return googleStorageClient.list_files(bucket_name)
