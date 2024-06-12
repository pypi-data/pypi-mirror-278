import os
import clisync
from typing import Optional, List
from pyhectiqlab.project import Project
from pyhectiqlab.client import Client
from pyhectiqlab.decorators import online_method, functional_alias


class Artifact:

    @staticmethod
    @online_method
    @clisync.include(wait_response=True)
    def create(
        local_path: str,
        run_id: str,
        project: str,
        name: Optional[str] = None,
        step: Optional[int] = None,
        group: Optional[str] = None,
        wait_response: bool = False,
    ):
        """
        Upload an artifact to a run.

        Args:
            local_path (str): Path to the file to upload.
            run_id (str): ID of the run.
            project (str): ID of the project.
            name (str, optional): Name of the artifact. If None, the basename of the file is used. Default: None.
            step (int, optional): Step number. If None, the artifact is not considered as a step artifact. Default: None.
            group (str, optional): Group name. If None, the group is determined from the local_path. Default: None.
            wait_response (bool): Set to true to upload sync. If False, the upload is made in background. Default: False.
        """
        name = name or os.path.basename(local_path)
        group = group or os.path.basename(local_path)
        num_bytes = os.path.getsize(local_path)
        extension = os.path.splitext(local_path)[1]

        json = {
            "name": name,
            "num_bytes": num_bytes,
            "group": group,
            "step": step,
            "project": project,
            "run": run_id,
            "extension": extension,
        }

        async def composition():
            artifact = Client.post("/app/artifacts", wait_response=True, json=json)
            if not artifact:
                return
            return await Client.upload(local_path=local_path, policy=artifact.get("upload_policy"))

        return Client.execute(composition, wait_response=wait_response, is_async_method=True)

    @staticmethod
    @online_method
    @functional_alias("delete_artifact")
    @clisync.include(wait_response=True)
    def delete(
        id: str,
        wait_response: bool = False,
    ):
        """
        Delete an artifact.

        Args:
            id (str): ID of the artifact.
            wait_response (bool): Set to true to delete sync. If False, the deletion is made in background. Default: False.
        """
        return Client.delete(f"/app/artifacts/{id}", wait_response=wait_response)

    @staticmethod
    @online_method
    @functional_alias("get_artifact")
    @clisync.include()
    def retrieve(id: str, fields: Optional[List[str]] = None):
        """
        Retrieve an artifact.

        Args:
            id (str): ID of the artifact.
        """
        return Client.get(f"/app/artifacts/{id}", wait_response=True, params={"fields": fields})

    @staticmethod
    @online_method
    @functional_alias("download_artifact")
    @clisync.include(wait_response=True)
    def download(
        id: str,
        path: str = "./",
        wait_response: bool = True,
    ):
        """
        Download an artifact from a run.

        Args:
            name (str): Name of the artifact.
            path (str): Path to save the file. Default: './'.
            block: Name of the block. If None, the block is determined from the context. Default: None.
        """
        path = path or "./"

        async def composition():
            fields = ["download_url", "num_bytes", "name"]
            artifact = Client.get(f"/app/artifacts/{id}", wait_response=True, params={"fields": fields})
            if not artifact:
                return
            os.makedirs(path, exist_ok=True)
            await Client.download(
                url=artifact["download_url"],
                local_path=os.path.join(path, artifact["name"]),
                num_bytes=artifact["num_bytes"],
            )

        Client.execute(composition, wait_response=wait_response, is_async_method=True)
        pass

    @staticmethod
    @online_method
    @functional_alias("list_artifacts")
    @clisync.include()
    def list(
        run_id: str,
        project: Optional[str] = None,
        fields: Optional[List[str]] = None,
        group_by_step: Optional[bool] = True,
        page: Optional[int] = 1,
        limit: Optional[int] = 50,
        order_by: Optional[str] = "name",
        order_direction: Optional[str] = "asc",
    ):
        """
        List the artifacts of a run.

        Args:
            run_id (str): ID of the run.
            project (str): ID of the project.
            fields (List[str], optional): List of fields to retrieve. Default: None.
            group_by_step (bool, optional): Set to True to group the artifacts by step. Default: True.
            page (int, optional): Page number. Default: 1.
            limit (int, optional): Number of artifacts to retrieve per page. Default: 50.
            order_by (str, optional): Field to order by. Default: "name".
            order_direction (str, optional): Order direction. Default: "asc".
        """
        project = Project.get(project)
        if not project:
            return

        return Client.get(
            "/app/artifacts",
            wait_response=True,
            params={
                "run": run_id,
                "project": project,
                "fields": fields,
                "keep_latest_step": True if group_by_step else False,
                "page": page,
                "limit": limit,
                "order_by": order_by,
                "order_direction": order_direction,
            },
        )
