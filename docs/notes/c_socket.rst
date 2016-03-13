===================
C socket cheatsheet
===================

Check local machine endian
--------------------------

.. code-block:: c

    #include <stdio.h>
    #include <stdlib.h>

    int main(int argc, char *argv[])
    {
        uint32_t x = 0x12345678;
        unsigned char *xp = NULL; 

        xp = (unsigned char *) &x;
        printf("%0x %0x %0x %0x\n",
            xp[0], xp[1], xp[2], xp[3]);
        return 0;
    }

output: (from a little endian machine)

.. code-block:: console

    $ ./a.out 
    78 56 34 12

Basic socket server
-------------------

.. code-block:: c

    #include <stdio.h>
    #include <string.h>
    #include <unistd.h>
    #include <sys/socket.h>
    #include <netinet/in.h>

    #define BUF_SIZE 1024
    #define isvalidsock(s) (s > 0 ? 1 : 0 )

    static int port = 5566;

    int main(int argc, char *argv[])
    {
        int ret = -1;
        int s = -1;
        int c = -1;
        socklen_t clen = 0;
        ssize_t len = 0;
        struct sockaddr_in s_addr;
        struct sockaddr_in c_addr;
        const int on = 1;
        char buf[BUF_SIZE] = {0};
        
        /* set socket host and port */
        bzero(&s_addr, sizeof(s_addr));
        s_addr.sin_family = AF_INET;
        s_addr.sin_addr.s_addr = htonl(INADDR_ANY);
        s_addr.sin_port = htons(port);    

        /* create socket */
        s = socket(AF_INET, SOCK_STREAM, 0);
        if (!isvalidsock(s)) {
            printf("Create socket fail\n");
            goto Error;
        }
        /* set sockopt */
        if (0 > setsockopt(s, SOL_SOCKET, 
                SO_REUSEADDR, &on, sizeof(on))) {
            printf("setsockopt fail\n");
            goto Error;
        }
        /* bind address and port */
        if (0 > bind(s, (struct sockaddr *) &s_addr,
                sizeof(s_addr))) {
            printf("bind socket fail\n");
            goto Error;
        }
        /* listen */
        if (0 > listen(s, 10)) {
            printf("listen fail\n");
            goto Error;
        }
        for(;;) {
            clen = sizeof(c_addr);
            c = accept(s, (struct sockaddr *)&c_addr, &clen);    
            if (!isvalidsock(c)) {
                printf("accept error\n");
                continue;
            }
            bzero(buf, BUF_SIZE);
            if (0 > (len = recv(c, buf, BUF_SIZE-1, 0))) {
                close(c);
            }   
            send(c, buf, BUF_SIZE-1, 0);
            close(c); 
        }
    Error:
        return ret;
    }

.. code-block:: console

    $ ./a.out &
    [1] 63546
    $ nc localhost 5566
    Hello Socket
    Hello Socket
