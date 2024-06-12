import os
from io import StringIO
from typing import Any, Callable, List, Optional

import grpc
import yaml  # type: ignore

from ._common import get_commander_and_metadata, get_commander_v2_and_metadata
from ._protobufs.bauplan_pb2 import (
    JobId,
    RunnerInfo,
)
from ._protobufs.commander_pb2 import RunnerEvent
from .bpln_proto.commander.service.v2.service_pb2 import (
    ApplyImportPlanRequest,
    ApplyImportPlanResponse,
    CreateImportPlanRequest,
    CreateImportPlanResponse,
)

JOB_STATUS_FAILED = 'FAILED'
JOB_STATUS_SUCCESS = 'SUCCESS'
JOB_STATUS_CANCELLED = 'CANCELLED'


def _validate_plan_yaml(plan_yaml: str) -> None:
    if not isinstance(plan_yaml, str):
        raise ValueError('invalid plan YAML; plan YAML string is required')
    if not plan_yaml or plan_yaml.strip() == '':
        raise ValueError('invalid plan YAML; plan YAML string is required')

    try:
        yaml.safe_load(StringIO(plan_yaml))
    except yaml.YAMLError as exception:
        raise exception


class ApplyPlanState:
    """
    Hold state for a plan import request.
    """

    job_id: str
    error: Optional[str] = None
    job_status: Optional[str] = None
    runner_events: Optional[List[RunnerEvent]]

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id
        self.runner_events = []


def _handle_apply_import_log(log: RunnerInfo, state: ApplyPlanState) -> None:
    if log.runner_event.apply_plan_done.error_message or log.runner_event.apply_plan_done.success:
        if log.runner_event.apply_plan_done.error_message:
            state.error = log.runner_event.apply_plan_done.error_message
            state.job_status = JOB_STATUS_FAILED
            if os.getenv('BPLN_DEBUG'):
                print(f'Apply plan failed, error is: {state.error}')
            return True
        if log.runner_event.apply_plan_done.success:
            state.job_status = JOB_STATUS_SUCCESS
            if os.getenv('BPLN_DEBUG'):
                print('Apply plan successful')
            return True
    return False


def _timeout_factory_apply(seconds: int) -> Callable:
    def _timeout(sig: Any, frame: Any) -> None:
        raise TimeoutError(f'Plan import execution took longer than {seconds} seconds')

    return _timeout


def apply(plan_yaml: str, branch: str, table: str) -> ApplyPlanState:
    """
    Apply a Bauplan table import plan for a given branch and table.
    This is the equivalent of running through the CLI the ``bauplan import apply`` command.

    .. code-block:: python

        from bauplan.import_ import apply, plan
        # get the YAML representing the table import plan
        s3_path = 's3://path/to/my/files/*.parquet'
        plan_state = plan(s3_path)
        if plan_state.error:
            plan_error_action(...)

        # apply the table import plan to create/replace a table on this branch
        apply_state = apply(
            plan_yaml=plan_state.plan_yaml,
            branch='myname.mybranch',
            table='newtablename'
        )
        if apply_state.error:
            apply_error_action(...)

    :param plan_yaml: string contents of a plan YAML file
    :param branch: name of the branch on which to apply the plan
    :param table: name of the table on which to apply the plan
    """
    _validate_plan_yaml(plan_yaml)
    if not isinstance(table, str) and table.strip():
        raise ValueError("table is required, e.g. 'table_name'")
    if not isinstance(branch, str) and branch.strip():
        raise ValueError("branch is required, e.g. 'myname.mybranch'")

    client_v1, metadata_v1 = get_commander_and_metadata()
    client_v2, metadata_v2 = get_commander_v2_and_metadata()

    if os.getenv('BPLN_DEBUG'):
        print('Apply import plan', 'plan_yaml\n', plan_yaml)
        print('Apply import plan', 'branch', branch)
        print('Apply import plan', 'table', table)
    response: ApplyImportPlanResponse = client_v2.ApplyImportPlan(
        ApplyImportPlanRequest(plan_yaml=plan_yaml, branch=branch, table=table), metadata=metadata_v2
    )
    job_id = JobId(id=response.job_id)
    if os.getenv('BPLN_DEBUG'):
        print('Apply import plan job_id', response.job_id)
    log_stream: grpc.Call = client_v1.SubscribeLogs(job_id, metadata=metadata_v1)
    state = ApplyPlanState(job_id=job_id.id)
    for log in log_stream:
        if _handle_apply_import_log(log, state):
            break
    return state


class PlanImportState:
    """
    Hold state for a plan import request.
    """

    job_id: str
    plan_yaml: Optional[str] = None
    error: Optional[str] = None
    job_status: Optional[str] = None
    runner_events: Optional[List[RunnerEvent]]

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id
        self.runner_events = []


def _handle_plan_import_log(log: RunnerInfo, state: PlanImportState) -> None:
    if (
        log.runner_event.import_plan_created.error_message
        or log.runner_event.import_plan_created.plan_as_yaml
    ):
        if log.runner_event.import_plan_created.error_message:
            state.error = log.runner_event.import_plan_created.error_message
            state.job_status = JOB_STATUS_FAILED
            if os.getenv('BPLN_DEBUG'):
                print(f'Plan import failed, error is: {log.runner_event.import_plan_created.error_message}')
            return True
        if log.runner_event.import_plan_created.success:
            state.job_status = JOB_STATUS_SUCCESS
            state.plan_yaml = log.runner_event.import_plan_created.plan_as_yaml
            if os.getenv('BPLN_DEBUG'):
                print('Create import plan success')
            return True
    return False


def _timeout_factory_plan(seconds: int) -> Callable:
    def _timeout(sig: Any, frame: Any) -> None:
        raise TimeoutError(f'Plan import execution took longer than {seconds} seconds')

    return _timeout


def plan(search_string: str) -> PlanImportState:
    """
    Create a table import plan from an S3 location.
    This is the equivalent of running through the CLI the ``bauplan import plan`` command.

    .. code-block:: python

        from bauplan.import_ import plan
        s3_path = 's3://path/to/my/files/*.parquet'
        plan_state = plan(s3_path)
        if plan_state.error:
            plan_error_action(...)
        success_action(plan_state.plan_yaml)

    :param search_string: The filepath of the plan to import.
    """
    if not isinstance(search_string, str):
        raise ValueError(
            "invalid search string; search string is required, e.g., 's3://bucket-name/*.parquet'"
        )
    if not search_string or search_string.strip() == '':
        raise ValueError("search string is required, e.g., 's3://bucket-name/*.parquet'")
    search_string = search_string.strip()
    if not search_string.startswith('s3://'):
        raise ValueError('search string must be an S3 path')
    if not isinstance(search_string, str):
        raise ValueError("invalid output file; output file is required, e.g., 'my_import_plan.yaml'")

    client_v1, metadata_v1 = get_commander_and_metadata()
    client_v2, metadata_v2 = get_commander_v2_and_metadata()

    if os.getenv('BPLN_DEBUG'):
        print('Create import plan', 'search_string', search_string)
    response: CreateImportPlanResponse = client_v2.CreateImportPlan(
        CreateImportPlanRequest(search_string=search_string), metadata=metadata_v2
    )
    job_id = JobId(id=response.job_id)
    if os.getenv('BPLN_DEBUG'):
        print('Create import plan job_id', response.job_id)

    log_stream: grpc.Call = client_v1.SubscribeLogs(job_id, metadata=metadata_v1)
    state = PlanImportState(job_id=job_id.id)
    for log in log_stream:
        if _handle_plan_import_log(log, state):
            break
    return state
