Undo
====

Undoes the last change you've made.

Syntax
------

.. code-block:: bash

        undo 
                undoes the last change to the table

Examples
--------
Undo changes in the table:

.. code-block:: bash

        1 SCOUT
        2 AWESOME_MPRAGE
        
        >> rename 2 okay_mprage

        1 SCOUT
        2 okay_mprage

        >> ignore 1

        2 okay_mprage

        >> undo

        1 SCOUT
        2 okay_mprage

        >> undo

        1. SCOUT
        2. AWESOME_MPRAGE

        >> undo

        No further changes to undo.
