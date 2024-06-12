import clisync
import logging
from typing import Optional, List

from pyhectiqlab.const import DISABLE_BLOCK_CREATION
from pyhectiqlab.project import Project
from pyhectiqlab.client import Client
from pyhectiqlab.decorators import functional_alias, online_method


class Block:

    _block: Optional[str] = None

    @staticmethod
    @functional_alias("get_block")
    def get(block: Optional[str] = None):
        return block or Block._block

    @staticmethod
    @functional_alias("set_block")
    def set(block: str):
        Block._block = block

    @staticmethod
    def format_id(block: Optional[int] = None, project: Optional[str] = None):
        block = block or Block.get()
        project = project or Project.get()
        if not block or not project:
            return
        return f"{block}::{project.replace('/', '::')}"

    @staticmethod
    @online_method
    @functional_alias("create_block")
    @clisync.include(wait_response=True)
    def create(
        title: str, 
        status: Optional[str] = None, 
        project: Optional[str] = None,
        wait_response: Optional[bool] = False
    ):
        """Create a block.

        Args:
            title (str): Block title.
            status (str, optional): Block status. Default: None.
            project (str, optional): Project name. If None, the current project is used. Default: None.
        """
        if DISABLE_BLOCK_CREATION:
            logging.error("Block creation is disabled. Continuing anyway...")
            return
        project = project or Project.get()
        if not project:
            return None

        body = {"title": title, "status": status, "project": project}
        block = Client.post("/app/blocks", json=body, wait_response=wait_response)
        return block

    @staticmethod
    @online_method
    @functional_alias("update_block")
    @clisync.include(wait_response=True)
    def update(
        block: str, 
        title: Optional[str] = None, 
        status: Optional[str] = None, 
        wait_response: Optional[bool] = False
    ):
        """Update a block.

        Args:
            block (str): Block ID.
            title (str, optional): Block title. Default: None.
            status (str, optional): Block status. Default: None.
        """
        body = {"title": title, "status": status}
        # Remove None
        body = {k: v for k, v in body.items() if v is not None}
        if len(body) == 0:
            return
        block = Client.put(f"/app/blocks/{block}", json=body, wait_response=wait_response)
        return block

    @staticmethod
    @online_method
    @functional_alias("list_blocks")
    @clisync.include()
    def list(
        project: Optional[str] = None,
        search: Optional[str] = None,
        fields: Optional[List[str]] = None,
        page: Optional[int] = 1,
        limit: Optional[int] = 50,
        order_by: Optional[str] = "created_at",
        order_direction: Optional[str] = "desc",
    ):
        """List blocks.

        Args:
            project (str, optional): Project name. If None, the current project is used. Default: None.
            search (str, optional): Search string. Default: None.
        """
        project = project or Project.get()
        if not project:
            return None
        params = {
            "project": project,
            "search": search,
            "fields": fields,
            "page": page,
            "limit": limit,
            "order_by": order_by,
            "order_direction": order_direction,
        }
        blocks = Client.get("/app/blocks", params=params, wait_response=True)
        return blocks
