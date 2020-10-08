==========================
Data Structure & Algorithm
==========================

.. contents:: Table of Contents
    :backlinks: none

``std::map`` sort by key
------------------------

.. code-block:: cpp

    // g++ -std=c++17 -Wall -Werror -O3 a.cc

    #include <iostream>
    #include <map>

    int main(int argc, char *argv[])
    {
      // ascending
      std::map<int, int, std::less<int>> a{{3, 3}, {2, 2}, {1, 1}};
      // descending
      std::map<int, int, std::greater<int>> d{{3, 3}, {2, 2}, {1, 1}};

      auto print = [](auto &m) {
        for (const auto &[k, v] : m) {
          std::cout << k << " " << v << "\n";
        }
      };
      print(a); // 1, 2, 3
      print(d); // 3, 2, 1
    }

``std::map`` with object as key
-------------------------------

.. code-block:: cpp

    #include <iostream>
    #include <map>

    struct Data {
      int a;
      int b;
    };

    int main(int argc, char *argv[])
    {
      auto cmp = [](auto &x, auto &y) { return x.a < y.b; };
      std::map<Data, int, decltype(cmp)> m{cmp};
      m[Data{1, 2}] = 1;
      m[Data{3, 4}] = 4;

      for (const auto &[k, v] : m) {
        std::cout << k.a << " " << k.b << " " << v << "\n";
      }
    }

