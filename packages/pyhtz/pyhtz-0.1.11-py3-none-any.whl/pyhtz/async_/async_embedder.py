import subprocess
from typing import List, Dict, Generator
import pandas as pd
from pyhtz.async_.async_manager import BasicAsyncManager
from time import sleep, time
import asyncio


def create_batch(lst: List, batch_size: int) -> Generator:
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]

def create_instances(
    temp_df: pd.DataFrame, text_col: str, batch_size=50, task_type="SEMANTIC_SIMILARITY"
):
    """
    create a list of 5 dicts as instances
    """
    instances = []
    for _, row in temp_df.iterrows():
        instances.append(
            {
                "task_type": task_type,
                "content": row[text_col],
                "article_id": row["article_id"],
            }
        )
    return instances

class GeckoAsyncEmbedder(BasicAsyncManager):

    def __init__(self, base_url=None, api_key=None):
        super().__init__(base_url)
        self.api_key = api_key or subprocess.getoutput("gcloud auth print-access-token")

    def get_tasks(self, session, _requests_list, mini_batch=5):
        tasks = []
        token = subprocess.getoutput("gcloud auth print-access-token")
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        }
        for req in create_batch(_requests_list, mini_batch):
            tasks.append(
                session.post(self.base_url, json={"instances": req}, headers=header)
            )
        return tasks

    def reset_quote_count(self, quote_limit, quote_time_frame):
        if self.request_count >= quote_limit:
            elapsed_time = time() - self.start_time
            if elapsed_time < quote_time_frame:
                pause_duration = int(quote_time_frame - elapsed_time + 1)
                print(f"Quota limit reached. Pausing for {pause_duration} seconds.")
                sleep(pause_duration)
            self.request_count = 0
            self.start_time = time()

    def process_single_batch(
        self,
        batch,
        timeout,
        connect,
        max_retries,
        retry_delay,
        quote_limit,
        quote_time_frame,
    ):
        for attempt in range(max_retries):
            try:
                self.reset_quote_count(quote_limit, quote_time_frame)
                results = asyncio.run(
                    self.run_async_tasks(batch, timeout=timeout, connect=connect)
                )
                self.request_count += len(batch)
                return results
            except Exception as e:
                print(f"Error: {e}. Retrying attempt {attempt + 1} of {max_retries}...")
                sleep(retry_delay)
        print(f"Failed to process batch after {max_retries} attempts.")
        return []

    def run(
        self,
        requests_list,
        batch_size=1000,
        timeout=120.0,
        connect=60.0,
        max_retries=3,
        retry_delay=2,
        quote_limit=10000,
        quote_time_frame=60.0,
        flatten=True,
    ):
        self.start_time = time()
        results = []

        if isinstance(requests_list, str):
            requests_list = [requests_list]

        for batch in self.async_batcher(requests_list, batch_size=batch_size):
            batch_results = self.process_single_batch(
                batch,
                timeout=timeout,
                connect=connect,
                max_retries=max_retries,
                retry_delay=retry_delay,
                quote_limit=quote_limit,
                quote_time_frame=quote_time_frame,
            )
            results.extend(batch_results)

        if flatten:
            return [
                item["embeddings"]["values"]
                for sublist in [r["predictions"] for r in results]
                for item in sublist
            ]

        return results

    def __call__(self, requests_list, *args, **kwargs):
        results = self.run(requests_list, *args, **kwargs)
        return results




