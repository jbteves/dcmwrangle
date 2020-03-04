Redo
====
Redoes the last change you undid. If you make changes without undo/redo then
you will not be able to redo anymore due to a simplistic implementation.

Syntax
------

.. code-block:: bash
        redo
                redoes the last undo you made to the table.

Examples
--------
Redo changes for a whole table:

.. code-block:: bash

        1 AWESOME_MPRAGE

        >> rename 1 okay_mprage

        1 okay_mprage

        >>  undo

        1 AWESOME_MPRAGE

        >> redo

        1 okay_mprage

Scenario where you cannot continue to redo:

.. code-block:: bash

        1 AWESOME_MPRAGE

        >> rename 1 okay_mprage

        1 okay_mprage

        >> undo
        
        1 AWESOME_MPRAGE

        >> rename 1 t1

        1 t1

        >> redo

        Cannot redo; changes made since last undo.
