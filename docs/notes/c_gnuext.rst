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
            int i = 0;

            void up(void) { i++; }
            printf("i = %d\n", i);
            up();
            printf("i = %d\n", i);
            up();
            printf("i = %d\n", i);

            return 0;
    }
    #endif

output:

.. code-block:: bash

    ./a.out
    i = 0
    i = 1
    i = 2


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

            char *access(char **arr, int idx)
            {
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


.. note::

    A nested function can jump to a label inherited from
    a containing function, provided the label is explicitly
    declared in the containing function.

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    int main(int argc, char *argv[])
    {
            __label__ end;
            int ret = -1, i = 0;

            void up(void)
            {
                    i++;
                    if (i > 2) goto end;
            }
            printf("i = %d\n", i); /* i = 0 */
            up();
            printf("i = %d\n", i); /* i = 1 */
            up();
            printf("i = %d\n", i); /* i = 2 */
            up();
            printf("i = %d\n", i); /* i = 3 */
            up();
            printf("i = %d\n", i); /* i = 4 */
            up();
            ret = 0;
    end:
            return ret;
    }
    #endif

output:

.. code-block:: bash

    $ ./a.out
    i = 0
    i = 1
    i = 2


.. note::

    If you need to declare the nested function before its
    definition, use ``auto`` (which is otherwise meaningless
    for function declarations).

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    int main(int argc, char *argv[])
    {
            int i = 0;
            auto void up(void);

            void up(void) { i++; }
            printf("i = %d\n", i); /* i = 0 */
            up();
            printf("i = %d\n", i); /* i = 1 */
            up();
            printf("i = %d\n", i); /* i = 2 */
            up();
            return 0;
    }
    #endif

output:

.. code-block:: bash

    $ ./a.out
    i = 0
    i = 1
    i = 2

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


Conditionals with Omitted Operands
-----------------------------------

ref: `Conditionals with Omitted Operands <https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Conditionals.html#Conditionals>`_

.. note::

    The middle operand in a conditional expression may be
    omitted. Then if the first operand is nonzero, its value
    is the value of the conditional expression.

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    int main(int argc, char *argv[])
    {
            int x = 1, y = 0;
            int z = -1;

            /* equivalent to x ? x : y */
            z = x ? : y;
            printf("z = %d\n", z);
            return 0;
    }

output:

.. code-block:: bash

    $ ./a.out
    z = 1


Arrays of Length Zero
----------------------

    ref: `Zero-length arrays <https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Zero-Length.html#Zero-Length>`_

.. note::

    Zero-length arrays are allowed in GNU C. They are very useful as the **last
    element** of a structure which is really a header for a **variable-length**
    object

.. code-block:: c

    #include <stdlib.h>
    #include <errno.h>
    #include <string.h>

    #define CHECK_NULL(ptr, fmt, ...)                   \
            do {                                        \
                    if (!ptr) {                         \
                            printf(fmt, ##__VA_ARGS__); \
                            goto End;                   \
                    }                                   \
            } while(0)

    /* array item has zero length */
    typedef struct _list {
            int len;
            char *item[0];
    } list;

    int main(int argc, char *argv[])
    {

            int ret = -1, len = 3;
            list *p_list = NULL;

            p_list = (list *)malloc(sizeof(list) + sizeof(char *) * len);
            CHECK_NULL(p_list, "malloc fail. [%s]", strerror(errno));

            p_list->item[0] = "Foo";
            p_list->item[1] = "Bar";
            p_list->item[2] = NULL;

            printf("item[0] = %s\n", p_list->item[0]);
            printf("item[1] = %s\n", p_list->item[1]);
            printf("item[2] = %s\n", p_list->item[2]);

            ret = 0;
    End:

            if (p_list)
                    free(p_list);

            return ret;
    }

    #endif

output:

.. code-block:: bash

    $ ./a.out
    item[0] = Foo
    item[1] = Bar
    item[2] = (null)


.. note::

    GCC allows static initialization of flexible array members

.. code-block:: c

    #ifndef __GNUC__
    #error "__GNUC__ not defined"
    #else

    #include <stdio.h>

    typedef struct _list {
            int len;
            int item[];
    } list;

    #define PRINT_LIST(l)                             \
            do {                                      \
                    int i = 0;                        \
                    for (i = 0; i < l.len; i++) {     \
                            printf("%d ", l.item[i]); \
                    }                                 \
                    printf("\n");                     \
            } while(0)

    int main(int argc, char *argv[])
    {
            static list l1 = {3, {1, 2, 3}};
            static list l2 = {5, {1, 2, 3, 4, 5}};

            PRINT_LIST(l1);
            PRINT_LIST(l2);
            return 0;
    }

    #endif

output:

.. code-block:: bash

    $ ./a.out
    1 2 3
    1 2 3 4 5


Variadic Macros
----------------

ref: `Variadic Macros <https://gcc.gnu.org/onlinedocs/gcc-4.1.2/gcc/Variadic-Macros.html#Variadic-Macros>`_

.. code-block:: c

    #include <stdio.h>

    #define DEBUG_C99(fmt, ...)     fprintf(stderr, fmt, ##__VA_ARGS__)
    #define DEBUG_GNU(fmt, args...) fprintf(stderr, fmt, ##args)

    int main(int argc, char *argv[])
    {
            DEBUG_C99("ISO C supported variadic macros\n");
            DEBUG_GNU("GNU C supported variadic macors\n");

            DEBUG_C99("ISO C format str = %s\n", "Foo");
            DEBUG_GNU("GNU C format str = %s\n", "Bar");

            return 0;
    }

output:

.. code-block:: bash

    $ ./a.out
    ISO C supported variadic macros
    GNU C supported variadic macors
    ISO C format str = Foo
    GNU C format str = Bar
