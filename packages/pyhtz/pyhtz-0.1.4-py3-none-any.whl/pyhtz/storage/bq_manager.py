import datetime
from urllib.parse import urlparse
from google.cloud.exceptions import GoogleCloudError
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.bigquery_storage import types
from google.cloud import bigquery_storage
import pyarrow.dataset as ds
import pandas as pd

        
class BqReader:
    WRITE_DISPOSITION = "WRITE_TRUNCATE"
    EXPIRATION_DAYS = 1
    MAX_TABLE_ROWS = 20_000
    
    def __init__(
        self,
        query_path: str,
        destination_table: str,
        storage_uri: str,
        project_id: str,
        temp_table_name:str,
        use_streaming: bool = True,
        batch_size: int = None
    ):
        self.query_path = query_path
        self.destination_table = destination_table
        self.storage_uri = storage_uri
        self.project_id = project_id
        self.temp_table_name = temp_table_name
        self.batch_size = batch_size
        self.client = bigquery.Client(project=self.project_id)
        self.query = self.read_query()
        self.use_streaming = use_streaming
    
        
    def read_query(self):
        with open(self.query_path) as f:
            query = f.read()
        return query
    
    def get_query_config(self):
        return bigquery.QueryJobConfig(
        destination=self.destination_table,
        write_disposition=self.WRITE_DISPOSITION,
        )
        

    def run_bigquery_query(self, query, job_config=None):
        query_job = self.client.query(query, job_config=job_config)
        return query_job
    
    def check_query_state(self, query_job, timeout=3600):
        import time
        counter = 0
        while query_job.state != "DONE" and counter < timeout:
            time.sleep(10)
            counter += 10
            query_job.reload()
        return True if query_job.state == "DONE" else False

    @staticmethod
    def extract_bucket_name_and_prefix(gcs_uri):
        parsed_url = urlparse(gcs_uri)
        bucket_name = parsed_url.netloc
        prefix = parsed_url.path.strip("/")
        return bucket_name, prefix
    
    def get_blobs(self):
        bucket_name, prefix = self.extract_bucket_name_and_prefix(self.storage_uri)
        storage_client = storage.Client(project=self.project_id)
        bucket = storage_client.get_bucket(bucket_name)

        return bucket.list_blobs(prefix=prefix)
    
    def remove_all_blobs(self):
        blobs = self.get_blobs()
        for blob in blobs:
            blob.delete()
            
    def get_files_uris(self):
        bucket_name, prefix = self.extract_bucket_name_and_prefix(self.storage_uri)
        blobs = self.get_blobs()
        return [f'gs://{bucket_name}/{blob.name}'
                for blob in blobs
            ]
    
    def get_table(self):
        return self.client.get_table(self.destination_table)
    
    def get_table_properties(self):
        table = self.get_table()
        return table.to_api_repr()
    
    def change_expire_date(self) -> None:
        table = self.get_table()
        expiration_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                days=self.EXPIRATION_DAYS
             )
        table.expires = expiration_date
        self.client.update_table(table, ["expires"])
        
    def run_extract_table_job(self, extract_job_config=None):
        table = bigquery.table.Table(table_ref=self.temp_table_name)

        if extract_job_config is None:
            extract_job_config = {}
        job_config = bigquery.job.ExtractJobConfig(**extract_job_config)
        table_atrr = self.client.get_table(table).to_api_repr()
        
        if not extract_job_config.get('destination_format'):
            raise ValueError(f"destination format must be specified. - Options : ['CSV', 'PARQUET', 'AVRO']")
        
        export_uri = self.storage_uri + '/*-.' + extract_job_config.get('destination_format').lower()
        extract_job = self.client.extract_table(
            table,
            export_uri,
            job_config=job_config,
        )

        try:
            result = extract_job.result()
        except GoogleCloudError as e:
            print(f"Error extracting table - {e}")
            raise e
              
    def extract_job(self):
        
        query_job = self.run_bigquery_query(
            self.query, 
            job_config=self.get_query_config()
        )
        self.check_query_state(query_job)
        self.change_expire_date()
        
    def use_storage(self):    
        extract_job_config = {
            "destination_format": "PARQUET",
            "compression": "GZIP",
        }
        self.remove_all_blobs()
        self.run_extract_table_job(extract_job_config=extract_job_config)
        files = self.get_files_uris()
        dataset = ds.dataset(self.storage_uri)
        if self.batch_size:
            batched_dataset = dataset.to_batches(batch_size=self.batch_size)
            for batch in batched_dataset:
                yield batch.to_pandas()
        else:
            for file in files:
                yield pd.read_parquet(file)
        
    def stream_reader(self):
        bqstorageclient = bigquery_storage.BigQueryReadClient()
        requested_session = types.ReadSession(
        table='projects/{project_id}/datasets/{dataset_id}/tables/{table_id}'.format(
            project_id=self.project_id,
            dataset_id=self.destination_table.split('.')[1],
            table_id=self.destination_table.split('.')[2],
        ),
        data_format=types.DataFormat.ARROW,
        read_options=None,
        )
        read_session = bqstorageclient.create_read_session(
            parent="projects/{}".format(self.project_id),
            read_session=requested_session,
            max_stream_count=1,
        )
        stream = read_session.streams[0]
        reader = bqstorageclient.read_rows(stream.name)
        for message in reader.rows().pages:
            yield message.to_dataframe()
        
    def load_bq(self):
        self.extract_job()
        num_rows = int(self.get_table_properties().get('numRows'))
        if num_rows > self.MAX_TABLE_ROWS and not self.use_streaming:
            return  self.use_storage()
        else:
            return self.stream_reader()
        
        
        