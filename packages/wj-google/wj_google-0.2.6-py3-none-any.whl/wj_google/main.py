from examples.sorage_and_drive import *
from examples.bigquery import *

if __name__ == "__main__":
    command = str(input("Enter command: "))

    if command == "upload_to_drive":
        folder_id = "1XFeGaXDL9D6xGbw40jJ2FUMLzG0LY9BJ"
        file_paths = ["G:/Proyectos/Python/Libs/wj-google/files/dark_dragon.jpg"]
        mime_types = ["image/jpeg"]
        upload_files_to_drive(folder_id, file_paths, mime_types)

    if command == "download_from_drive":
        # File id to download from Drive and the name of the file in local
        file_ids = ["121La8gl0HURGIk-_pmJMOjT9G4KsSR0b"]
        file_names = ["image.jpg"]
        download_file_from_drive(file_ids, file_names)

    if command == "download_from_drive_with_path":
        # File id to download from Drive and the name of the file in local
        file_ids = ["121La8gl0HURGIk-_pmJMOjT9G4KsSR0b"]
        file_names = ["image.jpg"]
        path = "d:/Descargas"
        download_file_from_drive(file_ids, file_names, path)

    if command == "create_directory_in_drive":
        directory_name = "test"
        create_directory_in_drive(directory_name)

    if command == "upload_to_bucket":
        # File downloaded from  Drive and path for bucket
        FILE_TO_UPLOAD = "G:/Proyectos/Python/Libs/wj_google/files/image.jpg"
        FILE_PATH = "files/image.jpg"
        bucket_name = "jcmantilla_bucket"
        upload_file_to_bucket(bucket_name, FILE_TO_UPLOAD, FILE_PATH)

    if command == "download_from_bucket":
        bucket_name = "jcmantilla_bucket"
        file_name = "files/image.jpg"
        destination = "G:/Proyectos/Python/Libs/wj_google/files/image.jpg"
        download_file_from_bucket(bucket_name, file_name, destination)

    if command == "create_bucket":
        bucket_name = "jcmantilla_test_bucket"
        create_bucket(bucket_name)

    if command == "list_bucket_files":
        bucket_name = "jcmantilla_bucket"
        print(list_bucket_files(bucket_name))

    if command == "bigquery_consult":
        query = """
         SELECT * FROM `test.tw` LIMIT 10
        """
        query_job = sql_query(query)

    if command == "add_table_label_bigquery":
        dataset_name = "dt_OCEANA_Holberton"
        table_name = "test_Holberton"
        labels = {
            "type": "social_media",
            "category": "cloud",
        }
        add_labels_in_table(labels, dataset_name, table_name)

    if command == "delete_table_label_bigquery":
        dataset_name = "dt_OCEANA_Holberton"
        table_name = "test_Holberton"
        delete_labels_in_table(dataset_name, table_name)

    if command == "save_query_as_table":
        query = """
        SELECT * FROM `thematic-cider-416220.dt_OCEANA_Holberton.test_Holberton` LIMIT 100
        """
        destination_dataset_name = "reports"
        destination_table_name = "test_table"
        save_query_as_table(query, destination_dataset_name, destination_table_name)

    '''if command == "export_querys_to_Excel":
        query1 = """
        SELECT * FROM `test.tw` LIMIT 10
        """
        query2 = """
        SELECT * FROM `reports.reports` LIMIT 10
        """
        queries = [query1, query2]
        export_queries_to_excel(queries=queries)'''
