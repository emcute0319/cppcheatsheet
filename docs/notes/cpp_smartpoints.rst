============
Smart Points
============

Custom Deleters
---------------

.. code-block:: cpp

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <errno.h>
    #include <iostream>
    #include <string>
    #include <exception>
    #include <memory>

    using FilePtr = std::unique_ptr<FILE, int (*)(FILE *)>;

    constexpr void assert_that(bool statement, const char *msg) {
        if (!statement) {
            throw std::runtime_error(msg);
        }
    }

    int main(int argc, char *argv[]) {

        assert_that(argc == 2, "Usage: command [path]");

        FILE *f = nullptr;
        f = fopen(argv[1], "r+");
        assert_that(f, strerror(errno));

        // assign FILE* to a unique_ptr
        FilePtr fptr{f, fclose};
        assert_that(!!fptr, strerror(errno));
        assert_that(fseek(fptr.get(), 0, SEEK_END) == 0, strerror(errno));

        long size = ftell(fptr.get());
        assert_that(size >=0, strerror(errno));
        rewind(fptr.get());

        // using unique_ptr to create a buffer instead of using malloc
        std::unique_ptr<char[]> buf{ new char[size + 1]{0} };
        assert_that(!!buf, strerror(errno));

        size_t r = fread(buf.get(), 1, size, fptr.get());
        assert_that(r == size, "Reading error");
        std::cout << buf.get();
    end:
        return 0;
    }
