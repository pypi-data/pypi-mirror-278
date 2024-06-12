from typing import Any, List

# from grpc._channel import _InactiveRpcError, _RPCState
from ._common import get_commander_and_metadata, get_commander_v2_and_metadata
from ._protobufs.bauplan_pb2 import (
    Branch,
    CreateBranchRequest,
    CreateBranchResponse,
    DeleteBranchRequest,
    DeleteBranchResponse,
    GetBranchesRequest,
    GetBranchesResponseData,
    GetBranchRequest,
    GetBranchResponse,
    GetTableRequest,
    GetTableResponse,
    MergeBranchRequest,
    MergeBranchResponse,
    TableField,
)
from .bpln_proto.commander.service.v2.service_pb2 import DropTableRequest, DropTableResponse


def get_branches() -> List[Branch]:
    """
    Get the available data branches in the Bauplan catalog.

    Upon failure, raises grpc._channel._InactiveRpcError

    .. code-block:: python

        from bauplan.catalog import get_branches
        branch_names = [branch.name for branch in get_branches()]

    :return: a list of branches, each having "name", "hash", "user", "data_name"
    """
    client, metadata = get_commander_and_metadata()

    response: GetBranchesResponseData = client.GetBranches(GetBranchesRequest(), metadata=metadata)
    return response.data.branches


def get_branch(branch_name: str) -> List[Any]:
    """
    Get the tables and views in the target branch.

    Upon failure, raises grpc._channel._InactiveRpcError

    .. code-block:: python

        from bauplan.catalog import get_branch
        # retrieve only the tables as tuples of (name, kind)
        tables = [(b.name, b.kind) for b in get_branch('main') if b.kind == 'TABLE']

    :param branch_name: The name of the branch to retrieve.
    :return: A list of tables, each having "name", "kind" (e.g. TABLE)
    """
    client, metadata = get_commander_and_metadata()

    response: GetBranchResponse = client.GetBranch(
        GetBranchRequest(branch_name=branch_name), metadata=metadata
    )
    return response.data.entries


def merge_branch(onto_branch: str, from_ref: str) -> bool:
    """
    Merge one branch into another.

    Upon failure, raises grpc._channel._InactiveRpcError

    .. code-block:: python

        from bauplan.catalog import merge_branch
        merge_branch(onto_branch='myzone.somebranch',from_ref='myzone.oldbranch')

    :param onto_branch: The name of the merge target
    :param from_ref: The name of the merge source; either a branch like "main" or ref like "main@[sha]"
    :return: a boolean for whether the merge worked
    """
    client, metadata = get_commander_and_metadata()

    _: MergeBranchResponse = client.MergeBranch(
        MergeBranchRequest(onto_branch=onto_branch, from_ref=from_ref),
        metadata=metadata,
    )
    return True


def create_branch(branch_name: str, ref: str) -> bool:
    """
    Create a new branch at a given ref.

    Upon failure, raises grpc._channel._InactiveRpcError

    .. code-block:: python

        from bauplan.catalog import create_branch
        create_branch(branch_name='myzone.newbranch', ref='main')

    :param branch_name: The name of the new branch
    :param ref: The name of the base branch; either a branch like "main" or ref like "main@[sha]"
    :return: a boolean for whether the new branch was created
    """
    client, metadata = get_commander_and_metadata()

    _: CreateBranchResponse = client.CreateBranch(
        CreateBranchRequest(branch_name=branch_name, ref=ref),
        metadata=metadata,
    )
    return True


def delete_branch(branch_name: str) -> bool:
    """
    Delete a branch.

    Upon failure, raises grpc._channel._InactiveRpcError

    .. code-block:: python

        from bauplan.catalog import delete_branch
        delete_branch(branch_name='mybranch')

    :param branch_name: The name of the branch to delete.
    :return: A boolean for if the branch was deleted
    """
    client, metadata = get_commander_and_metadata()

    _: DeleteBranchResponse = client.DeleteBranch(
        DeleteBranchRequest(branch_name=branch_name), metadata=metadata
    )
    return True


def get_table(branch_name: str, table_name: str) -> list[TableField]:
    """
    Get the table metadata for a table in the target branch.

    Upon failure, raises grpc._channel._InactiveRpcError

    .. code-block:: python

        from bauplan.catalog import get_table
        # get the fields and metadata for the taxi_zones table in the main branch
        cnt_f = get_table(branch_name='main', table_name='taxi_zones')
        # loop through the fields and print their name, required, and type
        for c in cnt_f:
            print(c.name, c.required, c.type)

    :param branch_name: The name of the branch to get the table from.
    :param table_name: The name of the table to retrieve.
    :return: a list of fields, each having "name", "required", "type"
    """
    client, metadata = get_commander_and_metadata()

    response: GetTableResponse = client.GetTable(
        GetTableRequest(branch_name=branch_name, table_name=table_name),
        metadata=metadata,
    )
    return response.data.entry.fields


def drop_table(table_name: str, branch_name: str) -> bool:
    """
    Drop a table.

    Upon failure, raises grpc._channel._InactiveRpcError

    .. code-block:: python

        from bauplan.catalog import drop_table
        drop_table(table_name='mytable', branch_name='mybranch')

    :param table_name: The name of the table to delete
    :param branch_name: The name of the branch on which the table is stored
    :return: A boolean for if the table was deleted
    """
    client, metadata = get_commander_v2_and_metadata()

    _: DropTableResponse = client.DropTable(
        DropTableRequest(table_name=table_name, branch_name=branch_name), metadata=metadata
    )
    return True
