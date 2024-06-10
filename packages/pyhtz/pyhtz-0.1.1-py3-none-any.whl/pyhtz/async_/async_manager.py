from time import sleep, time
import asyncio
import httpx

class BasicAsyncManager:

    def __init__(self, base_url=None):
        self.base_url = base_url
        self.results = []
        self.request_count = 0  # Add a request count attribute
        self.start_time = None  # Track the start time for request count reset

    def get_tasks(self, session, _requests_list):
        raise NotImplementedError

    @staticmethod
    def async_batcher(_requests, batch_size=100):
        for count, i in enumerate(range(0, len(_requests), batch_size)):
            print(f"Batch {count+1} of {len(_requests) // batch_size}")
            yield _requests[i : i + batch_size]
            
    async def run_async_tasks(self, requests_list, timeout=120.0, connect=60.0):
        timeout = httpx.Timeout(timeout=timeout, connect=connect)
        async with httpx.AsyncClient(timeout=timeout) as client:
            tasks = self.get_tasks(client, requests_list)
            try:
                responses = await asyncio.gather(*tasks)
                return [response.json() for response in responses]
            except Exception as e:
                print(f"Error: {e}")
                return []
    
    def run(self):
        raise NotImplementedError