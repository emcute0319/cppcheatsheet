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
