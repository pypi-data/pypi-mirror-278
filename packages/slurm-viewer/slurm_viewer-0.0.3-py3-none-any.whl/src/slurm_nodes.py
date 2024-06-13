import re
import subprocess
from pathlib import Path

from src.config import Config
from src.models import Node

NODE_RE = (r'^NodeName=(?P<node_name>.+?)\s+Arch=(?P<arch>.+?)\s+CoresPerSocket=(?P<cores_per_socket>\d+)\s+'
           r'CPUAlloc=(?P<cpu_alloc>\d+)\s+CPUEfctv=(?P<cpu_efctv>\d+)\s+CPUTot=(?P<cpu_tot>\d+)\s+'
           r'CPULoad=(?P<cpuload>\d+\.\d+)\s+AvailableFeatures=(?P<available_features>.+?)\s+'
           r'ActiveFeatures=(?P<active_features>.+?)\s+Gres=(?P<gres>.+?)\s+NodeAddr=(?P<node_addr>.+?)\s+'
           r'NodeHostName=(?P<node_hostname>.+?)\s+Version=(?P<version>.+?)\s+OS=(?P<os>.+?)\s+'
           r'RealMemory=(?P<real_memory>\d+)\s+AllocMem=(?P<alloc_mem>\d+)\s+FreeMem=(?P<freemem>\d+)\s+'
           r'Sockets=(?P<sockets>\d+)\s+Boards=(?P<boards>\d+)\s+State=(?P<state>.+?)\s+'
           r'ThreadsPerCore=(?P<threads_per_core>\d+)\s+TmpDisk=(?P<tmp_disk>\d+)\s+Weight=(?P<weight>.+?)\s+'
           r'Owner=(?P<owner>.+?)\s+MCS_label=(?P<mcs_label>.+?)\s+Partitions=(?P<partitions>.+?)\s+'
           r'BootTime=(?P<boot_time>.+?)\s+SlurmdStartTime=(?P<slurmd_start_time>.+?)\s+'
           r'LastBusyTime=(?P<last_busy_time>.+?)\s+ResumeAfterTime=(?P<resume_after_time>.+?)\s+'
           r'CfgTRES=(?P<cfgtres>.+?)\s+AllocTRES=(?P<alloc_tres>.+?)\s+')


def _create_node_info(node_str: str) -> Node | None:
    m = re.search(NODE_RE, node_str)
    if not m:
        return None

    return Node(**m.groupdict())


def info(config: Config) -> list[Node]:
    try:
        arguments = f'ssh -t {config.server} ' if config.server is not None else ''
        arguments += 'scontrol --oneliner show nodes'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print(f'{Path(__file__).name}: TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print(f'{Path(__file__).name}: CalledProcessError')
        return []

    nodes = []
    for node_str in stdout.splitlines():
        node_info = _create_node_info(node_str)
        if node_info is None:
            continue

        nodes.append(node_info)

    return nodes
