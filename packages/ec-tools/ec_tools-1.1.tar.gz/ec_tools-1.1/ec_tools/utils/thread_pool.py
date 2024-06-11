import logging
import time
from concurrent.futures import ThreadPoolExecutor, Future

from typing import List, Callable, Any


def try_wrapper(func: Callable, **kwargs):
    try:
        return func(**kwargs)
    except Exception as e:
        logging.error(f"try to run failed with %s", e)


class CustomizedThreadPoolExecutor(ThreadPoolExecutor):
    futures: List[Future[Any]]

    def __init__(
        self, max_workers=None, thread_name_prefix="", initializer=None, initargs=()
    ):
        self.futures = []
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)

    def submit(self, fn, use_try: bool = True, **kwargs):
        if use_try:
            future = super().submit(try_wrapper, func=fn, **kwargs)
        else:
            future = super().submit(fn, **kwargs)
        self.futures.append(future)
        return future

    def join(self, log_time: int = 1, clear_after_wait: bool = True) -> List[Any]:
        while True:
            tasks_left = self._work_queue.qsize()
            if tasks_left > 0:
                logging.info(
                    "[ThreadPool] waiting for %s tasks to complete", tasks_left
                )
                time.sleep(log_time)
            else:
                break
        results = [future.result() for future in self.futures]
        if clear_after_wait:
            self.futures.clear()
        logging.info("[ThreadPool] all futures complete")
        return results

    def __del__(self):
        self.join()
