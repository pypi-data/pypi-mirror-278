# Standard Library Imports
import logging
import random
import time

# 3rd-Party Imports
import requests

# Application-Local Imports
from capiche.lib import CallbackHandler, ThrottledQueue
from capiche.lib.constants import THREAD_SLEEP_TIME
from capiche.lib.exceptions import QueueFullException

logging.basicConfig(filename="/tmp/example.log", level=logging.INFO)


def do_call(duration: int) -> str:
    # time.sleep(duration)
    return f"do call: {duration}"


def call_remote_api() -> requests.Response:
    endpoint = "https://official-joke-api.appspot.com/random_joke"
    logging.debug(f"Making request to {endpoint}")
    response = requests.get(url=endpoint)
    logging.debug(f"Made request to {endpoint}")
    return response


def handle_response(response: requests.Response):
    response = response.json()
    logging.info(f"Response: {response['setup']} {response['punchline']}")


if __name__ == "__main__":
    t = ThrottledQueue(
        max_rate=1,
        window=3,
        cache_age=300,
        callback=CallbackHandler[requests.Response](callback=handle_response),
        max_queue_size=None,
    )

    t.start()

    # total_jobs = random.randint(20, 50)
    total_jobs = random.randint(2, 2)
    # total_jobs = random.randint(1,1)

    for _ in range(total_jobs):
        sleep_time = random.randint(1, 5)
        try:
            # t.queue_request(method=do_call, kwargs={"duration": sleep_time}, use_cache=True)
            # t.queue_request(method=call_example_com, use_cache=True)
            t.queue_request(method=call_remote_api, use_cache=False)
        except QueueFullException as e:
            logging.error(e)

    while not t.is_empty:
        logging.debug(t.queued_requests, t.completed_api_call_times, t.cache)
        time.sleep(THREAD_SLEEP_TIME)

    time.sleep(2)
