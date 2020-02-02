===============================
Return Value Optimization (RVO)
===============================

.. code-block:: cpp

    #include <iostream>

    struct Foo {
        Foo() { std::cout << "Constructor" << "\n"; }
        ~Foo() { std::cout << "Destructor" << "\n"; }
        Foo(const Foo&) { std::cout << "Copy Constructor" << "\n"; }
        Foo(Foo &&) { std::cout << "Move Constructor" << "\n"; }
        Foo& operator=(const Foo&) {
            std::cout << "Copy Assignment" << "\n";
            return *this;
        }
        Foo& operator=(Foo &&){
            std::cout << "Move Assignment" << "\n";
            return *this;
        }
    };

    Foo FooRVO() {
        return Foo();
    }

    int main(int argc, char *argv[]) {
        Foo f = FooRVO();
        return 0;
    }
