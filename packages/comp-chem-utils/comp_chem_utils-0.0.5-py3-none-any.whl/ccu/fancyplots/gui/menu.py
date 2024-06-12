"""Functions for menu creation and manipulation."""

from collections.abc import Callable
import tkinter as tk
from tkinter import ttk


def create_edit_menu(root: tk.Widget | ttk.Widget) -> tk.Menu:
    """Create an edit menu.

    Args:
        root: The master object for the menu.

    Returns:
        The created edit menu.
    """
    the_menu = tk.Menu(root, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")
    the_menu.add_separator()
    the_menu.add_command(label="Select all")
    return the_menu


def show_edit_menu(root: tk.Widget | ttk.Widget) -> Callable[[tk.Event], None]:
    """Create an event handler that shows a cut-copy-paste-select all menu.

    Args:
        root: A widget to which the menu will belong.

    Returns:
        A handler that can create an edit menu.
    """

    def handler(event: tk.Event) -> None:
        menu = create_edit_menu(root)
        widget: ttk.Entry = event.widget

        def _generate_command(command: str) -> Callable[[], None]:
            return lambda _: widget.event_generate(command)

        menu.entryconfigure("Cut", command=_generate_command("<<Cut>>"))
        menu.entryconfigure("Copy", command=_generate_command("<<Copy>>"))
        menu.entryconfigure("Paste", command=_generate_command("<<Paste>>"))
        menu.entryconfigure("Select all", command=widget.selectrange(0, "end"))
        menu.tk.call("tk_popup", menu, event.x_root, event.y_root)

    return handler
