"""Tkinter styles for FancyPlots."""

from tkinter import ttk


def initialize_styles() -> None:
    """Create custom styles for themed widgets."""
    entry_style = ttk.Style()
    entry_style.configure("Fancy.TEntry")
    invalid_entry_style = ttk.Style()
    invalid_entry_style.configure("Invalid.Fancy.TEntry", foreground="red")
