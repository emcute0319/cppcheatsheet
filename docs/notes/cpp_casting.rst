=======
Casting
=======

.. contents:: Table of Contents
    :backlinks: none

C Style Casting
---------------

Const Casting
-------------

Reinterpret Casting
-------------------

Static Casting
--------------

.. code-block:: cpp

    #include <iostream>
    #include <memory>

    struct A {
      virtual void f() { std::cout << __func__ << "\n"; }
      virtual ~A() = default;
    };

    struct B : public A {;
      B(int *x) : x_{x} {}
      int *g() { return x_; }
      int *x_;
    };

    int main(int argc, char *argv[]) {
      auto a = std::make_unique<A>();
      // downcasting may be dangerous
      auto b = static_cast<B *>(a.get());
      auto x = b->g();
      std::cout << *x << "\n";
    }

Dynamic Casting
---------------

.. code-block:: cpp

    #include <iostream>
    #include <memory>

    struct A {
      virtual void f() { std::cout << __func__ << "\n"; }
    };

    struct B : public A {
       void f() override { std::cout << __PRETTY_FUNCTION__ << "\n"; }
    };

    int main(int argc, char *argv[]) {
      auto a = std::make_unique<A>();
      auto b = std::make_unique<B>();

      // downcast
      auto bb = dynamic_cast<B *>(a.get());
      std::cout << "Is dynamic_cast(*a) to *b success? " << !!bb << "\n";
      // output: Is dynamic_cast(*a) to *b success? 0

      // upcast
      auto aa = dynamic_cast<A *>(b.get());
      std::cout << "Is dynamic_cast(*b) to *a success? " << !!aa << "\n";
      // output: Is dynamic_cast(*a) to *b success? 1
    }

