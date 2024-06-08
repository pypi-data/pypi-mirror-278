import os

from google_cloud.cloud_connector import GoogleBigQuery
from dotenv import load_dotenv

load_dotenv()  # For Windows systems

# Google API config
CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
API_NAME = os.getenv("API_NAME")
API_VERSION = os.getenv("API_VERSION")
GOOGLE_DRIVE_SCOPES = os.getenv("GOOGLE_DRIVE_SCOPES")

# Google storage service
GOOGLE_BIGQUEY_CREDENTIALS = os.getenv("GOOGLE_BIGQUEY_CREDENTIALS")
BIGQUERY = "BIGQUERY"
BUCKET = os.getenv("BUCKET_NAME")


def sql_query(query):
    bigquery = GoogleBigQuery(service=BIGQUERY, credentials=GOOGLE_BIGQUEY_CREDENTIALS)
    sql_job = bigquery.sql_query(query=query)
    for item in sql_job:
        print(item)


def add_labels_in_table(labels, dataset_name, table_name):
    bigquery = GoogleBigQuery(service=BIGQUERY, credentials=GOOGLE_BIGQUEY_CREDENTIALS)
    bigquery.add_table_labels(
        labels=labels, dataset_name=dataset_name, table_name=table_name
    )


def delete_labels_in_table(dataset_name, table_name):
    bigquery = GoogleBigQuery(service=BIGQUERY, credentials=GOOGLE_BIGQUEY_CREDENTIALS)
    bigquery.delete_table_labels(dataset_name=dataset_name, table_name=table_name)


def save_query_as_table(query, destination_dataset_name, destination_table_name):
    bigquery = GoogleBigQuery(service=BIGQUERY, credentials=GOOGLE_BIGQUEY_CREDENTIALS)
    bigquery.save_query_as_table(
        query=query,
        destination_dataset_name=destination_dataset_name,
        destination_table_name=destination_table_name,
    )


def export_queries_to_excel(queries):
    # TODO! make constants for scopes services
    scopes = [
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/bigquery",
    ]
    bigquery = GoogleBigQuery(
        service=BIGQUERY, credentials=GOOGLE_BIGQUEY_CREDENTIALS, scopes=scopes
    )
    bigquery.export_queries_to_excel(queries=queries)
