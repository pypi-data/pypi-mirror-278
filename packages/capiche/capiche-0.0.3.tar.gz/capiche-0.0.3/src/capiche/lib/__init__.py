# Standard Library Imports
import logging
import threading
import time
from collections import deque
from datetime import UTC, datetime, timedelta
from typing import Callable, Dict, List, Optional

# Local Folder Imports
from .constants import DEFAULT_CACHE_DURATION, THREAD_SLEEP_TIME
from .exceptions import QueueFullException

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class CallbackHandler[T]:
    def __init__(self, callback: Callable):
        self.callback = callback

    def __call__(self, response: T):
        return self.callback(response=response)


class ThrottledRequest:
    def __init__(self, method: Callable, args: List | None = None, kwargs: Dict | None = None, use_cache: bool = False):
        self.method = method
        self.args = args
        self.kwargs = kwargs
        self.use_cache = use_cache

    def __repr__(self):
        return f"ThrottledRequest(method={self.method.__name__}, args={self.args}, kwargs={self.kwargs}, use_cache={self.use_cache})"

    @property
    def cache_key(self) -> str:
        return f"{self.method.__name__}{str(self.args)}{str(self.kwargs)}"


class ThrottledQueue(threading.Thread):
    def __init__(
        self,
        max_rate: int,
        window: int,
        callback: CallbackHandler,
        max_queue_size: Optional[int] = None,
        cache_age: int = DEFAULT_CACHE_DURATION,
    ):
        threading.Thread.__init__(self, target=self.run, daemon=True)

        # cache of responses
        self.cache = {}

        # work to be done goes here
        self.queue = deque()

        # list of timestamps of requests made
        self.completed_api_call_times = []

        # The maximum number of requests that can be made in the window
        self.max_rate = max_rate

        # The maximum number of requests that can be queued. if None, no limit
        self.max_queue_size = max_queue_size

        # Dict of duration of the API rate limit for each source
        self.window = window

        # The time, in seconds, for which to cache a response
        self.cache_age = cache_age

        # Callback function to be called when a request is made
        self.callback = callback

    def __repr__(self):
        return f"ThrottledQueue(max_rate={self.max_rate}, window={self.window}, callback={self.callback.__name__}, max_queue_size={self.max_queue_size}, cache_age={self.cache_age}"

    @property
    def callback_name(self) -> str:
        return self.callback.callback.__name__

    @property
    def rate(self) -> int:
        # Returns the number of requests made in the last window
        return len(self.completed_api_call_times)

    @property
    def rate_limit_reached(self) -> bool:
        return self.rate >= self.max_rate

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    @property
    def is_full(self) -> bool:
        if self.max_queue_size is None:
            return False

        return len(self.queue) >= self.max_queue_size

    @property
    def queued_requests(self) -> int:
        return len(self.queue)

    def trim_cache(self) -> None:
        # Removes cache entries that are older than the cache_age
        cutoff = datetime.now(UTC) - timedelta(seconds=self.cache_age)
        removables = []

        # for key, (timestamp, _) in self.cache.items():
        for key, (timestamp, _) in list(self.cache.items()):
            if timestamp < cutoff:
                removables.append(key)

        for key in removables:
            logger.debug(f"removing {key} from cache")
            self.cache.pop(key)

    def trim_completed(self) -> None:
        # Removes completed timestamps that are older than the window
        cutoff = datetime.now(UTC) - timedelta(seconds=self.window)
        cutoff_index = None

        for i, timestamp in enumerate(self.completed_api_call_times):
            if timestamp < cutoff:
                cutoff_index = i

        if cutoff_index is not None:
            logger.info(f"removing {cutoff_index + 1} completed requests from queue")
            self.completed_api_call_times = self.completed_api_call_times[cutoff_index + 1 :]

    def run(self):
        last_log_line = ""
        repeats = 0

        while True:
            self.trim_completed()
            self.trim_cache()

            if not self.is_empty:
                # if exceed max rate, need to wait
                if self.rate_limit_reached:
                    time.sleep(THREAD_SLEEP_TIME)
                else:
                    # remove the oldest request from the queue and process it
                    request = self.queue.popleft()
                    logger.info(f"processing request: {request}")
                    logger.info(f"self.queue length: {len(self.queue)}")
                    self.process_request(request)

    def queue_request(
        self, method: Callable, args: List | None = None, kwargs: Dict | None = None, use_cache: bool = False
    ) -> ThrottledRequest:
        if self.is_full:
            raise QueueFullException

        request = ThrottledRequest(method=method, use_cache=use_cache, kwargs=kwargs, args=args)
        self.queue.append(request)
        return request

    def process_request(self, request: ThrottledRequest) -> None:
        now = datetime.now(UTC)

        logger.info(
            f"request.use_cache: {request.use_cache}, request.cache_key: {request.cache_key}, self.cache: {self.cache}"
        )

        if request.use_cache and request.cache_key in self.cache:
            logger.debug(f"Making request with cache key: {request.cache_key}")
            timestamp, data = self.cache[request.cache_key]

            if (now - timestamp).seconds < self.cache_age:
                logger.debug(f"calling callback: {self.callback_name}")
                # Don't need to mark this as a call made to the external service since we just used the cached copy
                self.callback(data)
                # Our work here is done
                return
        else:
            logger.debug(f"Making request without cache key: {request.cache_key}")

        if request.args is None:
            args = []
        else:
            args = request.args

        if request.kwargs is None:
            kwargs = {}
        else:
            kwargs = request.kwargs

        logging.critical(f"calling method: {request.method.__name__}")

        response = request.method(*args, **kwargs)  # potential exception raise

        logging.critical(f"response: {response}")

        self.completed_api_call_times.append(now)

        if request.use_cache:
            logger.debug(f"Caching response {response} with cache key: {request.cache_key}")
            # cache the response
            self.cache[request.cache_key] = (now, response)
            logger.debug(f"self.cache: {self.cache.keys()}")

        logger.debug(f"calling callback: {self.callback_name}")
        self.callback(response)

        return
