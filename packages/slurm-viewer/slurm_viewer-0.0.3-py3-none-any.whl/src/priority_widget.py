import datetime
from typing import Any

from rich.text import Text
from textual import work
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Label, Button

from src.config import Config
from src.loading import Loading
from src.models import Priority
from src.slurm_priority import info
from src.sortable_data_table import SortableDataTable


class PriorityWidget(Static):
    CSS_PATH = 'slurm_viewer.tcss'

    config: reactive[Config] = reactive(Config.init, layout=True, always_update=True)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.priority_info: list[Priority] = []

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id='priority_horizontal'):
                yield Label(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}', id='priority_label')
                yield Button(label='Refresh', id='priority_refresh', disabled=True)
            with ScrollableContainer():
                yield SortableDataTable(id='priority_table')

    @work(thread=True)
    def watch_config(self, _: Config, __: Config) -> None:
        with Loading(self):
            self.priority_info = info(self.config)
            self._priority_data_table()

    def on_mount(self) -> None:
        self._priority_data_table()

    def copy_to_clipboard(self) -> None:
        self.app.copy_to_clipboard('PriorityWidget copy to clipboard')

    def _priority_data_table(self) -> None:
        def _text(value: str | int | float) -> Text:
            if isinstance(value, str):
                return Text(value, justify='right')
            if isinstance(value, int):
                return Text(str(value), justify='right')
            if isinstance(value, float):
                if value < 1.0:
                    return Text(f'{value:.6f}', justify='right')
                return Text(f'{value:.0f}', justify='right')
            raise RuntimeError(f'Unexpected type {type(value)}')

        if not self.is_mounted:
            return

        data_table = self.query_one('#priority_table', SortableDataTable)
        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*self.config.priority_columns)
        data_table.border_title = f'{len(self.priority_info)} nodes'

        for index, row in enumerate(self.priority_info, 1):
            label = Text(str(index), style='#B0FC38 italic')
            data = [_text(getattr(row, key)) for key in self.config.priority_columns]
            data_table.add_row(*data, label=label)
