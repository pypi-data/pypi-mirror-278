"""A subpackage for the FancyPlots GUI.

The FancyPlots GUI can be launched programatically a via the following idiom:

.. code-block:: python

    import tkinter as tk
    from ccu.fancyplots.gui.root import FancyPlotsGUI

    root = tk.Tk()
    app = FancyPlotsGUI(master=root)
    app.master.mainloop()

Alternatively, the GUI can be launched from the command line, via the
:program:`ccu-fancyplots` subcommand:

.. code-block:: console

    ccu fed

In both cases, one has the option to load data from a previous FancyPlots
session by specifying a cache file via the ``cache_file`` parameter of
the :class:`ccu.fancyplots.gui.root.FancyPlotsGUI` constructor or the
:option:`ccu-fancyplots --cache` CLI option of ``ccu fed``.
"""
