from __future__ import annotations

import subprocess
from pathlib import Path

from pydantic import ValidationError

from src.config import Config
from src.models import Job


def _get_lines(server: str | None, partitions: list[str], num_weeks: int = 4) -> list[str]:
    try:
        args = f'ssh -t {server} ' if server is not None else ''
        args += f'sacct --starttime now-{num_weeks}week --long --allusers --parsable2 --partition={",".join(partitions)}'

        with subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print(f'{Path(__file__).name}: TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print(f'{Path(__file__).name}: CalledProcessError')
        return []
    return stdout.splitlines()


def info(config: Config, num_weeks: int) -> list[Job]:
    lines = _get_lines(config.server, config.partitions, num_weeks=num_weeks)

    if len(lines) == 0:
        return []

    header = lines[0].rstrip().split('|')
    try:
        return [Job(**dict(zip(header, x.rstrip().split('|')))) for x in lines[1:]]
    except ValidationError:
        return []
