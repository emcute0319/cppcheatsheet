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
        ret = 0
    Error:
        if (s >= 0){
            close(s);
        }
        return ret;
    }

output:

.. code-block:: console

    $ ./a.out &
    [1] 63546
    $ nc localhost 5566
    Hello Socket
    Hello Socket


Event driven socket via ``select``
----------------------------------

.. code-block:: c

    #include <stdio.h>
    #include <string.h>
    #include <unistd.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <errno.h>

    #define BUF_SIZE 1024
    #define isvalidsock(s) (s > 0 ? 1 : 0)
    #define PORT 5566

    int socket_init(void)
    {
        struct sockaddr_in s_addr;
        int sfd = -1;
        int ret = -1;
        const int on = 1;

        bzero(&s_addr, sizeof(s_addr));
        s_addr.sin_family = AF_INET;
        s_addr.sin_addr.s_addr = htonl(INADDR_ANY);
        s_addr.sin_port = htons(PORT);

        sfd = socket(AF_INET, SOCK_STREAM, 0);
        if (!isvalidsock(sfd)) {
            printf("create socket error\n");
            goto Error;
        }
        if (0 > setsockopt(
                sfd, SOL_SOCKET, 
                SO_REUSEADDR, &on, sizeof(on))) {
            printf("setsockopt error\n");
            goto Error;
        }
        if (0 > bind(sfd,
                    (struct sockaddr *)&s_addr,
                    sizeof(s_addr))) {
            printf("bind error\n");
            goto Error;
        }
        if (0 > listen(sfd, 10)) {
            printf("listen network error\n"); 
            goto Error;
        } 
        ret = sfd; 
    Error:
        if (ret == -1) {
            if (sfd >=0) {
                close(sfd);
            }
        }
        return ret;
    }

    int main(int argc, char *argv[])
    {
        int ret = -1;
        int sfd = -1;
        int cfd = -1;
        ssize_t len = 0;
        struct sockaddr_in c_addr;
        int i = 0;
        int rlen = 0;
        char buf[BUF_SIZE] = {0};
        socklen_t clen = 0;
        fd_set wait_set;
        fd_set read_set;
       
        if (-1 == (sfd = socket_init())) {
            printf("socket_init error\n");
            goto Error;
        }
        FD_ZERO(&wait_set);
        FD_SET(sfd, &wait_set);
        for (;;) {
            read_set = wait_set;
            if (0 > select(FD_SETSIZE, &read_set,
                           NULL, NULL, NULL)) {
                printf("select get error\n"); 
                goto Error;
            }
            for (i=0; i < FD_SETSIZE; i++) {
                if (!FD_ISSET(i, &read_set)) {
                    continue;
                }
                if (i == sfd) {
                    clen = sizeof(c_addr);
                    cfd = accept(sfd,
                        (struct sockaddr *)&c_addr, &clen);
                    if (!isvalidsock(cfd)) {
                        goto Error; 
                    }
                    FD_SET(cfd, &wait_set);
                } else {
                    bzero(buf, BUF_SIZE);
                    if (0 > (rlen = read(i, buf, BUF_SIZE-1))) {
                        close(i);
                        FD_CLR (i, &wait_set);
                        continue;
                    }
                    if (0 > (rlen = write(i, buf, BUF_SIZE-1))) {
                        close(i);
                        FD_CLR (i, &wait_set);
                        continue;
                    }
                }
            }
        }    
        ret = 0;
    Error:
        if (sfd >= 0) {
            FD_CLR(sfd, &wait_set);
            close(sfd);
        }
        return ret;
    }

output: (bash 1)

.. code-block:: console

    $ ./a.out &
    [1] 64882
    Hello
    Hello

output: (bash 2)

.. code-block:: console

    $ nc localhost 5566
    Socket
    Socket
