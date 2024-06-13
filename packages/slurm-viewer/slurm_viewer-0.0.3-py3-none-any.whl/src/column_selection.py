from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import SelectionList, Button
from textual.widgets.selection_list import Selection


class ColumnSelectionScreen(Screen):
    CSS_PATH = 'slurm_viewer.tcss'

    def __init__(self, selection: list[Selection]) -> None:
        super().__init__()
        self.selection = selection

    def compose(self) -> ComposeResult:
        yield Grid(
            SelectionList(*self.selection, id='selection'),
            Button('OK', variant='success', id='ok'),
            Button('Cancel', variant='primary', id='cancel'),
            id='dialog',
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'ok':
            self.dismiss(self.query_one(SelectionList).selected)
        else:
            self.dismiss(None)
