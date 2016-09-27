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


EXPECT_SUCCESS
---------------

.. code-block:: c

    #include <stdio.h>
    #include <string.h>
    #include <errno.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>


    #define EXPECT_SUCCESS(ret) \
        if (ret < 0) { \
            printf("error: %s\n", strerror(errno)); \
            goto End; \
        }

    /*
     * Entry point
     */
    int main(int argc, char *argv[])
    {
        int ret = -1;
        struct stat st = {};
        char *path = NULL;

        if (argc != 2) {
            printf("Usage: COMMAND [file]\n");
            goto End;
        }
        path = argv[1];

        EXPECT_SUCCESS(stat(path, &st));

        ret = 0;
    End:
        return ret;
    }

output:

.. code-block:: bash

    $ cc -g -Wall -o checkerr checkerr.c
    $ ./checkerr /etc/passwd
    $ ./checkerr /etc/passw
    error: No such file or directory
