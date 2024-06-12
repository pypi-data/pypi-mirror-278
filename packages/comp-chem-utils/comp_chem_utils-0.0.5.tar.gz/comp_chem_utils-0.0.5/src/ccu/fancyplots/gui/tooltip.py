"""A robust tooltip class.

This module provides the :class:`Tooltip` class.
"""

import tkinter as tk
from tkinter import ttk


class Tooltip:
    """Create a tooltip for a given widget as the mouse goes on it.

    see:

    http://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-
           in-tkinter/36221216#36221216

    http://www.daniweb.com/programming/software-development/
           code/484591/a-tooltip-class-for-tkinter

    - Originally written by vegaseat on 2014.09.09.

    - Modified to include a delay time by Victor Zaccardo on 2016.03.25.

    Attributes:
        parent: The widget over which the user must hover to activate the
            tooltip.
        bg: The tooltip background as a hex string. Defaults to `"#FFFFEA"`.
        pad: A 4-tuple `(left, top, bottom, right)`, indicating the
            padding around the text within the tooltip (in pixels).
        text: The text displayed in the tooltip. Defaults to an empty string.
        waittime: Time before displaying (in milliseconds). Defaults to `400`.
        wraplength: Length before wrapping text (in pixels). Defaults to `250`.

    """

    def __init__(
        self,
        parent: tk.Widget | ttk.Widget,
        *,
        bg: str = "#000000",
        pad: tuple[float, float, float, float] = (5, 3, 5, 3),
        text: str = "",
        waittime: int = 400,
        wraplength: float = 250,
    ) -> None:
        """Create a tooltip.

        Args:
            parent: The parent widget over which one must hover to generate
                the tooltip.
            bg: The tooltip background. Defaults to "#FFFFEA".
            pad: The padding to use for the tooltip. Defaults to (5, 3, 5, 3).
            text: The text to display on the tooltip. Defaults to "".
            waittime: The time (in milliseconds) to wait for a user to hover
                before generating the tooltip. Defaults to 400.
            wraplength: The character length at which the tooltip message will
                wrap. Defaults to 250.
        """
        self._id: str | None = None
        self._top_level: tk.Toplevel | None = None
        self.parent = parent
        self.bg = bg
        self.pad = pad
        self.text = text
        self.waittime = waittime
        self.wraplength = wraplength
        self._bind_keys()

    def on_enter(self, _: tk.Event | None = None) -> None:
        """Begin counting to display the tooltip."""
        self.schedule()

    def on_leave(self, _: tk.Event | None = None) -> None:
        """Stop counting to display the tooltip."""
        self.unschedule()
        self.hide()

    def schedule(self) -> None:
        """Plan to display the tooltip."""
        self.unschedule()
        self._id = self.parent.after(self.waittime, self.show)

    def unschedule(self) -> None:
        """Cancel scheduling to show the tooltip."""
        id_ = self._id
        self._id = None
        if id_:
            self.parent.after_cancel(id_)

    def show(self) -> None:
        """Show the tooltip."""

        def calculate_tooltip_position(
            widget: tk.Widget | ttk.Widget,
            label: tk.Label,
            *,
            offset: tuple[float, float] = (10, 5),
            pad: tuple[float, float, float, float] = (5, 3, 5, 3),
        ) -> tuple[float, float]:
            """Calculate the position of the tooltip based on cursor position.

            Args:
                widget: The hidden :class:`tk.Toplevel` widget to which the
                    tooltip belongs.
                label: The :class:`tk.Label` widget used to display to tooltip.
                offset: A 2-tuple `(offset_x, offset_y)` indicating the
                    number of pixels by which to offset the tooltip from the
                    left and top of the cursor, respectively. Defaults to
                    `(10, 5)`.
                pad: 4-tuple `(left, top, bottom, right)` indicating the
                    number of pixels by which to pad the label from the left,
                    top, bottom and right, respectively. Defaults to
                    `(5, 3, 5, 3)`.

            Returns:
                A 2-tuple `(x, y)`, representing the position of the tooltip.

            """
            w = widget
            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()
            width, height = (
                pad[0] + label.winfo_reqwidth() + pad[2],
                pad[1] + label.winfo_reqheight() + pad[3],
            )
            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + offset[0], mouse_y + offset[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            # offscreen
            if (x_delta, y_delta) != (0, 0):
                x1 = mouse_x - offset[0] - width if x_delta else x1
                y1 = mouse_y - offset[1] - height if y_delta else y1

            # offscreen_again - out on the top; no further checks will be done
            y1 = 0 if y1 < 0 else y1

            return x1, y1

        # Leaves only the label and removes the app window
        self._top_level = tk.Toplevel(self.parent)
        self._top_level.wm_overrideredirect(True)

        frame = ttk.Frame(self._top_level, borderwidth=0)
        # This must remain a tk.Label due to rendering issues
        # see https://stackoverflow.com/a/41381685
        label = tk.Label(
            frame,
            text=self.text,
            justify=tk.LEFT,
            background=self.bg,
            foreground="#FFFFFF",
            relief=tk.SOLID,
            borderwidth=0,
            wraplength=self.wraplength,
        )

        label.grid(
            padx=(self.pad[0], self.pad[2]),
            pady=(self.pad[1], self.pad[3]),
            sticky=tk.NSEW,
        )
        frame.grid()

        x, y = calculate_tooltip_position(self.parent, label)
        self._top_level.wm_geometry(f"+{x}+{y}")

    def hide(self) -> None:
        """Hide the tooltip."""
        if self._top_level:
            self._top_level.destroy()
        self._top_level = None

    def _bind_keys(self) -> None:
        """Configure key bindings."""
        self.parent.bind("<Enter>", self.on_enter)
        self.parent.bind("<Leave>", self.on_leave)
        self.parent.bind("<ButtonPress>", self.on_leave)
