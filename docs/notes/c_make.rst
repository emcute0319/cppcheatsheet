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

    $ make
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

    $ make
    cc -Wall -Werror -fPIC -O2 -g -I./include -c src/foo.c -o src/foo.o
    cc -Wall -Werror -fPIC -O2 -g -I./include -c src/bar.c -o src/bar.o
    cc -shared -Wl,-soname,libfoobar.so.1 -o src/libfoobar.so.1.0.0 src/foo.o src/bar.o


build recursively
--------------------

directory layout

.. code-block:: bash

    .
    |-- Makefile
    |-- include
    |   `-- common.h
    |-- src
    |   |-- Makefile
    |   |-- bar.c
    |   `-- foo.c
    `-- test
        |-- Makefile
        `-- test.c

Makefile

.. code-block:: make

    SUBDIR = src test

    .PHONY: all clean $(SUBDIR)

    all: $(SUBDIR)

    clean: $(SUBDIR)

    $(SUBDIR):
            $(MAKE) -C $@ $(MAKECMDGOALS)


src/Makefile

.. code-block:: make

    SONAME   = libfoobar.so.1
    SHARED   = libfoobar.so.1.0.0
    SOFILE   = libfoobar.so

    CFLAGS  += -Wall -g -O2 -Werror -fPIC -I../include
    LDFLAGS += -shared -Wl,-soname,$(SONAME)

    SRC      = $(wildcard *.c)
    OBJ      = $(SRC:.c=.o)

    .PHONY: all clean

    all: $(SHARED) $(OBJ)

    $(SHARED): $(OBJ)
            $(CC) $(LDFLAGS) -o $@ $^
            ln -sf $(SHARED) $(SONAME)
            ln -sf $(SHARED) $(SOFILE)

    %.o: %.c
            $(CC) $(CFLAGS) -c $< -o $@

    clean:
            rm -rf *.o *.so.* *.a *.so

test/Makefile

.. code-block:: make

    CFLAGS    += -Wall -Werror -g -I../include
    LDFLAGS   += -Wall -L../src -lfoobar

    SRC        = $(wildcard *.c)
    OBJ        = $(SRC:.c=.o)
    EXE        = test_main

    .PHONY: all clean

    all: $(OBJ) $(EXE)

    $(EXE): $(OBJ)
            $(CC) -o $@ $^ $(LDFLAGS)

    %.o: %.c
            $(CC) $(CFLAGS) -c $< -o $@

    clean:
            rm -rf *.so *.o *.a $(EXE)

output

.. code-block:: bash

    $ make
    make -C src 
    make[1]: Entering directory '/root/proj/src'
    cc -Wall -g -O2 -Werror -fPIC -I../include -c foo.c -o foo.o
    cc -Wall -g -O2 -Werror -fPIC -I../include -c bar.c -o bar.o
    cc -shared -Wl,-soname,libfoobar.so.1 -o libfoobar.so.1.0.0 foo.o bar.o
    ln -sf libfoobar.so.1.0.0 libfoobar.so.1
    ln -sf libfoobar.so.1.0.0 libfoobar.so
    make[1]: Leaving directory '/root/proj/src'
    make -C test 
    make[1]: Entering directory '/root/proj/test'
    cc -Wall -Werror -g -I../include -c test.c -o test.o
    cc -o test_main test.o -Wall -L../src -lfoobar
    make[1]: Leaving directory '/root/proj/test'
    $ tree .
    .
    |-- Makefile
    |-- include
    |   `-- common.h
    |-- src
    |   |-- Makefile
    |   |-- bar.c
    |   |-- bar.o
    |   |-- foo.c
    |   |-- foo.o
    |   |-- libfoobar.so -> libfoobar.so.1.0.0
    |   |-- libfoobar.so.1 -> libfoobar.so.1.0.0
    |   `-- libfoobar.so.1.0.0
    `-- test
        |-- Makefile
        |-- test.c
        |-- test.o
        `-- test_main

    3 directories, 14 files
