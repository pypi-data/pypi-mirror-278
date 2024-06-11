
Commands
========

Top-level :term:`commands<command>` are primarily a way to group
:term:`subcommands<subcommand>`.


.. _running-commands:

Running a Command
-----------------

Top-level commands are installed in such a way that they are available
within the ``bin`` folder of the virtual environment.  (Or the
``Scripts`` folder if on Windows.)  For instance:

.. code-block:: sh

   cd /path/to/venv
   bin/wutta --help

This folder should be in the ``PATH`` when the virtual environment is
activated, in which case you can just run the command by name, e.g.:

.. code-block:: sh

   wutta --help

To actually *do* anything you must also specify a subcommand, e.g.:

.. code-block:: sh

   wutta make-appdir

Many subcommands may accept arguments of their own:

.. code-block:: sh

   wutta make-appdir --path=/where/i/want/my/appdir

But top-level commands also accept global arguments.  See the next
section for the full list of "global" command options.  A complete example
then might be like:

.. code-block:: sh

   wutta --config=/path/to/my/file.conf make-appdir --path=/where/i/want/my/appdir

Note that the top-level command will parse its global option args
first, and give only what's leftover to the subcommand.  Therefore it
isn't strictly necessary to specify global options before the
subcommand:

.. code-block:: sh

   wutta make-appdir --path=/where/i/want/my/appdir --config=/path/to/my/file.conf


``wutta`` command
-----------------

WuttJamaican comes with one top-level command named ``wutta``.  Note
that the list of available subcommands is shown in the top-level
command help.

See :mod:`wuttjamaican.cmd` for more on the built-in ``wutta``
subcommands.

.. command-output:: wutta -h
   :returncode: 1


.. _adding-commands:

Adding a New Command
--------------------

There is not much to this since top-level commands are mostly just a
grouping mechanism.

First create your :class:`~wuttjamaican.cmd.base.Command` class, and a
``main()`` function for it (e.g. in ``poser/commands.py``)::

   import sys
   from wuttjamaican.cmd import Command

   class PoserCommand(Command):
       name = 'poser'
       description = 'my custom top-level command'
       version = '0.1'

   def poser_main(*args):
       args = list(args) or sys.argv[1:]
       cmd = PoserCommand()
       cmd.run(*args)

Then register the :term:`entry point(s)<entry point>` in your
``setup.cfg``.  The command name should *not* contain spaces but *may*
include hyphen or underscore.

You can register more than one top-level command if needed; these
could refer to the same ``main()`` function (in which case they
are really aliases) or can use different functions:

.. code-block:: ini

   [options.entry_points]
   console_scripts =
       poser = poser.commands:poser_main
       wutta-poser = poser.commands:wutta_poser_main

Next time your ``poser`` :term:`package` is installed, the command
will be available:

.. code-block:: sh

   cd /path/to/venv
   bin/poser --help
   bin/wutta-poser --help

You will then likely want to add subcommand(s) for this to be useful;
see :ref:`adding-subcommands`.
