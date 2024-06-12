from __future__ import annotations

import datetime
import os
import signal
from pathlib import Path
from typing import Any, List, Optional, Tuple

import grpc
import pyarrow  # type: ignore
import yaml  # type: ignore
from grpc import (
    ssl_channel_credentials,
)

from ._protobufs.bauplan_pb2 import CancelJobRequest, JobId
from ._protobufs.bauplan_pb2_grpc import CommanderServiceStub
from .bpln_proto.commander.service.v2 import service_pb2_grpc as v2

GRPC_METADATA_HEADER_API_KEY = 'x-bauplan-api-key'


def _get_log_ts_str(val: int) -> str:
    """
    Output ISO timestamp to the decisecond from a nanosecond integer timestamp input.
    """
    return str(datetime.datetime.fromtimestamp(round(val / 1000000000, 2)))[:21]


def _get_api_key() -> str:
    api_key = load_default_config_profile().get('api_key', '')
    if api_key == '':
        api_key = os.getenv('BPLN_API_KEY', '')
    if api_key == '':
        raise Exception(
            'No API key found in environment. Please update your ~/.bauplan/config.yml or set BPLN_API_KEY.'
        )
    return api_key


def get_commander_and_metadata() -> Tuple[CommanderServiceStub, List[Tuple[str, str]]]:
    conn: grpc.Channel = dial_commander()
    client: CommanderServiceStub = CommanderServiceStub(conn)
    api_key = _get_api_key()
    metadata = [(GRPC_METADATA_HEADER_API_KEY, api_key)]
    return client, metadata


def get_commander_v2_and_metadata() -> Tuple[v2.V2CommanderServiceStub, List[Tuple[str, str]]]:
    conn: grpc.Channel = dial_commander()
    client = v2.V2CommanderServiceStub(conn)
    api_key = _get_api_key()
    metadata = [(GRPC_METADATA_HEADER_API_KEY, api_key)]
    return client, metadata


def load_default_config_profile() -> dict:
    home_dir = Path.home()
    config_path = home_dir / '.bauplan' / 'config.yml'

    if not config_path.is_file():
        return {}

    with open(config_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)

    return config_data.get('profiles', {}).get('default', {})


def dial_commander() -> grpc.Channel:
    addr: str = ''
    env: Optional[str] = os.getenv('BPLN_ENV')
    if env == 'local':
        addr = 'localhost:2758'
    elif env == 'dev':
        addr = 'commander-poc.use1.adev.bauplanlabs.com:443'
    elif env == 'qa':
        addr = 'commander-poc.use1.aqa.bauplanlabs.com:443'
    elif env == 'fritzfood':
        addr = 'commander-poc.use1.afritzfood.bauplanlabs.com:443'
    else:
        addr = 'commander-poc.use1.aprod.bauplanlabs.com:443'
    creds: grpc.ChannelCredentials = ssl_channel_credentials()
    conn: grpc.Channel = grpc.secure_channel(addr, creds)
    return conn


class JobLifeCycleHandler:
    """
    Cancel jobs upon user or terminal interrupt.
    Also closes the flight client and grpc log stream connections.

    Try to cancel job, default timeout is 10 seconds.

    NOTE:
        This doesn't play nicely with threads.
        When we need that: https://stackoverflow.com/a/31667005
    """

    def __init__(
        self,
        job_id: JobId,
        client: CommanderServiceStub,
        metadata: Any,
        log_stream: grpc.Call = None,
        flight_client: pyarrow.flight.FlightClient = None,
        cancel_timeout: int = 10,  # seconds
    ) -> None:
        self.job_id = job_id
        self.client = client
        self.metadata = metadata
        self.cancel_timeout = cancel_timeout
        self.log_stream = log_stream
        self.flight_client = flight_client

    def __enter__(self) -> JobLifeCycleHandler:
        """
        Register signal handlers for SIGINT and SIGTERM
        """
        self.cancel_job_on_interrupt()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        """
        Stop signal handling.
        NOTE signal.pause() does not work on Windows; see https://stackoverflow.com/a/77129638
        """
        pass

    def add_log_stream(self, log_stream: grpc.Call) -> None:
        self.log_stream = log_stream

    def add_flight_client(self, flight_client: pyarrow.flight.FlightClient) -> None:
        self.flight_client = flight_client

    def cancel_job_on_interrupt(self) -> None:
        """
        Cancel the job when user or terminal interrupts.
        Try for 5 seconds to cancel the job.
        """

        def complete_handler(sig: Any, frame: Any) -> None:
            pass

        def timeout_handler(sig: Any, frame: Any) -> None:
            if os.getenv('BPLN_DEBUG'):
                print(f'Could not cancel job; jobId: {self.job_id.id}; message')
            # return

        def cancel_handler(sig: Any, frame: Any) -> None:
            if os.getenv('BPLN_DEBUG'):
                print(f'\nReceived interrupt signal {sig}')
                print(f'Canceling job: {self.job_id.id}')
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.signal(signal.SIGCONT, complete_handler)
            signal.alarm(self.cancel_timeout)
            try:
                if self.log_stream:
                    self.log_stream.cancel()
                if self.flight_client:
                    self.flight_client.close()
                response = self.client.CancelJob(CancelJobRequest(job_id=self.job_id), metadata=self.metadata)
            except Exception as e:
                raise e
            finally:
                # tell signal to stop waiting for a SIGALARM
                os.kill(os.getpid(), signal.SIGCONT)

            if os.getenv('BPLN_DEBUG'):
                print('Canceled job:')
                print(f'    id: {self.job_id.id}')
                print(f'    status: {response.status}')
                print(f'    message: {response.message}')

        signal.signal(signal.SIGINT, cancel_handler)
        signal.signal(signal.SIGTERM, cancel_handler)


def _build_query_from_scan(
    table: str,
    columns: Optional[list] = None,
    filters: Optional[str] = None,
    limit: Optional[int] = None,
) -> str:
    """
    Take as input the arguments of the scan function and build a SQL query
    using SQLGlot.

    Note: this is in a separate file and not next to the query function because
    I want this to be testable, but importing the query module in pytest cause grpc errors
    when we try to use fancy grpc types incompatible with Python 3.10, our lower bound.

    :meta private:

    """
    from sqlglot import select

    cols = columns or ['*']
    q = select(*cols).from_(table).where(filters)
    if limit:
        q = q.limit(limit)

    return q.sql()
