import re
import subprocess
from pathlib import Path

from src.config import Config
from src.models import Queue

QUEUE_RE = (r'^(?P<account>[\w\d-]+)[|](?P<tres_per_node>[\w\:]+)[|](?P<min_cpu>\d+)[|](?P<min_tmp_disk>\d+)[|]'
            r'(?P<end_time>[\w\d:-]+)[|](?P<features>[^|]+)[|](?P<group>[^|]+)[|](?P<over_subscribe>[^|]+)[|]'
            r'(?P<job_id>\d+)[|](?P<name>[^|]+)[|](?P<comment>[^|]+)[|](?P<time_limit>[^|]+)[|]'
            r'(?P<min_memory>[^|]+)[|](?P<req_nodes>[^|]*)[|](?P<command>[^|]+)[|](?P<priority>[^|]+)[|]'
            r'(?P<qos>[^|]+)[|](?P<reason>[^|]+)[|](?P<st>[^|]+)[|](?P<user>[^|]+)[|](?P<reservation>[^|]+)[|]'
            r'(?P<wc_key>[^|]+)[|](?P<excluded_nodes>[^|]*)[|](?P<nice>[^|]+)[|](?P<s_c_t>[^|]+)[|]'
            r'(?P<job_id_2>[^|]+)[|](?P<exec_host>[^|]+)[|](?P<cpus>[^|]+)[|](?P<nodes>[^|]+)[|]'
            r'(?P<dependency>[^|]+)[|](?P<array_job_id>[^|]+)[|](?P<group_2>[^|]+)[|](?P<sockets_per_node>[^|]+)[|]'
            r'(?P<cores_per_socket>[^|]+)[|](?P<threads_per_core>[^|]+)[|](?P<array_task_id>[^|]+)[|]'
            r'(?P<time_left>[^|]+)[|](?P<time>[^|]+)[|](?P<nodelist>[^|]*)[|](?P<contiguous>[^|]+)[|]'
            r'(?P<partition>[^|]+)[|](?P<priority_2>[^|]+)[|](?P<nodelist_reason>[^|]+)[|](?P<start_time>[^|]+)[|]'
            r'(?P<state>[^|]+)[|](?P<uid>[^|]+)[|](?P<submit_time>[^|]+)[|](?P<licenses>[^|]+)[|](?P<core_spec>[^|]+)[|]'
            r'(?P<scheduled_nodes>[^|]+)[|](?P<work_dir>[^|]+)$')


def _create_output(lines: list[str]) -> list[Queue]:
    def _create_node_queue(data: str) -> Queue | None:
        m = re.search(QUEUE_RE, data)
        if not m:
            return None

        return Queue(**m.groupdict())

    result = []
    for x in lines[1:]:
        val = _create_node_queue(x.rstrip())
        if val is None:
            continue

        result.append(val)

    return result


def info(config: Config) -> list[Queue]:
    try:
        arguments = f'ssh -t {config.server} ' if config.server is not None else ''
        arguments += f'squeue --partition {",".join(config.partitions)} --format=%all'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print(f'{Path(__file__).name}: TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print(f'{Path(__file__).name}: CalledProcessError')
        return []

    return _create_output(stdout.splitlines())
