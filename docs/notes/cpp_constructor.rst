===========
constructor
===========

.. contents:: Table of Contents
    :backlinks: none


Constructors
------------

.. code-block:: cpp

    #include <iostream>
    #include <utility>

    class C {
     public:
      // constructor
      C(int x) : x_(x) {}

      // default constructor
      C() = default;

      // copy constructor
      C(const C &other) : C(other.x_) {
        std::cout << "copy constructor\n";
      }

      // copy assignment
      C &operator=(const C &other) {
        std::cout << "copy assignment\n";
        x_ = other.x_;
        return *this;
      }

      // move constructor
      C(C &&other) : x_(std::move(other.x_)) {
        std::cout << "move constructor\n";
        other.x_ = 0;
      }

      // move assignment
      C &operator=(C &&other) {
        std::cout << "move assignment\n";
        x_ = std::move(other.x_);
        return *this;
      }

     private:
      int x_;
    };

    int main(int argc, char *argv[]) {
      C c1;                   // call default constructor
      C c2(1);                // call constructor
      C c3 = C(2);            // call constructor
      C c4(c2);               // call copy constructor
      C c5(std::move(C(2)));  // call move constructor
      C c6 = c1;              // call copy constructor
      C c7 = std::move(C(2)); // call move constructor
      C c8 = std::move(c3);   // call move constructor

      C c9;
      C c10;

      c9 = c2;                // call copy assignment
      c10 = std::move(c4);    // call move assignment
      c10 = C(2);             // call move assignment
    }
