=============================
C signal operation cheatsheet
=============================

Basic signal event handler 
--------------------------

.. code-block:: c

    #include <stdio.h>
    #include <string.h>
    #include <signal.h>
    #include <errno.h>
    #include <sys/types.h>
    #include <unistd.h>

    /** singal handler prototype :
     * 
     *  type void (*sighandler_t) (int)
     */

    void sig_handler(int signo)
    {
        printf("[%d] Get signal: %s\n", getpid(), strsignal(signo));
    }

    int main(int argc, char *argv[])
    {
        int ret = -1;
        
        /* overwrite default signal handler */
        if (SIG_ERR == signal(SIGHUP, sig_handler)) {
            printf("Get error: %s\n", strerror(errno));
            goto Error;
        }
        if (SIG_ERR == signal(SIGINT, sig_handler)) {
            printf("Get error: %s\n", strerror(errno));
            goto Error;
        }
        if (SIG_ERR == signal(SIGALRM, sig_handler)) {
            printf("Get error: %s\n", strerror(errno));
            goto Error;
        }
        /* ignore signal */
        if (SIG_ERR == signal(SIGUSR1, SIG_IGN)) {
            printf("Get error: %s\n", strerror(errno));
            goto Error;
        }
        while(1) { sleep(3); }
        ret = 0;
    Error:
        return ret;
    }

output:

.. code-block:: console

    $ ./a.out 
    ^C[54652] Get signal: Interrupt: 2
    [54652] Get signal: Hangup: 1
    [54652] Get signal: Alarm clock: 14
