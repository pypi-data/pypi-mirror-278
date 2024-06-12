import os
import clisync
import asyncio
import logging
import shutil

from typing import Optional, List, Union

from pyhectiqlab.tag import Tag
from pyhectiqlab.block import Block
from pyhectiqlab.project import Project
from pyhectiqlab.client import Client
from pyhectiqlab.decorators import functional_alias, online_method
from pyhectiqlab.utils import batched, list_all_files_in_dir, is_running_event_loop
from pyhectiqlab.settings import getenv


class Model:
    _client: Client = Client

    @staticmethod
    @online_method
    @functional_alias("create_model")
    @clisync.include()
    def create(
        name: str,
        path: Optional[str] = None,
        version: Optional[str] = None,
        run_id: Optional[str] = None,
        project: Optional[str] = None,
        block: Optional[str] = None,
        description: Optional[str] = None,
        upload: Optional[bool] = True,
    ):
        """Create a model

        Args:
            name (str): Name of the model
            run_id (str, optional):  ID of the run
            project (str, optional): Project of the model
            path (str, optional): Path to the model directory
            description (str, optional): Description of the model
            version (str, optional): Version of the model
            block (str, optional): Block of the model
            upload (bool, optional): Upload the model files. Default: True
        """
        from pyhectiqlab.run import Run

        project = Project.get(project)
        run_id = Run.get_id(run_id)
        block = Block.get(block)

        if project is None:
            logging.error("Project not found, skipping model creation.")
            return

        if name is None:
            raise ValueError("The `name` parameter is required.")

        if block:
            if "::" not in block:
                block = Block.format_id(block, project)

        json = {
            "name": name,
            "description": description,
            "version": version,
            "block": block,
            "project": project,
            "root_run": run_id,
        }

        model = Model._client.post("/app/models", wait_response=True, json=json)
        if not model or "id" not in model:
            return

        if upload and path:
            Model.upload(id=model["id"], path=path)

        Model.attach(name=name, version=version, run_id=run_id, project=project, wait_response=True)
        return model

    @staticmethod
    @online_method
    @functional_alias("upload_model")
    @clisync.include()
    def upload(id: str, path: str):
        """Upload local files to a model hosted in the Lab.

        Args:
            id (str): ID of the model.
            path (str): Path to the model directory.
        """
        all_files = list_all_files_in_dir(path)
        batch_size = 50
        Model._id = model_id = id
        for batch in batched(all_files, batch_size):
            # Create many files
            batch_body = [{"name": os.path.relpath(f, start=path), "num_bytes": os.path.getsize(f)} for f in batch]
            files = Model._client.post(
                f"/app/models/{model_id}/files", wait_response=True, json={"files": batch_body}
            )["results"]

            # For each file in batch, get the policy in files (use name for finding the file)
            sorted_files = []
            for el in batch:
                file = [f.get("upload_policy") for f in files if f["name"] == os.path.relpath(el, start=path)][0]
                sorted_files.append(file)

            # Upload model files
            asyncio.run(Model._client.upload_many(paths=batch, policies=sorted_files))

    @staticmethod
    @online_method
    @functional_alias("retrieve_model")
    @clisync.include()
    def retrieve(
        name: str,
        version: str,
        project: Optional[str] = None,
        fields: Optional[List[str]] = [],
    ):
        """Retrieve a model

        Args:
            name (str): Name of the model
            version (str): Version of the model
            project (str, optional): Project of the model. If None, the project of the current run is used. Default: None.
            fields (dict, optional): Fields to retrieve
            wait_response (bool, optional): Wait for the response from the server
        """
        project = Project.get(project)
        if project is None:
            return

        return Model._client.get(
            "/app/models/retrieve",
            params={
                "name": name,
                "project": project,
                "version": version,
                "fields": fields,
            },
            wait_response=True,
        )

    @staticmethod
    @online_method
    @functional_alias("list_models")
    @clisync.include(wait_response=True)
    def list(
        project: Optional[str] = None,
        search: Optional[str] = None,
        author: Optional[str] = None,
        block: Optional[str] = None,
        blocks: Optional[List[str]] = None,
        keep_latest_version: bool = False,
        fields: Optional[List[str]] = [],
        page: Optional[int] = 1,
        limit: Optional[int] = 100,
        order_by: Optional[str] = "created_at",
        order_direction: Optional[str] = "desc",
        wait_response: bool = False,
    ):
        """List the models

        Args:
            project (str): Project of the model
            block (str, optional): Block of the model
            search (str, optional): Search string
            author (str, optional): Author of the model
            blocks (List[str], optional): Blocks of the model
            keep_latest_version (bool, optional): If True, group by the latest version of model name and return only the latest version of each model name
            fields (List[str], optional): Fields to retrieve
            page (int, optional): Page number
            limit (int, optional): Limit of the models
            order_by (str, optional): Order by
            order_direction (str, optional): Order direction
            wait_response (bool, optional): Wait for the response from the server
        """

        if block is not None:
            if "::" not in block:
                from pyhectiqlab.block import Block

                block = Block.format_id(block, project)

        params = {
            "project": Project.get(project),
            "block": block,
            "search": search,
            "author": author,
            "blocks": blocks,
            "keep_latest_version": keep_latest_version or True,
            "fields": fields,
            "page": page or 1,
            "limit": limit or 100,
            "order_by": order_by,
            "order_direction": order_direction,
        }
        return Model._client.get("/app/models", params=params, wait_response=wait_response)

    @staticmethod
    @online_method
    @functional_alias("update_model")
    @clisync.include(wait_response=True)
    def update(
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        block: Optional[str] = None,
        wait_response: bool = False,
    ):
        """Update a model

        Args:
            id (str): ID of the model
            name (str, optional): Name of the model
            description (str, optional): Description of the model
            version (str, optional): Version of the model
            block (str, optional): Block of the model
            wait_response (bool, optional): Wait for the response from the server
        """
        if not id:
            return
        return Model._client.put(
            f"/app/models/{id}",
            json={"name": name, "description": description, "version": version, "block": block},
            wait_response=wait_response,
        )

    @staticmethod
    @online_method
    @functional_alias("delete_model")
    @clisync.include(wait_response=True)
    def delete(
        id: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        project: Optional[str] = None,
        wait_response: bool = False,
    ):
        """Delete a model

        Args:
            id (str): ID of the model
            name (str, optional): Name of the model
            version (str, optional): Version of the model
            project (str, optional): Project of the model
            wait_response (bool, optional): Wait for the response from the server
        """
        project = Project.get(project)
        assert id or (name and version and project), "Either `id` or `name`, `version` and `project` must be provided."
        if not id:
            model = Model.retrieve(name=name, project=project, version=version, fields=["id"])
            if not model:
                return
            id = model["id"]
        return Model._client.delete(f"/app/models/{id}", wait_response=wait_response)

    @staticmethod
    @online_method
    @functional_alias("upload_model")
    @clisync.include()
    def upload(id: str, path: str):
        """Upload local files to a model hosted in the Lab.

        Args:
            id (str): ID of the model.
            path (str): Path to the model directory.
        """

        def upload_files(paths, policies):
            if is_running_event_loop():
                Model._client.upload_many_sync(paths=paths, policies=policies)
            else:
                asyncio.run(Model._client.upload_many_async(paths=batch, policies=sorted_files))

        all_files = list_all_files_in_dir(path)
        batch_size = 50
        Model._id = model_id = id
        start = path if os.path.isdir(path) else os.path.dirname(path)
        for batch in batched(all_files, batch_size):
            # Create many files
            batch_body = [{"name": os.path.relpath(f, start=start), "num_bytes": os.path.getsize(f)} for f in batch]
            files = Model._client.post(
                f"/app/models/{model_id}/files", wait_response=True, json={"files": batch_body}
            )["results"]

            # For each file in batch, get the policy in files (use name for finding the file)
            sorted_files = []
            for el in batch:
                file = [f.get("upload_policy") for f in files if f["name"] == os.path.relpath(el, start=start)][0]
                sorted_files.append(file)

            # Upload model files
            upload_files(batch, sorted_files)

    @staticmethod
    @functional_alias("download_model")
    @clisync.include(wait_response=True)
    def download(
        name: str,
        version: str,
        project: Optional[str] = None,
        path: Optional[str] = None,
        overwrite: bool = False,
        wait_response: bool = True,
    ):
        """Download a model

        Args:
            name (str): Name of the model
            project (str): Project of the model
            version (str): Version of the model
            path (str, optional): Path to download the model
            overwrite (bool, optional): Overwrite the files if they already exist
            wait_response (bool, optional): Wait for the response from the server
        """
        if not Model.exists(name=name, version=version, project=project):
            logging.error(f"Model {name}-{version} does not exist.")
            return
        path = path or getenv("HECTIQLAB_MODELS_DOWNLOAD")
        path = os.path.join(path, f"{name}-{version}")
        if os.path.exists(path):
            if not overwrite:
                logging.warning(f"Directory {path} already exists. Set `overwrite=True` to overwrite the files.")
                return path

            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)
        from pyhectiqlab import Run

        project = Project.get(project)

        async def composition():
            model = Model.retrieve(name=name, project=project, version=version, fields=["id"])
            if not model:
                return
            model_id = model["id"]

            if Run.id is not None:
                Model._client.post(f"/app/models/{model_id}/attach-to-run/{Run.id}", wait_response=False)

            num_results = 0
            total_results = 1
            page = 1
            while not num_results == total_results:
                files = Model._client.get(
                    f"/app/models/{model_id}/files/",
                    params={"page": page, "limit": 50, "fields": ["download_url", "name", "num_bytes"]},
                    wait_response=True,
                )
                total_results = files["total_results"]

                await Model._client.download_many(
                    urls=[file["download_url"] for file in files["results"]],
                    local_paths=[os.path.join(path, file["name"]) for file in files["results"]],
                    num_bytes=[file["num_bytes"] for file in files["results"]],
                )
                num_results += len(files["results"])
                page += 1

            Model._client.post(f"/app/models/{model_id}/on-download-completed", wait_response=False)

        res = Model._client.execute(composition, wait_response=wait_response, is_async_method=True)
        if isinstance(res, asyncio.Task):
            return res
        return path

    @staticmethod
    @online_method
    def attach(
        name: str,
        version: str,
        run_id: Optional[str] = None,
        project: Optional[str] = None,
        wait_response: bool = True,
    ):
        """Attach a model to a run

        Args:
            run_id (str): ID of the run.
            name (str): Name of the model.
            version (str): Version of the model.
            project (str, optional): Project of the model. If None, the project of the current run is used. Default: None.
            wait_response (bool, optional): Wait for the response from the server. Default: False.
        """
        from pyhectiqlab.run import Run

        run_id = Run.get_id(run_id)
        if run_id is None:
            return
        project = Project.get(project)
        model = Model.retrieve(name=name, project=project, version=version, fields=["id"])
        if not model:
            return
        model_id = model["id"]
        return Model._client.post(f"/app/models/{model_id}/attach-to-run/{run_id}", wait_response=wait_response)

    @staticmethod
    @online_method
    def detach(
        name: str,
        version: str,
        run_id: str,
        project: Optional[str] = None,
        wait_response: bool = False,
    ):
        """Detach a model from a run

        Args:
            name (str): Name of the model.
            version (str): Version of the model.
            run_id (int): ID of the run.
            project (str, optional): Project of the model. If None, the project of the current run is used. Default: None.
            wait_response (bool, optional): Wait for the response from the server. Default: False.
        """
        project = Project.get(project)
        model = Model.retrieve(name=name, project=project, version=version, fields=["id"])
        if not model:
            return
        model_id = model["id"]
        return Model._client.post(f"/app/models/{model_id}/detach-from-run/{run_id}", wait_response=wait_response)

    @staticmethod
    @online_method
    @functional_alias("add_tags_to_model")
    def add_tags(
        tags: Union[str, List[str]],
        name: str,
        version: str,
        project: Optional[str] = None,
    ):
        """Add tags to a model

        Args:
            tags (Union[str, List[str]]): Tags to add.
            name (str): Name of the model.
            version (str): Version of the model.
            project (str): Project of the model. If None, the project of the current run is used. Default: None.
        """
        project = Project.get(project)
        model = Model.retrieve(name=name, project=project, version=version, fields=["id"])
        if not model:
            return
        model_id = model["id"]
        return Tag.attach_to_model(tags=tags, model_id=model_id, project=project)

    @staticmethod
    @online_method
    @functional_alias("detach_tag_from_model")
    def detach_tag(
        tag: str,
        name: str,
        version: str,
        project: Optional[str] = None,
    ):
        """Remove a tag from the model.

        Args:
            title (str): The new title of the run.
            name (str): Name of the model.
            version (str): Version of the model.
            project (str): Project of the model. If None, the project of the current run is used. Default: None.
        """
        project = Project.get(project)
        model = Model.retrieve(name=name, version=version, project=project, fields=["id"])
        if not model:
            return
        model_id = model["id"]
        Tag.detach_from_model(tag=tag, model_id=model_id, project=project)
