from typing import Protocol, cast

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header, TabbedContent, TabPane, Collapsible

import src.slurm_info
from src.column_selector import ColumnSelection
from src.config import Config
from src.nodes_widget import NodesWidget
from src.plot_widget import PlotWidget
from src.priority_widget import PriorityWidget
from src.queue_widget import QueueWidget


class SlurmTabBase(Protocol):
    def copy_to_clipboard(self) -> None:
        ...


class SlurmViewer(App):
    CSS_PATH = 'slurm_viewer.tcss'

    BINDINGS = [
        Binding('f5', 'reload_config', 'Reload config'),
        Binding('ctrl+b', 'copy_to_clipboard', 'Copy to clipboard')
    ]

    config: reactive[Config] = reactive(Config.init, layout=True, always_update=True)

    def __init__(self) -> None:
        super().__init__()
        self.title = f'{self.__class__.__name__} ({self.config.server})'  # type: ignore
        self.partitions: list[str] = src.slurm_info.partitions(self.config)

    def compose(self) -> ComposeResult:
        yield Header(name=self.config.server, show_clock=True)
        with Vertical():
            with Collapsible(title='Partitions'):
                yield ColumnSelection(self.partitions, self.config.partitions, id='partitions')
            with TabbedContent():
                with TabPane('Nodes', id='tab_cluster'):
                    yield NodesWidget().data_bind(SlurmViewer.config)
                with TabPane('Queue', id='tab_queue'):
                    yield QueueWidget().data_bind(SlurmViewer.config)
                # with TabPane('Priority', id='tab_priority'):
                #     yield PriorityWidget().data_bind(SlurmViewer.config)
                with TabPane('GPU usage', id='tab_gpu_usage'):
                    yield PlotWidget(id='plot').data_bind(SlurmViewer.config)
        yield Footer()

    def action_reload_config(self) -> None:
        self.notify('Reloading configuration')
        self.config = Config.init()  # type: ignore

    def action_copy_to_clipboard(self) -> None:
        pane = self.query_one(TabbedContent).active_pane
        assert pane

        children = pane.children
        assert len(children) == 1

        cast(SlurmTabBase, children[0]).copy_to_clipboard()

    @on(ColumnSelection.SelectedChanged, '#partitions')
    def partitions_changed(self, value: ColumnSelection.SelectedChanged) -> None:
        config = self.config
        config.partitions = value.selection.selection
        self.config = config


if __name__ == "__main__":
    app = SlurmViewer()
    app.run()
