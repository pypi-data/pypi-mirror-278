import subprocess
from pathlib import Path

from src.config import Config
from src.models import Priority


# Add export SPRIO_FORMAT="%a|%A|%B|%b|%c|%f|%F|%i|%j|%J|%n|%N|%o|%p|%P|%q|%Q|%r|%S|%t|%T|%u|%y|%Y" to the top of .bashrc,
# before the 'If not running interactively , don't do anything' line


def info(config: Config) -> list[Priority]:
    try:
        partitions = ",".join(config.partitions)
        arguments = f'ssh -tt {config.server} ' if config.server is not None else ''
        arguments += f'"sprio --partition={partitions}"'

        with subprocess.Popen(arguments, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True) as process:
            stdout, _ = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        print(f'{Path(__file__).name}: TimeoutExpired')
        return []
    except subprocess.CalledProcessError:
        print(f'{Path(__file__).name}: CalledProcessError')
        return []

    header = list(Priority.model_fields.keys())

    lines = stdout.splitlines()
    if len(lines) == 0:
        return []

    result = []
    for line in lines[1:]:  # skip the first row (it's the header)
        result.append(Priority(**dict(zip(header, line.rstrip().split('|')))))

    return result
