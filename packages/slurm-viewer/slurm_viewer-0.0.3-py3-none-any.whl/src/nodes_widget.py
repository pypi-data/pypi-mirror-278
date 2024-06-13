import csv
import datetime
from dataclasses import dataclass
from io import StringIO
from typing import Any, Callable

from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, ScrollableContainer
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, Label, Button, Checkbox

import src.slurm_info
import src.slurm_nodes
from src.config import Config
from src.loading import Loading
from src.models import Node
from src.sortable_data_table import SortableDataTable


@dataclass
class FilterOptions:
    gpu: bool
    gpu_available: bool
    partition: list[str] | None


def filter_nodes(nodes: list[Node], node_filter: FilterOptions) -> list[Node]:
    result = []
    for node in nodes:
        if node_filter.gpu and node.gpu_tot == 0:
            continue

        if node_filter.gpu_available and node.gpu_avail == 0:
            continue

        if node_filter.partition and len(set(node_filter.partition) & set(node.partitions)) == 0:
            continue

        result.append(node)
    return result


def sort_column(value: Any) -> Any:
    if value is None:
        return ''

    if isinstance(value, Text):
        return value.plain

    return value


class NodesWidget(Static):
    CSS_PATH = 'slurm_viewer.tcss'

    config: reactive[Config] = reactive(Config.init, layout=True, always_update=True)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.cluster_info: list[Node] = src.slurm_nodes.info(self.config)
        self.partitions: list[str] = src.slurm_info.partitions(self.config)
        self.sort_function: Callable[[Any], Any] | None = sort_column

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id='nodes_horizontal'):
                yield Checkbox(label='GPU only', id='nodes_show_gpu')
                yield Checkbox(label='GPU available', id='nodes_show_gpu_available')
                yield Label(id='nodes_label')
                yield Button(label='Refresh', id='nodes_refresh')
            with ScrollableContainer(id='nodes_scrollable_container'):
                table = SortableDataTable(id='nodes_data_table')
                table.sort_function = self.sort_function
                yield table

    @work(thread=True)
    def watch_config(self, _: Config, __: Config) -> None:
        try:
            widget: Widget = self.query_one('#nodes_scrollable_container', ScrollableContainer)
        except NoMatches:
            return

        with Loading(widget):
            self.cluster_info = src.slurm_nodes.info(self.config)
            self.query_one('#nodes_label', Label).update(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}')
        self.update_cluster_info()

    def copy_to_clipboard(self) -> None:
        with StringIO() as fp:
            fieldnames = list(self.cluster_info[0].model_dump().keys())
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for node in self.cluster_info:
                writer.writerow(node.model_dump())

            self.app.copy_to_clipboard(fp.getvalue())
            self.app.notify('Copied nodes to clipboard')

    def on_mount(self) -> None:
        self.update_cluster_info()
        self.query_one('#nodes_label', Label).update(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}')

    @on(Checkbox.Changed, '#nodes_show_gpu')
    @on(Checkbox.Changed, '#nodes_show_gpu_available')
    def show_gpu(self, _: Checkbox.Changed) -> None:
        self.update_cluster_info()

    @work(thread=True)
    @on(Button.Pressed, '#nodes_refresh')
    def refresh_info(self, _: Checkbox.Changed) -> None:
        data_table = self.query_one(SortableDataTable)

        with Loading(data_table):
            self.cluster_info = src.slurm_nodes.info(self.config)

        self.update_cluster_info()
        self.query_one('#nodes_label', Label).update(f'Last update: {datetime.datetime.now().strftime("%H:%M:%S")}')

    def _checkbox_values(self) -> dict[str, bool]:
        return {x.label.plain: x.value for x in self.query(Checkbox).nodes}

    def update_cluster_info(self) -> None:
        try:
            data_table = self.query_one(SortableDataTable)
        except NoMatches:
            return

        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*self.config.node_columns)

        checkboxes = self._checkbox_values()
        options = FilterOptions(gpu=checkboxes['GPU only'], gpu_available=checkboxes['GPU available'],
                                partition=self.config.partitions)
        self._update_data_table(filter_nodes(self.cluster_info, options), data_table)

    def _update_data_table(self, nodes: list[Node], table: SortableDataTable) -> None:
        table.border_title = f'{len(nodes)} nodes'
        for index, row in enumerate(nodes, 1):
            label = Text(str(index), style='#B0FC38 italic')
            data = []
            for key in self.config.node_columns:
                value = getattr(row, key)
                data.append(value if value is not None else '')
            table.add_row(*data, label=label)
