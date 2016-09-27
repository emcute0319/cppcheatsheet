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
