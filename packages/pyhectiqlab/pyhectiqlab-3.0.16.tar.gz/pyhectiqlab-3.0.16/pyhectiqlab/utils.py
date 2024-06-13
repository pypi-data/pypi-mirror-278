import os
import socket
import asyncio
import logging
from typing import List, Optional

logger = logging.getLogger()


def is_running_event_loop() -> bool:
    """Check if an event loop is running."""
    try:
        return asyncio.get_event_loop().is_running()
    except RuntimeError:
        return False


def batched(iterable, n):
    """Yield successive n-sized batches from iterable."""
    for i in range(0, len(iterable), n):
        i1 = min(i + n, len(iterable))
        yield iterable[i:i1]


def list_all_files_in_dir(local_folder: str) -> List[str]:
    """List all files in a directory.
    If the path is a file, the file is returned.

    Args:
        local_folder (str): The folder to list files from.
    """
    if not os.path.exists(local_folder):
        raise FileNotFoundError(f"Directory {local_folder} does not exist.")
    filenames = []
    if not os.path.isdir(local_folder):
        # If the path is a file, return the file
        return [local_folder]

    for el in os.walk(local_folder):
        for f in os.listdir(el[0]):
            complete_path = os.path.join(el[0], f)
            if not os.path.isdir(complete_path):
                if os.path.isfile(complete_path):
                    filenames.append(complete_path)
    return filenames


def extract_host_from_source(source: str) -> str:
    """Extract the resource from a path.

    If the path is a cloud path (e.g., s3://bucket/dataset), the resource is inferred from the path.
    If the path is a local path, the resource is set to "local" if not provided.

    Args:
        path (str): The path to extract the resource from.
        default_resource (str): The resource to compare the path with.
    """
    if source.startswith("s3://"):
        return "s3"
    elif source.startswith("gs://"):
        return "gs"
    else:
        return socket.gethostname()


async def queue_gather(tasks: List[callable], workers: Optional[int] = 10):
    """Gather tasks using a queue and workers.
    The tasks will be placed in a queue and workers will be
    created to process the tasks.
    The workers will be stopped when the queue is empty.

    Example usage:

    ```python
    async def task():
        await asyncio.sleep(1)
        return "done"
    tasks = [task() for _ in range(10)]
    results = await queue_gather(tasks)
    print(results)
    ```

    Args:
        tasks (List[callable]): A list of async methods
        workers (Optional[int], optional): The number of workers. Defaults to 10.
    """

    async def worker(i: int, queue: asyncio.Queue):
        """Worker to process tasks from a queue."""
        results = []
        while queue.empty() == False:
            logger.debug(f"Worker {i}. Queue size: {queue.qsize()}")
            idx, task = await queue.get()
            try:
                result = await task
                results.append((idx, result))
            except Exception as e:
                print(e)
                results.append((idx, None))
            finally:
                queue.task_done()
        return results

    queue = asyncio.Queue()
    [queue.put_nowait((i, task)) for i, task in enumerate(tasks)]
    # Create workers
    workers = [asyncio.create_task(worker(idx, queue)) for idx in range(workers)]
    await queue.join()
    for worker in workers:
        worker.cancel()
    results = await asyncio.gather(*workers, return_exceptions=True)
    flatten_results = [result for worker_results in results for result in worker_results]
    flatten_results.sort(key=lambda x: x[0])
    return [result for (_, result) in flatten_results]
