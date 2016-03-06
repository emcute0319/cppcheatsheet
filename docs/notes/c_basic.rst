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


Get lines of a file
-------------------

.. code-block:: c

    // basic API: fopen, getline

    #include <stdio.h>
    #include <stdlib.h>

    int main(int argc, char *argv[])
    {
        int ret = -1;
        FILE *f = NULL;
        ssize_t read_size = 0;
        size_t len = 0;
        char *path = NULL;
        char *line = NULL;

        if (argc != 2) {
            printf("Usage: PROG file\n");
            goto Error;
        }

        path = argv[1];
        if (NULL == (f = fopen(path, "r"))) {
            printf("Read file error");
            goto Error;
        }

        while (-1 != getline(&line, &len, f)) {
            printf("%s\n", line);
        }
        ret = 0;
    Error:
        if (line) {
            free(line);
            line = NULL;
        }
        if (f) {
            fclose(f);
        }
        return ret;
    }


Read content into memory from a file
------------------------------------

.. code-block:: c

    // basick API: fopen, fseek, ftell, rewind, fread
    #include <stdio.h>
    #include <stdlib.h>

    int main(int argc, char *argv[])
    {
        int ret = -1;
        FILE *f = NULL;
        char *path = NULL;
        int size = 0;
        int read_size = 0;
        char *buffer = NULL;

        if (argc != 2) {
            printf("Usage: PROG file\n");
            goto Error;
        }

        path = argv[1];
        if (NULL == (f = fopen(path, "r"))) {
            printf("Read %s into memory fail\n", path);
            goto Error;
        }
        fseek(f, 0, SEEK_END);
        size = ftell(f);
        rewind(f);

        if (NULL == (buffer = (char *)calloc(size, sizeof(char)))) {
            printf("malloc file fail\n");
            goto Error;
        }

        read_size = fread(buffer, 1, size, f);
        if (read_size != size) {
            printf("fread %s fail\n", path);
            goto Error;
        }
        buffer[size-1] = '\0';
        printf("%s\n", buffer);
        ret = 0;
    Error:
        if (buffer) {
            free(buffer);
            buffer = NULL;
        }
        if (f) {
            fclose(f);
        }
        return ret;
    }
