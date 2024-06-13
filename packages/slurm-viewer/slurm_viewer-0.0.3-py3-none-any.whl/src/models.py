from __future__ import annotations

import datetime
import math
import re
from enum import Enum
from typing import Any

import dateutil.parser
from pydantic import BaseModel, ConfigDict, field_validator

from src.common_types import MemoryUsed, CPU_TIME_RE, PostFixUnit

CFGTRESS_RE = r'^cpu=(?P<cpu>\d+),mem=(?P<mem>\d+\w),billing=(?P<billing>\d+),gres/gpu=(?P<gpu>\d+)$'
ALLOCTRESS_RE = (r'^cpu=(?P<cpu>\d+),mem=(?P<mem>\d+\w)(?:,gres/gpu=(?P<gpu_alloc>\d+))'
                 r'(?:,gres/gpu:(?P<gpu_type>\S+)=(?P<gpu_total>\d+))?$')

TRES_USAGE_IN_AVE_RE = (r'^cpu=(?P<cpu>(?:\d+-)?\d+:\d+:\d+),energy=(?P<energy>\d+),fs/disk=(?P<disk>\d+),'
                        r'gres/gpumem=(?P<gpu_mem>\w+),gres/gpuutil=(?P<gpu_util>\d+),mem=(?P<mem>\d+K),'
                        r'pages=(?P<pages>\d+),vmem=(?P<vmem>\d+K)$')


class State(Enum):
    IDLE = 'IDLE'
    MIXED = 'MIXED'
    ALLOCATED = 'ALLOCATED'
    DRAIN = 'DRAIN'
    MIXED_DRAIN = 'MIXED+DRAIN'
    MIXED_COMPLETING = 'MIXED+COMPLETING'
    IDLE_DRAIN = 'IDLE+DRAIN'


class JobStateCodes(Enum):
    BOOT_FAIL = 'BOOT_FAIL'
    CANCELLED = 'CANCELLED'
    COMPLETED = 'COMPLETED'
    DEADLINE = 'DEADLINE'
    FAILED = 'FAILED'
    NODE_FAIL = 'NODE_FAIL'
    OUT_OF_MEMORY = 'OUT_OF_MEMORY'
    PENDING = 'PENDING'
    PREEMPTED = 'PREEMPTED'
    RUNNING = 'RUNNING'
    REQUEUED = 'REQUEUED'
    RESIZING = 'RESIZING'
    REVOKED = 'REVOKED'
    SUSPENDED = 'SUSPENDED'
    TIMEOUT = 'TIMEOUT'


class ExitCodeSignal:  # pylint: disable=too-few-public-methods
    def __init__(self, value: str) -> None:
        self.code: int | None
        self.signal: int | None

        data = value.split(':')
        if len(data) == 2:
            self.code = int(data[0])
            self.signal = int(data[1])
            return

        if len(data) == 1:
            self.code = int(data[0])
            self.signal = None
            return

        self.code = None
        self.signal = None

    def __repr__(self) -> str:
        return f'{self.code}'


# noinspection PyNestedDecorators
class Queue(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    account: str
    tres_per_node: str
    min_cpu: int
    min_tmp_disk: int
    end_time: datetime.datetime
    features: str
    group: str
    over_subscribe: str
    job_id: int
    name: str
    comment: str
    time_limit: datetime.timedelta
    min_memory: MemoryUsed
    req_nodes: str
    command: str
    priority: float
    qos: str
    reason: str
    st: str
    user: str
    reservation: str
    wc_key: str
    excluded_nodes: str
    nice: int
    s_c_t: str
    exec_host: str
    cpus: int
    nodes: int
    dependency: str
    array_job_id: int
    sockets_per_node: str
    cores_per_socket: str
    threads_per_core: str
    array_task_id: str
    time_left: datetime.timedelta
    time: datetime.datetime
    nodelist: str
    contiguous: int
    partition: str
    nodelist_reason: str
    start_time: datetime.datetime
    state: JobStateCodes
    uid: int
    submit_time: datetime.datetime
    licenses: str
    core_spec: str
    scheduled_nodes: str
    work_dir: str

    @field_validator('state', mode='before')
    @classmethod
    def state_validator(cls, value: str) -> JobStateCodes:
        return JobStateCodes(value.split()[0])

    @property
    def start_delay(self) -> datetime.timedelta:
        return self.start_time - self.submit_time

    @property
    def run_time(self) -> datetime.timedelta:
        if self.state == JobStateCodes.RUNNING:
            # only report full seconds.
            return datetime.timedelta(seconds=math.ceil((datetime.datetime.now() - self.start_time).total_seconds()))
        return datetime.timedelta(0)

    @field_validator('time_limit', 'time_left', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})

    @field_validator('time', 'start_time', 'end_time', mode='before')
    @classmethod
    def datetime_validator(cls, value: str) -> datetime.datetime:
        try:
            return dateutil.parser.parse(value)
        except ValueError:
            return datetime.datetime(year=1970, month=1, day=1)

    @field_validator('min_memory', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


class CfgTRES(BaseModel):
    cpu: int = -1
    mem: str = 'NA'
    billing: int = -1
    gpu: int = -1


class AllocTRES(BaseModel):
    cpu: int = -1
    mem: str = 'NA'
    gpu_alloc: int | None = None
    gpu_type: str | None = None
    gpu_total: int | None = None


class GPU(BaseModel):
    name: str
    amount: int


# noinspection PyNestedDecorators
class Node(BaseModel):
    node_name: str
    arch: str
    cores_per_socket: int
    cpu_alloc: int
    cpu_efctv: int
    cpu_tot: int
    cpuload: float
    available_features: list[str]
    active_features: list[str]
    gres: GPU | None
    node_addr: str
    node_hostname: str
    version: str
    os: str
    real_memory: int
    alloc_mem: int
    freemem: int
    sockets: int
    boards: int
    state: State
    threads_per_core: int
    tmp_disk: int
    weight: int
    owner: str
    mcs_label: str
    partitions: list[str]
    boot_time: datetime.datetime | None
    slurmd_start_time: datetime.datetime
    last_busy_time: datetime.datetime
    resume_after_time: datetime.datetime | None
    cfgtres: CfgTRES
    alloc_tres: AllocTRES

    @property
    def cpu_avail(self) -> int:
        return self.cpu_tot - self.cpu_alloc

    @property
    def gpu_tot(self) -> int:
        if self.gres:
            return self.gres.amount
        return 0

    @property
    def gpu_alloc(self) -> int:
        if self.alloc_tres.gpu_alloc:
            return self.alloc_tres.gpu_alloc
        return 0

    @property
    def gpu_avail(self) -> int:
        if self.gres:
            return self.gpu_tot - self.gpu_alloc
        return 0

    @property
    def gpu_type(self) -> str:
        if self.gres:
            return self.gres.name
        return ''

    @property
    def mem_tot(self) -> int:
        return self.real_memory // 1024

    @property
    def mem_alloc(self) -> int:
        return self.alloc_mem // 1024

    @property
    def mem_avail(self) -> int:
        return self.mem_tot - self.mem_alloc

    @property
    def gpu_mem(self) -> str:
        for feature in self.available_features:
            if feature.startswith('gpu-'):
                return feature.lstrip('gpu-')
        return ''

    @property
    def short_name(self) -> str:
        return self.node_name[8:]

    @property
    def cpu_gpu(self) -> float | None:
        if self.gpu_avail == 0:
            return None
        return self.cpu_avail / self.gpu_avail

    @property
    def mem_gpu(self) -> float | None:
        if self.gpu_avail == 0:
            return None
        return self.mem_avail / self.gpu_avail

    @field_validator('resume_after_time', 'boot_time', mode='before')
    @classmethod
    def date_validator(cls, value: Any) -> datetime.datetime | None:
        if not isinstance(value, datetime.datetime) and len(value) > 0:
            return None
        # noinspection PyTypeChecker
        return dateutil.parser.parse(value)

    @field_validator('available_features', 'active_features', 'partitions', mode='before')
    @classmethod
    def list_validator(cls, value: str) -> list[str]:
        return value.split(',')

    @field_validator('gres', mode='before')
    @classmethod
    def split_validator(cls, value: str) -> GPU | None:
        data = value.split(':')
        if len(data) != 3:
            return None
        return GPU(name=data[1], amount=int(data[2]))

    @field_validator('cfgtres', mode='before')
    @classmethod
    def cfgtres_validator(cls, value: str) -> CfgTRES:
        m = re.search(CFGTRESS_RE, value)
        if not m:
            return CfgTRES()

        return CfgTRES(**m.groupdict())

    @field_validator('alloc_tres', mode='before')
    @classmethod
    def alloctres_validator(cls, value: str) -> AllocTRES:
        m = re.search(ALLOCTRESS_RE, value)
        if not m:
            return AllocTRES()

        return AllocTRES(**m.groupdict())


class TrackableResourceUsage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cpu: datetime.timedelta | None = None
    energy: int | None = None
    disk: MemoryUsed | None = None
    gpu_mem: MemoryUsed | None = None
    gpu_util: int | None = None
    mem: MemoryUsed | None = None
    pages: int | None = None
    vmem: MemoryUsed | None = None

    @field_validator('cpu', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})

    @field_validator('gpu_mem', 'mem', 'vmem', 'disk', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


class ReqAllocTrackableResources(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    cpu: int | None = None
    mem: MemoryUsed | None = None
    billing: int | None = None
    gpu: int | None = None
    gpu_name: str | None = None
    node: int | None = None
    energy: int | None = None

    @field_validator('mem', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)


class Job(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    JobID: str
    JobIDRaw: str
    JobName: str
    Partition: str
    MaxVMSize: MemoryUsed
    MaxVMSizeNode: str
    MaxVMSizeTask: str
    AveVMSize: MemoryUsed
    MaxRSS: MemoryUsed
    MaxRSSNode: str
    MaxRSSTask: str
    AveRSS: MemoryUsed
    MaxPages: str
    MaxPagesNode: str
    MaxPagesTask: str
    AvePages: str
    MinCPU: datetime.timedelta
    MinCPUNode: str
    MinCPUTask: str
    AveCPU: datetime.timedelta
    NTasks: str
    AllocCPUS: int
    Elapsed: datetime.timedelta
    State: JobStateCodes
    ExitCode: ExitCodeSignal
    AveCPUFreq: PostFixUnit
    ReqCPUFreqMin: PostFixUnit
    ReqCPUFreqMax: PostFixUnit
    ReqCPUFreqGov: PostFixUnit
    ReqMem: MemoryUsed
    ConsumedEnergy: PostFixUnit
    MaxDiskRead: MemoryUsed
    MaxDiskReadNode: str
    MaxDiskReadTask: str
    AveDiskRead: MemoryUsed
    MaxDiskWrite: MemoryUsed
    MaxDiskWriteNode: str
    MaxDiskWriteTask: str
    AveDiskWrite: MemoryUsed
    ReqTRES: ReqAllocTrackableResources
    AllocTRES: ReqAllocTrackableResources
    TRESUsageInAve: TrackableResourceUsage
    TRESUsageInMin: TrackableResourceUsage
    TRESUsageInMax: TrackableResourceUsage
    TRESUsageInTot: TrackableResourceUsage
    TRESUsageInMaxNode: str
    TRESUsageInMaxTask: str
    TRESUsageInMinNode: str
    TRESUsageInMinTask: str
    TRESUsageOutMaxNode: str
    TRESUsageOutMaxTask: str
    TRESUsageOutMax: str
    TRESUsageOutAve: str
    TRESUsageOutTot: str

    @field_validator('TRESUsageInAve', 'TRESUsageInMax', 'TRESUsageInMin', 'TRESUsageInTot', mode='before')
    @classmethod
    def tres_usage_in_ave_validator(cls, value: str) -> TrackableResourceUsage:
        m = re.search(TRES_USAGE_IN_AVE_RE, value)
        if not m:
            return TrackableResourceUsage()

        return TrackableResourceUsage(**m.groupdict())

    @field_validator('ReqTRES', 'AllocTRES', mode='before')
    @classmethod
    def req_alloc_tres_validator(cls, value: str) -> ReqAllocTrackableResources:
        if len(value) == 0:
            return ReqAllocTrackableResources()

        data = {}
        for key_values in value.split(','):
            key, value = key_values.split('=', maxsplit=1)
            if key == 'gres/gpu':
                key = 'gpu'
            if key.startswith('gres/gpu:'):
                value = key.split(':')[-1]
                key = 'gpu_name'
            data[key] = value

        return ReqAllocTrackableResources(**data)

    @field_validator('State', mode='before')
    @classmethod
    def state_validator(cls, value: str) -> JobStateCodes:
        return JobStateCodes(value.split()[0])

    @field_validator('ExitCode', mode='before')
    @classmethod
    def exit_code_validator(cls, value: str) -> ExitCodeSignal:
        return ExitCodeSignal(value)

    @field_validator('ReqMem', 'AveDiskWrite', 'AveDiskRead', 'MaxDiskWrite', 'MaxDiskRead', 'MaxVMSize', 'AveVMSize',
                     'AveRSS', 'MaxRSS', mode='before')
    @classmethod
    def mem_validator(cls, value: str) -> MemoryUsed:
        return MemoryUsed(value)

    @field_validator('AveCPUFreq', 'ReqCPUFreqMin', 'ReqCPUFreqMax', 'ReqCPUFreqGov', 'ConsumedEnergy', mode='before')
    @classmethod
    def post_fix_validator(cls, value: str) -> PostFixUnit:
        return PostFixUnit(value)

    @field_validator('Elapsed', 'MinCPU', 'AveCPU', mode='before')
    @classmethod
    def timedelta_validator(cls, value: str) -> datetime.timedelta:
        m = re.search(CPU_TIME_RE, value)
        if not m:
            return datetime.timedelta(0)

        return datetime.timedelta(**{k: float(v) for k, v in m.groupdict().items() if v is not None})

    def __repr__(self) -> str:
        return f'{self.JobID=}, {self.JobName=}, {self.State=}'


class Priority(BaseModel):
    age_n: float
    age_w: float
    association_n: float
    association_w: float
    cluster_name: str
    fair_share_n: float
    fair_share_w: float
    job_id: int
    job_size_n: float
    job_size_w: float
    qos_name: str
    nice_adjustment: float
    account_name: str
    partition_n: float
    partition_w: float
    qos_n: float
    qos_w: float
    partition_name: str
    admin_w: float
    tres_n: str
    tres_w: str
    user_name: str
    job_priority_n: float
    job_priority_w: float
