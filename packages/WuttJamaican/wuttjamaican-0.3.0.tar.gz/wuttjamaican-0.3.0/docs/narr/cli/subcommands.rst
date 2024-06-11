
Subcommands
===========

A top-level :term:`command` may have multiple
:term:`subcommands<subcommand>`.

The top-level command is responsible for invoking the subcommand, but
the subcommand is responsible for performing some action(s).

There is no restriction on what sort of action that might be, but for
sake of clarity it is best to make a distinct subcommand for each
"type" of action needed by the app.


Running a Subcommand
--------------------

You cannot run a subcommand directly; you must run a top-level command
and specify the subcommand as part of the command line arguments.  See
:ref:`running-commands`.

This restriction holds true even when running a subcommand "natively"
from within Python code.  For more info see
:meth:`wuttjamaican.cmd.base.Subcommand.run()`.


Built-in Subcommands
--------------------

WuttJamaican comes with one top-level command named ``wutta`` as well
as a few subcommands under that.

See :mod:`wuttjamaican.cmd` for more on the built-in ``wutta``
subcommands.


.. _adding-subcommands:

Adding a New Subcommand
-----------------------

There are two steps for this:

* define the subcommand
* register it under top-level command(s)

First create a Subcommand class (e.g. by adding to
``poser/commands.py``)::

   from wuttjamaican.cmd import Subcommand

   class Hello(Subcommand):
       """
       Say hello to the user
       """
       name = 'hello'
       description = __doc__.strip()

       def add_args(self):
           self.parser.add_argument('--foo', default='bar', help="Foo value")

       def run(self, args):
           print("hello, foo value is:", args.foo)

You may notice there is nothing in that subcommand definition which
ties it to the ``poser`` top-level command.  That is done by way of
another :term:`entry point` in your ``setup.cfg`` file.

As with top-level commands, you can "alias" the same subcommand so
it appears under multiple top-level commands.  Note that if the
top-level command name contains a hyphen, that must be replaced
with underscore for sake of the subcommand entry point:

.. code-block:: ini

   [options.entry_points]

   poser.subcommands =
       hello = poser.commands:Hello

   wutta_poser.subcommands =
       hello = poser.commands:Hello

Next time your ``poser`` :term:`package` is installed, the subcommand
will be available, so you can e.g.:

.. code-block:: sh

   cd /path/to/venv
   bin/poser hello --help
   bin/wutta-poser hello --help
