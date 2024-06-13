import csv
import datetime
from io import StringIO
from typing import Any

from rich.text import Text
from textual import work, on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Static, Label, Button, Checkbox

import src.slurm_info
import src.slurm_queue
from src.config import Config
from src.loading import Loading
from src.models import Queue, JobStateCodes
from src.sortable_data_table import SortableDataTable


class QueueWidget(Static):
    CSS_PATH = 'slurm_viewer.tcss'

    config: reactive[Config] = reactive(Config.init, layout=True, always_update=True)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.queue_info: list[Queue] = src.slurm_queue.info(self.config)
        self.partitions: list[str] = src.slurm_info.partitions(self.config)

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id='queue_horizontal'):
                yield Label(id='queue_label')
                yield Button(label='Refresh', id='queue_refresh')
            with ScrollableContainer(id='queue_scrollable_container'):
                yield SortableDataTable(id='queue_running_table')
                yield SortableDataTable(id='queue_pending_table')

    @work(thread=True)
    def watch_config(self, _: Config, __: Config) -> None:
        with Loading(self):
            self.queue_info = src.slurm_queue.info(self.config)
            self.query_one('#queue_label', Label).update(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}')
        self._update_table()

    def on_mount(self) -> None:
        self._update_table()

    def copy_to_clipboard(self) -> None:
        with StringIO() as fp:
            fieldnames = list(self.queue_info[0].model_dump().keys())
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for node in self.queue_info:
                writer.writerow(node.model_dump())

            self.app.copy_to_clipboard(fp.getvalue())
            self.app.notify('Copied queues to clipboard')

    def _update_table(self) -> None:
        if not self.is_mounted:
            return

        table = self.query_one('#queue_running_table', SortableDataTable)

        jobs = [x for x in self.queue_info if x.state == JobStateCodes.RUNNING]
        table.border_title = f'Running Jobs ({len(jobs)})'
        self._queue_data_table(jobs, table)

        table = self.query_one('#queue_pending_table', SortableDataTable)

        jobs = [x for x in self.queue_info if x.state == JobStateCodes.PENDING]
        table.border_title = f'Pending Jobs ({len(jobs)})'
        self._queue_data_table(jobs, table)

        self.query_one('#queue_label', Label).update(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}')

    def _queue_data_table(self, queue: list[Queue], data_table: SortableDataTable) -> None:
        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*self.config.queue_columns)

        for index, row in enumerate(queue, 1):
            label = Text(str(index), style='#B0FC38 italic')
            data = [getattr(row, key) for key in self.config.queue_columns]
            data_table.add_row(*data, label=label)

    @work(thread=True)
    @on(Button.Pressed, '#queue_refresh')
    def refresh_info(self, _: Checkbox.Changed) -> None:
        self._update_table()
