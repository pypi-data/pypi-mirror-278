import httpx
import asyncio
import threading
import logging
import os
import io

from typing import Any, Optional, List, Type, Union
from functools import partial
from google.resumable_media.requests import ResumableUpload
from rich.progress import Progress, TimeRemainingColumn, TaskProgressColumn, BarColumn, TextColumn, FileSizeColumn

from pyhectiqlab.auth import Auth
from pyhectiqlab.decorators import classproperty, request_handle
from pyhectiqlab.settings import getenv
from pyhectiqlab import API_URL


logger = logging.getLogger()

ResponseType = Union[dict[str, Any], bytes, Type[None]]


class Client:
    """
    Client singleton for making sync and async requests in the Hectiq Lab API. This client
    can be used in a context manager, or as a singleton. For performing async requests, the object
    must be instanciated.

    Example:
    ```python
    from pyhectiqlab.client import Client
    import asyncio

    client = Client()

    # Sync request
    response = client.get("/app/auth/is-logged-in")

    # Async request
    response = asyncio.run(client.async_get("/app/auth/is-logged-in"))
    ```
    """

    _auth: Auth = None
    _client: httpx.Client = None
    _online: bool = True
    _timeout: float = 30.0  # seconds

    @classproperty
    def auth(cls) -> Auth:
        if cls._auth is None:
            cls._auth = Auth()
        return cls._auth

    @classproperty
    def client(cls) -> httpx.Client:
        if cls._client is None:
            cls._client = httpx.Client(auth=cls.auth, timeout=cls._timeout)
        return cls._client

    @staticmethod
    def is_logged():
        return Client.auth.is_logged()

    @staticmethod
    def online(status: Optional[bool] = None):
        if status is not None:
            Client._online = status
        return Client.auth.online and Client._online

    @staticmethod
    def get(url: str, wait_response: bool = False, **kwargs: Any) -> ResponseType:
        return Client.request("get", url, wait_response=wait_response, **kwargs)

    @staticmethod
    def post(url: str, wait_response: bool = False, **kwargs: Any) -> ResponseType:
        return Client.request("post", url, wait_response=wait_response, **kwargs)

    @staticmethod
    def patch(url: str, wait_response: bool = False, **kwargs: Any) -> ResponseType:
        return Client.request("patch", url, wait_response=wait_response, **kwargs)

    @staticmethod
    def put(url: str, wait_response: bool = False, **kwargs: Any) -> ResponseType:
        return Client.request("put", url, wait_response=wait_response, **kwargs)

    @staticmethod
    def delete(url: str, wait_response: bool = False, **kwargs: Any) -> ResponseType:
        return Client.request("delete", url, wait_response=wait_response, **kwargs)

    @staticmethod
    def upload_sync(local_path: str, policy: dict, progress: Optional[Progress] = None) -> ResponseType:
        """Upload a file."""
        upload_method = policy.get("upload_method")
        if not upload_method:
            return

        if upload_method == "fragment":
            res = Client.upload_fragment_sync(local_path, policy, progress=progress)
        elif upload_method == "single":
            res = Client.upload_single_sync(
                local_path, policy.get("policy"), bucket=policy.get("bucket_name"), progress=progress
            )
        return res

    @staticmethod
    async def upload_async(local_path: str, policy: dict, progress: Optional[Progress] = None) -> ResponseType:
        """Upload a file."""
        upload_method = policy.get("upload_method")
        if not upload_method:
            return

        async with httpx.AsyncClient(timeout=Client._timeout) as asyncClient:
            if upload_method == "fragment":
                res = await Client.upload_fragment_async(local_path, policy, client=asyncClient, progress=progress)
            elif upload_method == "single":
                res = await Client.upload_single_async(
                    local_path,
                    policy.get("policy"),
                    bucket=policy.get("bucket_name"),
                    client=asyncClient,
                    progress=progress,
                )
        return res

    @staticmethod
    def get_upload_method(policy: dict) -> dict[str, Any]:
        """Get the upload method from the policy."""
        if "upload_method" in policy:
            return policy.get("upload_method")
        return policy.get("policy", {}).get("upload_method")

    @staticmethod
    def upload_many_sync(paths: List[str], policies: List[dict], progress: Optional[Progress] = None) -> None:
        """Upload many files synchronously."""
        single_upload_files = []
        fragment_upload_files = []
        for path, policy in zip(paths, policies):
            if not policy:
                continue
            method = Client.get_upload_method(policy)
            if method == "fragment":
                fragment_upload_files.append((path, policy))
            elif method == "single":
                single_upload_files.append((path, policy))

        for path, policy in single_upload_files:
            Client.upload_single_sync(path, policy.get("policy"), bucket=policy.get("bucket_name"), progress=progress)
        for path, policy in fragment_upload_files:
            Client.upload_fragment_sync(path, policy, progress=progress)

    @staticmethod
    async def upload_many_async(paths: List[str], policies: List[dict], progress: Optional[Progress] = None) -> None:
        """Upload many files asynchronously."""
        single_upload_files = []
        fragment_upload_files = []
        for path, policy in zip(paths, policies):
            if not policy:
                continue
            method = Client.get_upload_method(policy)
            if method == "fragment":
                fragment_upload_files.append((path, policy))
            elif method == "single":
                single_upload_files.append((path, policy))

        async with httpx.AsyncClient() as client:
            tasks = []
            for path, policy in single_upload_files:
                task = Client.upload_single_async(
                    path, policy.get("policy"), bucket=policy.get("bucket_name"), client=client, progress=progress
                )
                tasks.append(asyncio.ensure_future(task))
            for path, policy in fragment_upload_files:
                task = Client.upload_fragment_async(path, policy, client=client, progress=progress)
                tasks.append(asyncio.ensure_future(task))
            await asyncio.gather(*tasks)

    @staticmethod
    def upload_fragment_sync(
        local_path: str, policy: dict, chunk_size: int = 1024 * 1024 * 32, progress: Optional[Progress] = None
    ) -> None:
        """Upload a file in fragments."""
        upload = ResumableUpload(upload_url=policy.get("url"), chunk_size=chunk_size)
        data = open(local_path, "rb").read()
        upload._stream = io.BytesIO(data)
        upload._total_bytes = len(data)
        upload._resumable_url = policy.get("url")

        if progress is not None:
            filename = os.path.basename(local_path)
            task_desc = f"Upload {filename if len(filename) <= 15 else filename[:12] + '...'}"
            task_id = progress.add_task(task_desc, total=upload.total_bytes)
        bytes_uploaded = 0
        while upload.finished == False:
            method, url, payload, headers = upload._prepare_request()
            if headers.get("content-type") == None:
                headers["content-type"] = "application/octet-stream"
            result = httpx.request(method, url, data=payload, headers=headers, timeout=Client._timeout)
            upload._process_resumable_response(result, len(payload))
            if progress is not None:
                progress.update(task_id, advance=upload.bytes_uploaded - bytes_uploaded)
            bytes_uploaded = upload.bytes_uploaded

    @staticmethod
    async def upload_fragment_async(
        local_path: str,
        policy: dict,
        chunk_size: int = 1024 * 1024 * 32,
        client: Optional[httpx.AsyncClient] = None,
        progress: Optional[Progress] = None,
    ) -> None:
        """Upload a file in fragments."""
        upload = ResumableUpload(upload_url=policy.get("url"), chunk_size=chunk_size)
        data = open(local_path, "rb").read()
        upload._stream = io.BytesIO(data)
        upload._total_bytes = len(data)
        upload._resumable_url = policy.get("url")

        if progress is not None:
            filename = os.path.basename(local_path)
            task_desc = f"Upload {filename if len(filename) <= 15 else filename[:12] + '...'}"
            task_id = progress.add_task(task_desc, total=upload.total_bytes)

        bytes_uploaded = 0
        while upload.finished == False:
            method, url, payload, headers = upload._prepare_request()
            if headers.get("content-type") == None:
                headers["content-type"] = "application/octet-stream"
            result = await (client or httpx).request(
                method, url, data=payload, headers=headers, timeout=Client._timeout
            )
            upload._process_resumable_response(result, len(payload))
            if progress is not None:
                progress.update(task_id, advance=upload.bytes_uploaded - bytes_uploaded)
            bytes_uploaded = upload.bytes_uploaded

    @staticmethod
    def upload_single_sync(
        local_path: str, policy: dict, bucket: str, progress: Optional[Progress] = None
    ) -> ResponseType:
        """Upload a file in a single request synchronously."""
        url = policy.get("url")
        content = open(local_path, "rb")
        num_bytes = os.path.getsize(local_path)
        files = {"file": (bucket, content)}
        upload_method = request_handle(httpx.post)
        if progress is not None:
            filename = os.path.basename(local_path)
            task_desc = f"Upload {filename if len(filename) <= 15 else filename[:12] + '...'}"
            task_id = progress.add_task(task_desc, total=num_bytes)
        res = upload_method(url, data=policy.get("fields"), files=files)
        if progress is not None:
            progress.update(task_id, advance=num_bytes)
        return res

    @staticmethod
    async def upload_single_async(
        local_path: str,
        policy: dict,
        bucket: str,
        client: Optional[httpx.AsyncClient] = None,
        progress: Optional[Progress] = None,
    ) -> ResponseType:
        """Upload a file in a single request asynchronously."""
        url = policy.get("url")
        content = open(local_path, "rb")
        num_bytes = os.path.getsize(local_path)
        files = {"file": (bucket, content)}
        upload_method = client.post if client else request_handle(httpx.post)
        if progress is not None:
            filename = os.path.basename(local_path)
            task_desc = f"Upload {filename if len(filename) <= 15 else filename[:12] + '...'}"
            task_id = progress.add_task(task_desc, total=num_bytes)
        res = await upload_method(url, data=policy.get("fields"), files=files)
        if progress is not None:
            progress.update(task_id, advance=num_bytes)
        return res

    @staticmethod
    def download_sync(
        url: str, local_path: str, num_bytes: Optional[int] = None, progress: Optional[Progress] = None
    ) -> str:
        """Download a file synchronously.

        Args:
            url (str): URL of the file to download.
            local_path (str): Local path to save the file (includes the file name)
            num_bytes (Optional[int], optional): Number of bytes to download. Default: None.
            progress: (rich.progress.Progress, optional): Progress object for track download. Default: None.
        """

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            if progress:
                filename = os.path.basename(local_path)
                task_desc = f"Download {filename if len(filename) <= 15 else filename[:12] + '...'}"
                task_id = progress.add_task(task_desc, total=num_bytes)
            with httpx.stream("GET", url) as r:
                for data in r.iter_bytes():
                    f.write(data)
                    if progress:
                        progress.update(task_id, advance=len(data))
        return local_path

    @staticmethod
    async def download_async(
        url: str,
        local_path: str,
        num_bytes: Optional[int] = None,
        client: Optional[httpx.AsyncClient] = None,
        progress: Optional[Progress] = None,
    ) -> str:
        """Download a file asynchronously.

        Args:
            url (str): URL of the file to download.
            local_path (str): Local path to save the file (includes the file name)
            num_bytes (Optional[int], optional): Number of bytes to download. Default: None.
            client: (httpx.Client, optional): Alternative client to use (may be AsyncClient). Default: None.
            progress: (rich.progress.Progress, optional): Progress object for track download. Default: None.
        """
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, "wb") as f:
            if progress:
                filename = os.path.basename(local_path)
                task_desc = f"Download {filename if len(filename) <= 15 else filename[:12] + '...'}"
                task_id = progress.add_task(task_desc, total=num_bytes)
            async with (client or httpx.AsyncClient()).stream("GET", url) as r:
                async for data in r.aiter_bytes():
                    f.write(data)
                    if progress:
                        progress.update(task_id, advance=len(data))
        return local_path

    @staticmethod
    def download_many_sync(urls: List[str], local_paths: List[str], num_bytes: List[int], **kwargs) -> None:
        """Download many files synchronously.

        Args:
            urls (List[str]): URLs of the files to download.
            local_paths (List[str]): Local paths to save the files (includes the file names)
            num_bytes (List[int]): Number of bytes to download.
        """
        for url, local_path, byt in zip(urls, local_paths, num_bytes):
            Client.download_sync(url, local_path, byt, progress=kwargs.get("progress"))

    @staticmethod
    async def download_many_async(urls: List[str], local_paths: List[str], num_bytes: List[int], **kwargs) -> None:
        """Download many files asynchronously.

        Args:
            urls (List[str]): URLs of the files to download.
            local_paths (List[str]): Local paths to save the files (includes the file names)
            num_bytes (List[int]): Number of bytes to download.
        """
        async with httpx.AsyncClient() as client:
            tasks = []
            for url, local_path, byt in zip(urls, local_paths, num_bytes):
                task = Client.download_async(url, local_path, byt, client=client, progress=kwargs.get("progress"))
                tasks.append(asyncio.ensure_future(task))
            await asyncio.gather(*tasks)

    @staticmethod
    def request(call: str, url: str, wait_response: bool = False, **kwargs) -> ResponseType:
        """Execute a request to the Hectiq Lab API."""
        if not Client.online():
            return

        url = Client.format_url(url)
        method = request_handle(partial(getattr(Client.client, call), url=url))
        return Client.execute(method=method, wait_response=wait_response, **kwargs)

    @staticmethod
    def execute(
        method: callable,
        wait_response: bool = False,
        is_async_method: bool = False,
        with_progress: bool = False,
        **kwargs,
    ) -> ResponseType:

        def execution_handler(**kwargs):
            """Execute a request in the background or in the main thread."""
            if wait_response:
                if is_async_method:
                    return asyncio.run(method(**kwargs))
                return method(**kwargs)

            def threading_method(**kwargs):
                if is_async_method:
                    return asyncio.run(method(**kwargs))
                return method(**kwargs)

            t = threading.Thread(target=threading_method, kwargs=kwargs)
            t.start()
            return

        if not getenv("HECTIQLAB_SHOW_PROGRESS") or not with_progress:
            kwargs.pop("progress", None)
            return execution_handler(**kwargs)
        with Progress(
            TextColumn("[bold bright_blue]{task.description}", justify="left"),
            BarColumn(),
            TaskProgressColumn(text_format="[progress.iteration]{task.percentage:>3.0f}%", show_speed=True),
            FileSizeColumn(),
            TimeRemainingColumn(compact=False, elapsed_when_finished=True),
            transient=True,
        ) as progress:
            kwargs["progress"] = progress
            return execution_handler(**kwargs)

    @staticmethod
    def format_url(url: str) -> str:
        if not url.startswith("http") and url[0] == "/":
            url = API_URL + url
        return url
