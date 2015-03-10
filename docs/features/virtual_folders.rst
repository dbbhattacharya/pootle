.. _virtual_folders:

Virtual Folders
===============

.. versionadded:: 2.7

Virtual folders provide a way to group translations based on any criteria,
including a file across all the languages in a project, or files on specific
locations. Virtual folders have priority, so they can be used to allow
translators to focus on the most important work.


.. _virtual_folders#attributes:

Virtual folders' attributes
---------------------------

Virtual folders have several attributes:

- A mandatory lowercase name,
- A mandatory location,
- An optional priority,
- An optional browsability flag,
- An optional description,
- An optional filtering rule.

The location indicates the root place where the virtual folder applies. It can
use placeholders for language (``{LANG}``) and project (``{PROJ}``).

Each virtual folder must have a unique combination of name and location. This
means that there can exist two different virtual folders with the same name if
they have different locations.

The priority defaults to ``1`` and accepts any value greater than ``0``,
including numbers with decimals, like ``0.75``. Higher numbers means higher
priority.

By default virtual folders can be browsed.

Also the virtual folders can have a description which might be useful to
explain the contents of the folder or provide additional instructions. This
might be handy when using the virtual folders as goals.

The filtering rule specifies which translation units are included within a
virtual folder. Currently it consists of a list of file paths relative to the
virtual folder location.
