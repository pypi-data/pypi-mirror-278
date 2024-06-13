from __future__ import annotations
from typing import Any

from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.widgets import Static, SelectionList
from textual.widgets.selection_list import Selection


class ColumnSelection(Static):
    CSS_PATH = 'slurm_viewer.tcss'

    class SelectedChanged(Message):
        def __init__(self, selection: ColumnSelection) -> None:
            super().__init__()
            self.selection = selection

        @property
        def control(self) -> ColumnSelection:
            """An alias for `selection_list`."""
            return self.selection

    def __init__(self, columns: list[str], selected: list[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._columns = columns
        self._selected = selected

    def compose(self) -> ComposeResult:
        selections = [Selection(x, x, x in self._selected) for x in self._columns]

        yield SelectionList[str](*selections)

    def select(self, selection: list[str]) -> None:
        selection_list = self.query_one(SelectionList)
        selection_list.deselect_all()
        for value in selection:
            self.query_one(SelectionList).select(value)

    @property
    def selection(self) -> list[str]:
        return self.query_one(SelectionList).selected

    @on(SelectionList.SelectedChanged)
    def selection_changed(self, _: SelectionList.SelectedChanged) -> None:
        self.post_message(ColumnSelection.SelectedChanged(self))
