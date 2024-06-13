CPU_TIME_RE = r'^(?:(?P<days>\d+)-)?(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$'


class PostFixUnit:
    def __init__(self, value: str) -> None:
        self.value: float | None = None
        if value.endswith('K'):
            self.value = float(value[:-1]) / 1024
            return

        if value.endswith('M'):
            self.value = float(value[:-1])
            return

        if value.endswith('G'):
            self.value = float(value[:-1]) * 1024
            return

        try:
            self.value = float(value) / (1024 * 1204)
        except ValueError:
            self.value = None

    def __str__(self) -> str:
        return f'{self.value}'

    def __repr__(self) -> str:
        return f'{self.value}'


class MemoryUsed:
    def __init__(self, value: str) -> None:
        self.value: float | None = None
        if value.endswith('K'):
            self.value = float(value[:-1]) / 1024
            return

        if value.endswith('M'):
            self.value = float(value[:-1])
            return

        if value.endswith('G'):
            self.value = float(value[:-1]) * 1024
            return

        try:
            self.value = float(value) / (1024 * 1024)
        except ValueError:
            self.value = None

    def __str__(self) -> str:
        return f'{self.GB}GB'

    def __repr__(self) -> str:
        return f'{self.GB}GB'

    @property
    def MB(self) -> float:  # pylint: disable=invalid-name
        if self.value is None:
            return 0.0
        return self.value

    @property
    def GB(self) -> float:  # pylint: disable=invalid-name
        if self.value is None:
            return 0.0
        return self.value // 1024
