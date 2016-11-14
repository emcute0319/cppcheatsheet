==================
C Basic cheatsheet
==================

Machine endian check
---------------------

.. code-block:: c

    #include <stdio.h>
    #include <stdint.h>

    static union {
        uint8_t buf[2];
        uint16_t uint16;
    } endian = { {0x00, 0x3a}};

    #define LITTLE_ENDIAN ((char)endian.uint16 == 0x00)
    #define BIG_ENDIAN ((char)endian.uint16 == 0x3a)



    int main(int argc, char *argv[])
    {
        uint8_t buf[2] = {0x00, 0x3a};

        if (LITTLE_ENDIAN) {
            printf("Little Endian Machine: %x\n", ((uint16_t *)buf)[0]);
        } else {
            printf("Big Endian Machine: %x\n", ((uint16_t *)buf)[0]);
        }

        return 0;
    }

output:

.. code-block:: bash

    # on little endian macheine
    $ ${CC} endian_check.c
    $ ./a.out
    Little Endian Machine: 3a00

    # on big endian machine
    $ ${CC} endian_check.c
    $ ./a.out
    Big Endian Machine: 3a


Implement closure via ``static``
--------------------------------

.. code-block:: c

    #include <stdio.h>

    void foo()
    {
        static int s_var = 9527;
        int l_var = 5566;

        l_var++;
        s_var++;
        printf("s_var = %d, l_var = %d\n", s_var, l_var);
    }

    int main(int argc, char *argv[])
    {
        int i = 0;
        for (i=0; i < 5; i++) {
            foo();
        }
        return 0;
    }

output:

.. code-block:: bash

    $ ./a.out
    s_var = 9528, l_var = 5567
    s_var = 9529, l_var = 5567
    s_var = 9530, l_var = 5567
    s_var = 9531, l_var = 5567
    s_var = 9532, l_var = 5567


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


Callback in C
--------------

.. code-block:: c

    #include <stdio.h>
    #include <string.h>
    #include <errno.h>
    #include <stdint.h>
    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>

    #define CHECK_ERR(ret, fmt, ...)        \
        do {                                \
            if (ret < 0) {                  \
                printf(fmt, ##__VA_ARGS__); \
                goto End;                   \
            }                               \
        } while(0)

    void callback(int err)
    {
        if (err < 0) {
            printf("run task fail!\n");
        } else {
            printf("run task success!\n");
        }
    }

    int task(const char *path ,void (*cb)(int err))
    {
        int ret = -1;
        struct stat st = {};

        ret = stat(path, &st);
        CHECK_ERR(ret, "stat(%s) fail. [%s]\n", path, strerror(errno));

        ret = 0;
    End:
        cb(ret); /* run the callback function */
        return ret;
    }


    int main(int argc, char *argv[])
    {
        int ret = -1;
        char *path = NULL;

        if (argc != 2) {
            printf("Usage: PROG [path]\n");
            goto End;
        }
        path = argv[1];
        task(path, callback);
        ret = 0;
    End:
        return ret;
    }

output:

.. code-block:: bash

    $ ${CC} example_callback.c
    $ ./a.out /etc/passwd
    run task success!
    $ ./a.out /etc/passw
    stat(/etc/passw) fail. [No such file or directory]
    run task fail!


Simple ``try ... catch`` in C
-------------------------------

.. code-block:: c

    /* cannot distinguish exception */

    #include <stdio.h>
    #include <setjmp.h>

    enum {
        ERR_EPERM = 1,
        ERR_ENOENT,
        ERR_ESRCH,
        ERR_EINTR,
        ERR_EIO
    };

    #define try    do { jmp_buf jmp_env__;     \
                        if (!setjmp(jmp_env__))
    #define catch       else
    #define end    } while(0)

    #define throw(exc) longjmp(jmp_env__, exc)

    int main(int argc, char *argv[])
    {
        int ret = 0;

        try {
            throw(ERR_EPERM);
        } catch {
            printf("get exception!\n");
            ret = -1;
        } end;
        return ret;
    }

output:

.. code-block:: bash

    $ ./a.out
    get exception!


Simple ``try ... catch(exc)`` in C
------------------------------------

.. code-block:: c

    #include <stdio.h>
    #include <string.h>
    #include <setjmp.h>

    enum {
        ERR_EPERM = 1,
        ERR_ENOENT,
        ERR_ESRCH,
        ERR_EINTR,
        ERR_EIO
    };

    #define try    do { jmp_buf jmp_env__;             \
                        switch ( setjmp(jmp_env__) ) { \
                            case 0:
    #define catch(exc)          break;                 \
                            case exc:
    #define end    } } while(0)

    #define throw(exc) longjmp(jmp_env__, exc)

    int main(int argc, char *argv[])
    {
        int ret = 0;

        try {
            throw(ERR_ENOENT);
        } catch(ERR_EPERM) {
            printf("get exception: %s\n", strerror(ERR_EPERM));
            ret = -1;
        } catch(ERR_ENOENT) {
            printf("get exception: %s\n", strerror(ERR_ENOENT));
            ret = -1;
        } catch(ERR_ESRCH) {
            printf("get exception: %s\n", strerror(ERR_ENOENT));
            ret = -1;
        } end;
        return ret;
    }

output:

.. code-block:: bash

    $ ./a.out
    get exception: No such file or directory


Simple ``try ... catch(exc) ... finally`` in C
-----------------------------------------------

.. code-block:: c

    #include <stdio.h>
    #include <string.h>
    #include <setjmp.h>

    enum {
        ERR_EPERM = 1,
        ERR_ENOENT,
        ERR_ESRCH,
        ERR_EINTR,
        ERR_EIO
    };

    #define try  do { jmp_buf jmp_env__  ;             \
                        switch ( setjmp(jmp_env__) ) { \
                            case 0: while(1) {
    #define catch(exc)  	break;                 \
                            case exc:
    #define finally         break; }                   \
                        default:
    #define end  } } while(0)

    #define throw(exc) longjmp(jmp_env__, exc)

    int main(int argc, char *argv[])
    {
        int ret = 0;

        try {
            throw(ERR_ENOENT);
        } catch(ERR_EPERM) {
            printf("get exception: %s\n", strerror(ERR_EPERM));
            ret = -1;
        } catch(ERR_ENOENT) {
            printf("get exception: %s\n", strerror(ERR_ENOENT));
            ret = -1;
        } catch(ERR_ESRCH) {
            printf("get exception: %s\n", strerror(ERR_ENOENT));
            ret = -1;
        } finally {
            printf("finally block\n");
        } end;
        return ret;
    }

output:

.. code-block:: bash

    $ ./a.out
    get exception: No such file or directory
    finally block

ref: `Exceptions in C with Longjmp and Setjmp <http://www.di.unipi.it/~nids/docs/longjump_try_trow_catch.html>`_
