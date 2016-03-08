=============================
C signal operation cheatsheet
=============================

Print signal expression
-----------------------

.. code-block:: c

    #include <stdio.h>
    #include <signal.h>

    #define ARRAYLEN(arr) sizeof(arr) / sizeof((arr)[0])

    static int signo_arr[] = {
        SIGABRT , SIGALRM  , SIGBUS, 
        SIGCHLD , SIGCONT  , SIGFPE,
        SIGHUP  , SIGILL   , SIGINT,
        SIGIO   , SIGKILL  , SIGPIPE,
        SIGPROF , SIGQUIT  , SIGSEGV,
        SIGSYS  , SIGTERM  , SIGTRAP, 
        SIGTSTP , SIGTTIN  , SIGTTOU,
        SIGURG  , SIGVTALRM, SIGUSR1,
        SIGUSR2 , SIGXCPU  , SIGXFSZ
    };

    int main(int argc, char *argv[])
    {
        int i = 0; 
        int signo = -1;
        char *msg = "SIGNAL";

        for (i=0; i < ARRAYLEN(signo_arr); i++) {
            signo = signo_arr[i];
            printf("Signal[%d]: %s\n", signo, sys_siglist[signo]);
        }

        return 0;
    }

output:

.. code-block:: console

    $ ./a.out
    Signal[6]: Abort trap
    Signal[14]: Alarm clock
    Signal[10]: Bus error
    Signal[20]: Child exited
    Signal[19]: Continued
    Signal[8]: Floating point exception
    Signal[1]: Hangup
    Signal[4]: Illegal instruction
    Signal[2]: Interrupt
    Signal[23]: I/O possible
    Signal[9]: Killed
    Signal[13]: Broken pipe
    Signal[27]: Profiling timer expired
    Signal[3]: Quit
    Signal[11]: Segmentation fault
    Signal[12]: Bad system call
    Signal[15]: Terminated
    Signal[5]: Trace/BPT trap
    Signal[18]: Suspended
    Signal[21]: Stopped (tty input)
    Signal[22]: Stopped (tty output)
    Signal[16]: Urgent I/O condition
    Signal[26]: Virtual timer expired
    Signal[30]: User defined signal 1
    Signal[31]: User defined signal 2
    Signal[24]: Cputime limit exceeded
    Signal[25]: Filesize limit exceeded


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
