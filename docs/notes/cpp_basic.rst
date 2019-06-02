====================
C++ Basic cheatsheet
====================

Reference
---------

.. code-block:: cpp

    #include <iostream>

    template<typename T>
    void f(T& param) noexcept {}
    // param is a reference

    int main(int argc, char *argv[])
    {
        int x = 123;
        const int cx = x;
        const int &rx = x;

        f(x);   // type(param) = int&
        f(cx);  // type(param) = const int&
        f(rx);  // type(param) = const int&

        return 0;
    }


.. code-block:: cpp

    #include <iostream>

    template<typename T>
    void f(T&& param) noexcept {}
    // param is a universal reference

    int main(int argc, char *argv[])
    {
        int x = 123;
        const int cx = x;
        const int &rx = x;

        f(x);   // x is a lvalue, type(param) = int&
        f(cx);  // cx is a lvalue, type(param) = const int&
        f(rx);  // rx is a lvalue, type(param) = const int&
        f(12);  // 12 is a rvalue, type(param) = int&&

        return 0;
    }

.. code-block:: cpp

    #include <iostream>

    template<typename T>
    void f(T param) noexcept {}
    // param is neither a pointer nor a reference.

    int main(int argc, char *argv[])
    {
        int x = 123;
        const int cx = x;
        const int &rx = x;

        f(x);   // type(param) = int
        f(cx);  // type(param) = int
        f(rx);  // type(param) = int
        f(12);  // type(param) = int

        return 0;
    }

auto
----

.. code-block:: cpp

    auto x = 123;        // type(x) = int
    const auto cx = x;   // type(cx) = const int
    const auto &rx = x;  // type(rx) = const int&

    auto &&urx = x;      // type(urx) = int&
    auto &&urcx = cx;    // type(urcx) = const int&
    auto &&urrx = rx;    // type(urrx) = const int&
    auto &&urrv = 12;    // type(urrv) = int&&
