============================
GNU C Extensions cheatsheet
============================

Statements and Declarations in Expressions
--------------------------------------------

ref: `Statements and Declarations in Expressions <https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Statement-Exprs.html#Statement-Exprs>`_

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    #define square(x)   \
      ({                \
            int y = 0;  \
            y = x * x;  \
            y;          \
       })

    #define max(a, b)           \
      ({                        \
            typeof (a) _a = a;  \
            typeof (b) _b = b;  \
            _a > _b ? _a : _b;  \
       })

    int main(int argc, char *argv[])
    {
            int x = 3;
            int a = 55, b = 66;
            printf("square val: %d\n", square(x));
            printf("max(%d, %d) = %d\n", a, b, max(a, b));
            return 0;
    }

    #endif

output:

.. code-block:: bash

    $ ./a.out
    square val: 9
    max(55, 66) = 66


Locally Declared Labels
------------------------

ref: `Locally Declared Labels <https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Local-Labels.html#Local-Labels>`_

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    #define ARRAYSIZE(arr)                          \
      ({                                            \
            size_t size = 0;                        \
            size = sizeof(arr) / sizeof(arr[0]);    \
            size;                                   \
       })

    #define SEARCH(arr, size, target)           \
      ({                                        \
            __label__ found;                    \
            int i = 0;                          \
            int value = -1;                     \
            for (i = 0; i < size; i++) {        \
                    if (arr[i] == target) {     \
                            value = i;          \
                            goto found;         \
                    }                           \
            }                                   \
            value = -1;                         \
            found:                              \
            value;                              \
       })

    int main(int argc, char *argv[])
    {
            int arr[5] = {1, 2, 3, 9527, 5566};
            int target = 9527;

            printf("arr[%d] = %d\n",
                    SEARCH(arr, ARRAYSIZE(arr), target), target);
            return 0;
    }

    #endif

output:

.. code-block:: bash

    $ ./a.out
    arr[3] = 9527


Nested Functions
-----------------

ref: `Nested Functions <https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Nested-Functions.html#Nested-Functions>`_

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    int main(int argc, char *argv[])
    {
            double a = 3.0;
            double square(double x) { return x * x; }

            printf("square(%.2lf) = %.2lf\n", a, square(a));
            return 0;
    }
    #endif

output:

.. code-block:: bash

    $ ./a.out
    square(3.00) = 9.00

.. note::

    The nested function can access all the variables of the containing
    function that are visible at the point of its definition. This is
    called **lexical scoping**.

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    int main(int argc, char *argv[])
    {
            char *arr[5] = {"Hello", "World", "Foo", "Bar", NULL};
            char *ptr = NULL;
            int i = 0;
            int offset = 1;

            char *access(char **arr, int idx) {
                    return arr[idx + offset];
            }

            for (;;) {
                    ptr = access(arr, i++);
                    if (ptr != NULL) {
                            printf("str = %s\n", ptr);
                    } else {
                            break;
                    }
            }

        return 0;
    }
    #endif

.. note::

    It is possible to call the nested function from outside the scope of
    its name by storing its address or passing the address to another
    function.


.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    #define ARRAY_SIZE(arr) sizeof(arr) / sizeof(arr[0])
    void print_str(char **arr, int i, char *(*access)(char **arr, int idx))
    {
            char *ptr = NULL;

            if (arr == NULL) return;

            ptr = access(arr, i);
            if (ptr != NULL) {
                    printf("str = %s\n", ptr);
            }
    }

    int main(int argc, char *argv[])
    {
            char *arr[5] = {"Hello", "World", "Foo", "Bar", NULL};
            char *ptr = NULL;
            int i = 0;
            int offset = 1;

            char *access(char **arr, int idx) {
                    return arr[idx + offset];
            }

            for (i = 0; i < (ARRAY_SIZE(arr) - offset); i++) {
                    print_str(arr, i, access);
            }

        return 0;
    }
    #endif

output:

.. code-block:: bash

    $ ./a.out
    str = World
    str = Foo
    str = Bar


Referring to a Type with ``typeof``
-------------------------------------

ref: `Referring to a Type with typeof <https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Typeof.html#Typeof>`_


.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    #define pointer(T)  typeof(T *)
    #define array(T, N) typeof(T [N])

    int g_arr[5];

    int main(int argc, char *argv[])
    {
            int i = 0;
            char **ptr = NULL;

            /* This declares _val with the type of what ptr points to. */
            typeof (*g_arr) val = 5566;
            /* This declares _arr as an array of such values. */
            typeof (*g_arr) arr[3] = {1, 2,3};
            /* This declares y as an array of pointers to characters.*/
            array (pointer (char), 4) str_arr = {"foo", "bar", NULL};

            printf("val: %d\n", val);
            for (i = 0; i < 3; i++) {
                    printf("arr[%d] = %d\n", i, arr[i]);
            }
            for (i = 0, ptr = str_arr; *ptr != NULL ; i++, ptr++) {
                    printf("str_arr[%d] = %s\n", i, *ptr);
            }

            return 0;
    }
    #endif

output:

.. code-block:: bash

    $ ./a.out
    val: 5566
    arr[0] = 1
    arr[1] = 2
    arr[2] = 3
    str_arr[0] = foo
    str_arr[1] = bar
