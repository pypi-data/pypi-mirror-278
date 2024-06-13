from typing import Any

import textual


class Loading:
    def __init__(self, widget: textual.widget.Widget) -> None:
        self.widget = widget

    def __enter__(self) -> None:
        self.widget.loading = True

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.widget.loading = False
