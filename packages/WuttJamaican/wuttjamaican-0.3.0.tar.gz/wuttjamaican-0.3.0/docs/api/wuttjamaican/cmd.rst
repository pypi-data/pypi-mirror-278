
``wuttjamaican.cmd``
====================

.. automodule:: wuttjamaican.cmd
   :members:

The core framework is contained in :mod:`wuttjamaican.cmd.base`.

Note that :class:`~wuttjamaican.cmd.base.Command` serves as the base
class for top-level :term:`commands<command>` but it also functions as
the top-level ``wutta`` command.

Some :term:`subcommands<subcommand>` are available as well; these are
registered under the ``wutta`` command.

.. toctree::
   :maxdepth: 1

   cmd.base
   cmd.date_organize
   cmd.make_appdir
   cmd.setup
