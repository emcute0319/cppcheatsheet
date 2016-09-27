==================
C Macro cheatsheet
==================

ARRAYSIZE
----------

.. code-block:: c

    #include <stdio.h>

    #define ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))

    /*
     * Entry point
     */
    int main(int argc, char *argv[])                                                                                               
    {                                                                                                                              
        int ret = -1;                                                                                                              
        char *pszArr[] = {"Hello", "World", NULL};                                                                                 
                                                                                                                                   
        printf("array size: %lu\n", ARRAY_SIZE(pszArr));                                                                           
        ret = 0;                                                                                                                   
        return ret;                                                                                                                
    }

output:

.. code-block:: bash

    $ cc -g -Wall -o test test.c
    $ ./test
    array size: 3


FOREACH
--------

.. code-block:: c

    #include <stdio.h>

    #define FOREACH(item, arr) \                                                                                                   
        for (item=arr; *item; item++)

    /*
     * Entry point
     */
    int main(int argc, char *argv[])                                                                                               
    {                                                                                                                              
        int ret = -1;                                                                                                              
        char *pszArr[] = {"Hello", "World", NULL};                                                                                 
        char **str = NULL;                                                                                                         
                                                                                                                                   
        FOREACH (str, pszArr) {                                                                                                     
            printf("%s ", *str);                                                                                                   
        }                                                                                                                          
        printf("\n");                                                                                                              

        ret = 0;                                                                                                                   
        return ret;                                                                                                                
    }

output:

.. code-block:: bash

    $ cc -g -Wall -o test test.c
    $ ./test
    Hello World


lambda
-------

.. code-block:: c

    #define lambda(return_type, ...) \                                                                                             
        __extension__ \                                                                                                              
        ({ \                                                                                                                         
            return_type __fn__ __VA_ARGS__ \                                                                                           
            __fn__; \                                                                                                                  
        })

    /*
     * Entry point
     */
    int main(int argc, char *argv[])                                                                                               
    {                                                                                                                              
        int ret = -1;                                                                                                              
        int (*max) (int, int) =
            lambda (int, (int x, int y) { return x > y ? x : y; });                                            
                                                                                                                                   
        printf("lambda: %d\n", max(2,3));                                                                                          
                                                                                                                                   
        ret = 0;                                                                                                                   
        return ret;                                                                                                                
    }

output:

.. code-block:: bash

    $ gcc -g -Wall -o test test.c
    $ ./test
    lambda: 3


EXPECT_*
-----------

.. code-block:: c

    #include <stdio.h>                                                                                                                                   [19/1840]
    #include <string.h>
    #include <errno.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>

    #define EXPECT_TRUE(i, ...) \
        if (i != 1) { __VA_ARGS__ }

    #define EXPECT_FALSE(i, ...) \
        if (i != 0) { __VA_ARGS__ }

    #define EXPECT_EQ(i, e, ...) \
        if (i != e) { __VA_ARGS__ }

    #define EXPECT_NEQ(i, e, ...) \
        if (i == e) { __VA_ARGS__ }

    #define EXPECT_LT(i, e, ...) \
        if (i >= e) { __VA_ARGS__ }

    #define EXPECT_LE(i, e, ...) \
        if (i > e) { __VA_ARGS__ }

    #define EXPECT_GT(i, e, ...) \
        if (i <= e) { __VA_ARGS__ }

    #define EXPECT_GE(i, e, ...) \
        if (i < e) { __VA_ARGS__ }

    #define EXPECT_SUCCESS(ret, fmt, ...) \
        EXPECT_GT(ret, 0, \
            printf(fmt, ##__VA_ARGS__); \
            goto End; \
        )

    /*
     * Entry point
     */
    int main(int argc, char *argv[])
    {
        int ret = -1;

        EXPECT_TRUE(1);
        EXPECT_FALSE(0);
        EXPECT_LT(1, 0, printf("check less then fail\n"););
        EXPECT_GT(0, 1, printf("check great then fail\n"););
        EXPECT_SUCCESS(ret, "ret = %d\n", ret);
        ret = 0;
    End:
        return ret;
    }

output:

.. code-block:: bash

    $ cc -g -Wall -o checkerr checkerr.c
    $ ./checkerr
    check less then fail
    check great then fail
    ret = -1
