import subprocess
from pathlib import Path

from src.config import Config


def group_users(config: Config, group: str) -> list[str]:
    try:
        arguments = f'ssh -t {config.server} ' if config.server is not None else ''
        arguments += f'getent group {group}'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print(f'{Path(__file__).name}: TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print(f'{Path(__file__).name}: CalledProcessError')
        return []

    return sorted(stdout.rsplit(':', maxsplit=1)[-1].split(','))
