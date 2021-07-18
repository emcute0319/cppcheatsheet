==================================
Bash Regular Expression Cheatsheet
==================================

.. contents:: Table of Contents
    :backlinks: none

``grep`` vs ``grep -E``
-----------------------

The difference between grep and grep -E is that grep uses basic regular
expressions while grep -E uses extended regular expressions. In basic
regular expressions, the characters "?", "+", "{", "|", "(",")" lose their
special meaning; instead, use "?", "+", "{", "|", "(", ")".


.. code-block:: bash

    $ echo "987-123-4567" | grep "^[0-9]\{3\}-[0-9]\{3\}-[0-9]\{4\}$"
    $ echo "987-123-4567" | grep -E "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"
