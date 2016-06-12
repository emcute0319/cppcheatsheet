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


single dollar sign and double dollar sign
------------------------------------------

+-------------+-----------------------------------------+
| dollar sign | descriptions                            |
+-------------+-----------------------------------------+
|     ``$``   | reference a make variable using ``$``   |
+-------------+-----------------------------------------+
|    ``$$``   | reference a shell variable using ``$$`` |
+-------------+-----------------------------------------+

Makefile

.. code-block:: make

    LIST = one two three

    .PHONY: all single_dollar double_dollar

    all: single_dollar double_dollar

    double_dollar:
            @echo "=== double dollar sign example ==="
            @for i in $(LIST); do \
                    echo $$i;     \
            done

    single_dollar:
            @echo "=== single dollar sign example ==="
            @for i in $(LIST); do  \
                    echo $i;     \
            done


output

.. code-block:: bash

    $ make
    === single dollar sign example ===



    === double dollar sign example ===
    one
    two
    three


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


using ``$(eval)`` predefine variables
--------------------------------------

without ``$(eval)``

.. code-block:: make

    SRC = $(wildcard *.c)
    EXE = $(subst .c,,$(SRC))

    define PROGRAM_template
    $1_SHARED = lib$(strip $1).so
    endef

    .PHONY: all

    $(foreach exe, $(EXE), $(call PROGRAM_template, $(exe)))

    all:
            @echo $(foo_SHARED)
            @echo $(bar_SHARED)

output

.. code-block:: bash

    $ make
    Makefile:11: *** missing separator.  Stop.


with ``$(evall)``

.. code-block:: make

    CFLAGS  += -Wall -g -O2 -I./include
    SRC = $(wildcard *.c)
    EXE = $(subst .c,,$(SRC))

    define PROGRAM_template
    $1_SHARED = lib$(strip $1).so
    endef

    .PHONY: all

    $(foreach exe, $(EXE), $(eval $(call PROGRAM_template, $(exe))))

    all:
            @echo $(foo_SHARED)
            @echo $(bar_SHARED)

output

.. code-block:: bash

    $ make
    libfoo.so
    libbar.so


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


build shared and static library
--------------------------------

directory layout

.. code-block:: bash

    .
    |-- Makefile
    |-- include
    |   |-- bar.h
    |   `-- foo.h
    `-- src
        |-- Makefile
        |-- bar.c
        `-- foo.c

Makefile

.. code-block:: make

    SUBDIR = src

    .PHONY: all clean $(SUBDIR)

    all: $(SUBDIR)

    clean: $(SUBDIR)

    $(SUBDIR):
            make -C $@ $(MAKECMDGOALS)


src/Makefile

.. code-block:: bash

    SRC      = $(wildcard *.c)
    OBJ      = $(SRC:.c=.o)
    LIB      = libfoobar

    STATIC   = $(LIB).a
    SHARED   = $(LIB).so.1.0.0
    SONAME   = $(LIB).so.1
    SOFILE   = $(LIB).so

    CFLAGS  += -Wall -Werror -g -O2 -fPIC -I../include
    LDFLAGS += -shared -Wl,-soname,$(SONAME)

    .PHONY: all clean

    all: $(STATIC) $(SHARED) $(SONAME) $(SOFILE)

    $(SOFILE): $(SHARED)
            ln -sf $(SHARED) $(SOFILE)

    $(SONAME): $(SHARED)
            ln -sf $(SHARED) $(SONAME)

    $(SHARED): $(STATIC)
            $(CC) $(LDFLAGS) -o $@ $<

    $(STATIC): $(OBJ)
            $(AR) $(ARFLAGS) $@ $^

    %.o: %.c
            $(CC) $(CFLAGS) -c -o $@ $<

    clean:
            rm -rf *.o *.a *.so *.so.*

output

.. code-block:: bash

    $ make
    make -C src 
    make[1]: Entering directory '/root/test/src'
    cc -Wall -Werror -g -O2 -fPIC -I../include -c -o foo.o foo.c
    cc -Wall -Werror -g -O2 -fPIC -I../include -c -o bar.o bar.c
    ar rv libfoobar.a foo.o bar.o
    ar: creating libfoobar.a
    a - foo.o
    a - bar.o
    cc -shared -Wl,-soname,libfoobar.so.1 -o libfoobar.so.1.0.0 libfoobar.a
    ln -sf libfoobar.so.1.0.0 libfoobar.so.1
    ln -sf libfoobar.so.1.0.0 libfoobar.so
    make[1]: Leaving directory '/root/test/src'


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


replace current shell
----------------------

.. code-block:: make

    OLD_SHELL := $(SHELL)
    SHELL = /usr/bin/python

    .PHONY: all

    all:
            @import os; print os.uname()[0]

output

.. code-block:: bash

    $ make
    Linux


one line condition
-------------------

syntax: ``$(if cond, then part, else part)``

Makefile

.. code-block:: make

    VAR =
    IS_EMPTY = $(if $(VAR), $(info not empty), $(info empty))

    .PHONY: all

    all:
            @echo $(IS_EMPTY)

output

.. code-block:: bash

    $ make
    empty

    $ make VAR=true
    not empty


Using define to control CFLAGS
--------------------------------

Makefile

.. code-block:: make

    CFLAGS += -Wall -Werror -g -O2
    SRC     = $(wildcard *.c)
    OBJ     = $(SRC:.c=.o)
    EXE     = $(subst .c,,$(SRC))

    ifdef DEBUG
    CFLAGS += -DDEBUG
    endif

    .PHONY: all clean

    all: $(OBJ) $(EXE)

    clean:
            rm -rf $(OBJ) $(EXE)


output

.. code-block:: bash

    $ make
    cc -Wall -Werror -g -O2   -c -o foo.o foo.c
    cc   foo.o   -o foo
    $ make DEBUG=1
    cc -Wall -Werror -g -O2 -DDEBUG   -c -o foo.o foo.c
    cc   foo.o   -o foo
