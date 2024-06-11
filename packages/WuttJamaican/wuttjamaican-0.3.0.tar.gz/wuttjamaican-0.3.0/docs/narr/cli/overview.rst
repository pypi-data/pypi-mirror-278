
Overview
========

The command line interface is an important part of app automation and
may be thought of in a couple ways:

First there is the :term:`ad hoc script` which is a single file and
can be placed anywhere, but is not installed as part of a
:term:`package`.  See :doc:`scripts`.

But the "real" command line interface uses :term:`commands<command>`
and :term:`subcommands<subcommand>`; these are installed as part of a
package.

Top-level commands are mostly just a way to group subcommands.  Most
custom apps would define their own top-level command as well as
multiple subcommands.  See :doc:`commands` for top-level details.

Subcommands on the other hand are the real workhorse since they define
the action logic.  See :doc:`subcommands` for more about those.
