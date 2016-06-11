======================
C Makefile cheatsheet
======================

Automatic variables
--------------------

+------------------------+-----------------------------------------------------------------+
|   automatic variables  |        descriptions                                             |
+------------------------+-----------------------------------------------------------------+
|         $@             | The file name of the target                                     |
+------------------------+-----------------------------------------------------------------+
|         $<             | The name of the first prerequisite                              |
+------------------------+-----------------------------------------------------------------+
|         $^             | The names of all the prerequisites                              |
+------------------------+-----------------------------------------------------------------+
|         $\+            | prerequisites listed more than once are duplicated in the order |
+------------------------+-----------------------------------------------------------------+

Makefile

.. code-block:: make

    .PHONY: all

    all: hello world

    hello world: foo foo foo bar bar
            @echo "== target: $@ =="
            @echo $<
            @echo $^
            @echo $+

    foo:
            @echo "Hello foo"

    bar:
            @echo "Hello Bar"

output

.. code-block:: bash

    Hello foo
    Hello Bar
    == target: hello ==
    foo
    foo bar
    foo foo foo bar bar
    == target: world ==
    foo
    foo bar
    foo foo foo bar bar


build executable files respectively
------------------------------------

directory layout

.. code-block:: bash

    .
    |-- Makefile
    |-- bar.c
    |-- bar.h
    |-- foo.c
    `-- foo.h

Makefile

.. code-block:: make

    # CFLAGS: Extra flags to give to the C compiler
    CFLAGS   += -Werror -Wall -O2 -g
    SRC       = $(wildcard *.c)
    OBJ       = $(SRC:.c=.o)
    EXE       = $(subst .c,,$(SRC))

    .PHONY: all clean

    all: $(OBJ) $(EXE)

    clean:
        rm -rf *.o *.so *.a *.la $(EXE)


output

.. code-block:: bash

    $ make
    cc -Werror -Wall -O2 -g   -c -o foo.o foo.c
    cc -Werror -Wall -O2 -g   -c -o bar.o bar.c
    cc   foo.o   -o foo
    cc   bar.o   -o bar


build subdir and link together
-------------------------------

directory layout

.. code-block:: bash

    .
    |-- Makefile
    |-- include
    |   `-- foo.h
    `-- src
        |-- foo.c
        `-- main.c

Makefile

.. code-block:: make

    CFLAGS  += -Wall -g -O2 -I./include
    SRC     = $(wildcard src/*.c)
    OBJ     = $(SRC:.c=.o)
    EXE     = main

    .PHONY: all clean

    all: $(OBJ) $(EXE)

    $(EXE): $(OBJ)
            $(CC) $(LDFLAGS) -o $@ $^

    %.o: %.c
            $(CC) $(CFLAGS) -c $< -o $@

    clean:
            rm -rf *.o *.so *.a *.la $(EXE) src/*.o src/*.so src/*a

output

.. code-block:: bash

    cc -Wall -g -O2 -I./include -c src/foo.c -o src/foo.o
    cc -Wall -g -O2 -I./include -c src/main.c -o src/main.o
    cc  -o main src/foo.o src/main.o 


build shared library
---------------------

directory layout

.. code-block:: bash

    .
    |-- Makefile
    |-- include
    |   `-- common.h
    `-- src
        |-- bar.c
        `-- foo.c

Makefile

.. code-block:: make

    SONAME    = libfoobar.so.1
    SHARED    = src/libfoobar.so.1.0.0
    SRC       = $(wildcard src/*.c)
    OBJ       = $(SRC:.c=.o)

    CFLAGS    += -Wall -Werror -fPIC -O2 -g -I./include
    LDFLAGS   += -shared -Wl,-soname,$(SONAME)

    .PHONY: all clean

    all: $(SHARED) $(OBJ)

    $(SHARED): $(OBJ)
            $(CC) $(LDFLAGS) -o $@ $^

    %.o: %.c
            $(CC) $(CFLAGS) -c $^ -o $@

    clean:
            rm -rf src/*.o src/*.so.* src/*.a src/*.la

output

.. code-block:: bash

    cc -Wall -Werror -fPIC -O2 -g -I./include -c src/foo.c -o src/foo.o
    cc -Wall -Werror -fPIC -O2 -g -I./include -c src/bar.c -o src/bar.o
    cc -shared -Wl,-soname,libfoobar.so.1 -o src/libfoobar.so.1.0.0 src/foo.o src/bar.o
