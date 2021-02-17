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
