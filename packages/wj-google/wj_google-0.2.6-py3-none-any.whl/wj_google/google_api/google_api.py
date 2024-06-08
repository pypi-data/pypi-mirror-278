import os
import io
import logging
from typing import List, Optional

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

from .Google import Create_Service

logger = logging.getLogger(__name__)


class GoogleApi:
    """Google API client construct"""

    def __init__(
        self, client_secret_file: str, api_name: str, api_version, scopes: List[str]
    ) -> None:
        self.api_service = Create_Service(
            client_secret_file, api_name, api_version, scopes
        )

    def upload_files_to_drive(
        self, folder_id: str, file_paths: List[str], mime_types: List[str]
    ) -> List[str]:
        """Given a file, upload it to the folder indicated by the folder id"""
        files_ids = []
        for file_path, mime_type in zip(file_paths, mime_types):
            file_metadata = {"name": file_path.split("/")[-1], "parents": [folder_id]}

            media = MediaFileUpload(file_path, mime_type)

            file = (
                self.api_service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            files_ids.append(file.get("id"))

        return files_ids

    def download_files_drive(
        self,
        file_ids: List[str],
        file_names: List[str],
        destination_path: Optional[str] = None,
    ) -> None:
        """Given a file id, download it to the file path give"""
        for file_id, file_name in zip(file_ids, file_names):
            request = self.api_service.files().get_media(fileId=file_id)

            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fd=fh, request=request)
            done = False

            while not done:
                status, done = downloader.next_chunk()
                print("Download progress {0}".format(status.progress() * 100))

            fh.seek(0)
            path = destination_path if destination_path else "./"
            with open(os.path.join(path, file_name), "wb") as f:
                f.write(fh.read())
                f.close()

    def create_directory_drive(
        self, directory_name: str, directory_id: Optional[str] = None
    ) -> str:
        """Given folder name, creat it in a given directory, or in root path"""
        file_metadata = {
            "name": directory_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if directory_id:
            file_metadata["parents"] = [directory_id]
        directory = self.api_service.files().create(body=file_metadata).execute()
        return directory.get("id")

    def delete_directory_or_file_drive(self, entity_id: str) -> None:
        """Given a folder or file id, delete it"""
        self.api_service.files().delete(fileId=entity_id).execute()
