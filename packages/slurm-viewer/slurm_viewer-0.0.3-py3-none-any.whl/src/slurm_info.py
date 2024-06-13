import subprocess
from pathlib import Path

from src.config import Config


def partitions(config: Config) -> list[str]:
    try:
        args = f'ssh -t {config.server} ' if config.server is not None else ''
        args += 'sinfo --format=%R --noheader'

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
