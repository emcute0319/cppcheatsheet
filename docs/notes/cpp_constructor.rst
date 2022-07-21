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

Rule of three
-------------

.. code-block:: cpp

    #include <iostream>
    #include <memory>
    #include <string>
    #include <cstring>

    class RuleOfThree {
     public:
      RuleOfThree(const char *s, size_t n)
       : cstr_(new char[n])
       , n_(n) {
        memcpy(cstr_, s, n);
      }

      // if we have a user-defined destructor
      ~RuleOfThree() { delete[] cstr_; }
      // we need one a user-defined copy constructor
      RuleOfThree(const RuleOfThree &other)
        : RuleOfThree(other.cstr_, other.n_) {}
      // and user-defined copy assignment
      RuleOfThree &operator=(const RuleOfThree &other) {
        if (this == std::addressof(other)) {
          return *this;
        }
        delete[] cstr_;
        n_ = other.n_;
        cstr_ = new char[other.n_];
        memcpy(cstr_, other.cstr_, n_);
        return *this;
      }

      friend std::ostream &operator<<(std::ostream &os, const RuleOfThree &);

     private:
      char *cstr_;
      size_t n_;
    };

    std::ostream &operator<<(std::ostream &os, const RuleOfThree &r) {
      return os << r.cstr_;
    }

    int main(int argc, char *argv[]) {
      std::string s = "Rule of three";
      RuleOfThree r3(s.c_str(), s.size() + 1);
      std::cout << r3 << "\n";
    }


