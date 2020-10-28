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

``std::foreach``
----------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main(int argc, char *argv[])
    {
      std::vector v{1, 2, 3};
      std::for_each(v.begin(), v.end(), [](auto &i) { i = i * 2; });
      std::for_each(v.begin(), v.end(), [](auto &i) { std::cout << i << "\n"; });
    }

``std::find``
-------------

``std::find`` returns an iterator to the first element in an array like object.

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main(int argc, char *argv[])
    {
      std::vector v{1, 2, 3};

      // complexity O(n)
      auto it = std::find(v.begin(), v.end(), 2);
      std::cout << *it << "\n";
    }

``std::find_if`` & ``std::find_if_not``
---------------------------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main(int argc, char *argv[])
    {
      std::vector v{1, 2, 3};
      auto x = find_if(v.begin(), v.end(), [](auto &i) { return i == 2; });
      std::cout << *x << "\n";

      auto y = find_if_not(v.begin(), v.end(), [](auto &i) { return i == 2; });
      std::cout << *y << "\n";
    }

``std::transform``
------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <algorithm>

    int main(int argc, char *argv[])
    {
      std::string s = "Hello World";

      // transform elements in place
      std::transform(s.begin(), s.end(), s.begin(), ::toupper);
      std::cout << s << "\n";

      // transform elements and store in another object
      std::string o(s.size(), 0);
      std::transform(s.begin(), s.end(), o.begin(), ::tolower);
      std::cout << o << "\n";
    }

