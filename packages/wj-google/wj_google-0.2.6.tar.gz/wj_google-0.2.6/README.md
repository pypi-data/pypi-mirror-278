# wj_google
## Connection to GCP
In order to use the client, you need a json [credentials](https://cloud.google.com/docs/authentication/application-default-credentials?hl=es-419) from the google project. The first time to connect to a service, It is necessary to authorize the app through the browser.

## Supported services

The currently supported services are:
- Google Drive
- Buckets
- BigQuery

## Google Drive
The GCP account must have Google Drive API enabled, and make sure that you have a OAuth 2.0 application created, in Google Cloud console, you can see the [documentation](https://developers.google.com/drive/api/guides/about-sdk?hl=es-419).

The following methods are currently supported:
- Upload files
- Download files
- Create directory
You must The package must be instantiated as follows:
```
from wj_google.google_api.google_api import GoogleApi

googleApi = GoogleApi(
    client_secret_file=CLIENT_SECRET_FILE, -> Json file must be configured in GCP
    api_name=API_NAME, -> drive in this case
    api_version=API_VERSION, -> Current version, 3 in this case
    scopes=GOOGLE_DRIVE_SCOPES, -> Scope of drive see doc
)
```
There are diferent scopes, as you can see in the [documentation](https://developers.google.com/drive/api/guides/api-specific-auth?hl=es-419).

## Google Drive
The GCP account must have Google Drive API enabled, and make sure that you have a OAuth 2.0 application created, in Google Cloud console, you can see the [documentation](https://developers.google.com/drive/api/guides/about-sdk?hl=es-419).

The following methods are currently supported:
- Upload files
- Download files
- Create directory

To use the library, it is necessary to prepare the credentials, and then instantiate the service that will be used.
```
from wj_google.google_api.google_api import GoogleApi

googleApi = GoogleApi(
    client_secret_file=CLIENT_SECRET_FILE, -> Json file must be configured in GCP
    api_name=API_NAME, -> drive in this case
    api_version=API_VERSION, -> Current version, 3 in this case
    scopes=GOOGLE_DRIVE_SCOPES, -> Scope of drive see doc
)
```
There are diferent scopes, as you can see in the [documentation](https://developers.google.com/drive/api/guides/api-specific-auth?hl=es-419).

### Uploading a file:
```
googleApi.upload_files_to_drive(
    folder_id, -> Id from the drive of the directory 
    file_paths, -> Path of yur file
    mime_types -> Type of file
)
```
### Downloading a file:
```
googleApi.download_files_drive(
    file_ids -> Google Drive id file, you can find it in the uri
    file_names -> Name given in your local
)
```
### Creating a directory:
```
googleApi.create_directory_drive(
    directory_name
)
```

## Google storage buckets

This resource can be used with the credentials of a service user, you see de [documentation](https://cloud.google.com/iam/docs/manage-access-service-accounts?hl=es).

The following methods are currently supported:
- Upload files
- Download files
- Create directory

As in the previous case, credentials are required. After which the resource is instantiated.
```
from wj_google.google_cloud.cloud_connector import GoogleStorage
googleStorageClient = GoogleStorage(
    service -> STORAGE in this case and for now***
    credentials
)
```
### Uploading a file:
```
googleStorageClient.upload_file(
    bucket_name -> Destination bucket 
    source_file_name -> Path of the file to upload
    destination_file_name Name of the file in bucket
)
```
### Downloading a file:
```
googleStorageClient.download_file(
    bucket_name -> bucket file
    file_name -> name and path in the bucket
    destination_file -> name and path in your local of the file
)
```
### Creating a bucket:
```
googleStorageClient.create_bucket(
    bucket_name,
    storage_class, -> Optional, to define the type of bucket to use
    location, -> Optional, to define in which region the bucket is hosted 
)
```
### Listing bucket's files:
```
googleStorageClient.list_files(bucket_name)
```

## Google BigQuery
This resource can be used with the credentials of a service user, you see de [documentation](https://cloud.google.com/python/docs/reference/bigquery/latest).


With the credentials are required. After which the resource is instantiated, in this case just execute the query.
```
from google_cloud.cloud_connector import GoogleBigQuery

bigquery = GoogleBigQuery(
    service=BIGQUERY,
    credentials=GOOGLE_BIGQUEY_CREDENTIALS,
    scopes=scopes -> To use services like Google Drive
)

```
### Do a consult:

```
query = 'YOUR_SQL_QUERY'
sql_job = bigquery.sql_query(query=query)
```

You can iterate over the sql_job:
```
for item in sql_job:
    print(item.name)
```

### Add label to bigquery table:

```
labels = {
    "type": "social_media",
    "category": "cloud",
}
bigquery = GoogleBigQuery(service=BIGQUERY, credentials=GOOGLE_BIGQUEY_CREDENTIALS)
bigquery.add_table_labels(
    labels=labels, dataset_name=dataset_name, table_name=table_name
)

```
### Delete label to bigquery table:
```
delete_labels_in_table(dataset_name, table_name)
```
