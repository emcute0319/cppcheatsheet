======
Ranges
======

.. contents:: Table of Contents
    :backlinks: none

Generate a Sequence
-------------------

.. code-block:: cpp

    // g++-10 -Wall -Werror -O3 -g --std=c++20 a.cc

    #include <iostream>
    #include <ranges>

    int main(int argc, char *argv[])
    {
      using namespace std::ranges;

      for (auto i : views::iota(1) | views::take(5)) {
        std::cout << i << std::endl;
      }
    }

Transform
---------

.. code-block:: cpp

    #include <iostream>
    #include <ranges>
    #include <vector>

    int main(int argc, char *argv[])
    {
      using namespace std::ranges;

      std::vector v{1, 2, 3};
      auto adaptor = views::transform([](auto &e) { return e * e; });
      for (auto i : v | adaptor) {
        std::cout << i << std::endl;
      }
    }

Filter
------

.. code-block:: cpp

    #include <iostream>
    #include <ranges>
    #include <vector>

    int main(int argc, char *argv[])
    {
      using namespace std::ranges;

      std::vector v{1, 2, 3};
      auto adaptor = views::filter([](auto &e) { return e % 2 == 0; });

      for (auto i : v | adaptor) {
        std::cout << i << std::endl;
      }
    }


Split
-----

.. code-block:: cpp

    #include <iostream>
    #include <ranges>
    #include <string>

    int main(int argc, char *argv[])
    {
      using namespace std::ranges;
      std::string s{"This is a string."};

      for (auto v : s | views::split(' ')) {
        std::string w;
        for (auto &c : v) {
          w += c;
        }
        std::cout << w << std::endl;
      }
    }

Join
----

.. code-block:: cpp

    #include <iostream>
    #include <ranges>
    #include <vector>
    #include <string>

    int main(int argc, char *argv[])
    {
      using namespace std::ranges;
      std::vector<std::string> v{"This", " ", "is", " ", "a", " ", "string."};
      std::string s;
      for (auto &c : v | views::join) {
        s += c;
      }
      std::cout << s << std::endl;
    }

range-v3 - debug a vector
-------------------------

.. code-block:: cpp

    // g++ -O3 -std=c++17 -Wall -Werror -I${HDR} a.cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{5, 4, 3, 2, 1, 1, 1};
      std::cout << ranges::views::all(v) << "\n";
      // [5,4,3,2,1,1,1]
    }

range-v3 - slice
----------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/algorithm/copy.hpp>
    #include <range/v3/action/slice.hpp>
    #include <range/v3/view/slice.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> x{5, 4, 3, 2, 1};

      auto y = x | ranges::copy | ranges::actions::slice(1, 3);
      std::cout << ranges::views::all(y) << "\n";
      // [4,3]

      for (auto &&e : x | ranges::views::slice(2, 4)) {
        std::cout << e << "\n";
      }
    }

range-v3 - enumerate
--------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/view/enumerate.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{5, 4, 3, 2, 1, 1, 1};
      for (auto &&[i, e] : v |  ranges::views::enumerate) {
        std::cout << i << ", " << e << "\n";
      }
    }

range-v3 - sort
---------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/action/sort.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{5, 4, 3, 2, 1, 1, 1};
      v |= ranges::actions::sort;
      std::cout << ranges::views::all(v) << "\n";
      // [1,1,1,2,3,4,5]
    }

range-v3 - sort & uniqe
-----------------------

.. code-block:: cpp

    // echo 5 4 3 2 1 1 1 | tr -s " " "\n" | sort | uniq

    #include <iostream>
    #include <vector>
    #include <range/v3/action/unique.hpp>
    #include <range/v3/action/sort.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{5, 4, 3, 2, 1, 1, 1};
      v |= ranges::actions::sort | ranges::actions::unique;
      std::cout << ranges::views::all(v) << "\n";
      // [1,2,3,4,5]
    }

range-v3 - zip
--------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/view/zip.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> x{5, 4, 3, 2};
      std::vector<int> y{1, 2, 3 ,4};

      for (auto &&[a, b] : ranges::views::zip(x, y)) {
        std::cout << a << " " << b << "\n";
      }
    }
