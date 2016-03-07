==================
C Basic cheatsheet
==================

Split String
------------

.. code-block:: c

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <assert.h>

    char ** split(char *str, const int sep)
    {
        int num_cut = 1;
        int i = 0;
        char **buf = NULL;
        char *ptr = NULL;
        char delimiters[2] ={sep, '\0'};

        assert(str != NULL);
        printf("pattern = %s\n",str);
        for (ptr = str; *ptr != '\0'; ptr++) {
            if (*ptr == sep){ num_cut++; }
        }
        num_cut++;

        if (NULL == (buf = (char **)calloc(num_cut, sizeof(char *)))) {
            printf("malloc fail\n");
            goto Error;
        }

        ptr = strtok(str, delimiters);
        while (ptr != NULL) {
           buf[i++] = strdup(ptr); 
           ptr = strtok(NULL, delimiters);
        }
    Error:
        return buf;
    }

    void free_strlist(char **buf)
    {
        char **ptr = NULL;
        for (ptr = buf; *ptr; ptr++) {
            free(*ptr); 
        }
    }

    int main(int argc, char *argv[])
    {
        int ret = -1;
        char *pattern = NULL;
        char **buf = NULL;
        char **ptr = NULL;

        if (argc != 2) {
            printf("Usage: PROG string\n");
            goto Error;
        }

        pattern = argv[1];
        buf = split(pattern, ',');
        for (ptr = buf; *ptr; ptr++) {
            printf("%s\n",*ptr);
        } 
        ret = 0;
    Error:
        if (buf) {
            free_strlist(buf);
            buf = NULL;
        }
        return ret;
    }

output:

.. code-block:: console

    $ ./a.out hello,world
    pattern = hello,world
    hello
    world
