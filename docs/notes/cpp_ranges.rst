======
Ranges
======

.. contents:: Table of Contents
    :backlinks: none

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

range-v3 - concat vectors
-------------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/view/concat.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> x{1, 5};
      std::vector<int> y{2, 8};
      std::vector<int> z{0, 3};
      auto r = ranges::views::concat(x, y, z);
      std::cout << ranges::views::all(r) << "\n";
      // [1,5,2,8,0,3]
    }

range-v3 - accumulate (sum)
---------------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/numeric/accumulate.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{1, 2, 3, 4, 5};
      const auto r = ranges::accumulate(v, 0);
      std::cout << r << "\n";
      // 15
    }

range-v3 - accumulate (reduce)
------------------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/numeric/accumulate.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{1, 2, 3, 4, 5};
      const auto r = ranges::accumulate(v, 1, [](auto &a, auto &b){
        return a + b;
      });
      std::cout << r << "\n";
      // 120
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

range-v3 - reverse sort
-----------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/action/sort.hpp>
    #include <range/v3/action/reverse.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{1, 5, 3, 2, 6};
      v |= ranges::actions::sort | ranges::actions::reverse;
      std::cout << ranges::views::all(v) << "\n";
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

range-v3 - split
----------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <string>
    #include <range/v3/view/c_str.hpp>
    #include <range/v3/action/split.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::string s = "hello c++";
      auto v = ranges::actions::split(s, ranges::views::c_str(" "));
      std::cout << ranges::views::all(v) << "\n";
      // [hello,c++]
    }

range-v3 - tokenize
-------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <string>
    #include <regex>
    #include <range/v3/view/tokenize.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      const std::string s = "hello cpp";
      const auto p = std::regex{"[\\w]+"};
      auto r = s | ranges::views::tokenize(p);
      std::cout << ranges::views::all(r) << "\n";
    }

range-v3 - join
---------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <string>
    #include <range/v3/core.hpp>
    #include <range/v3/view/join.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<std::string> v{"hello", "c++"};
      auto s = v | ranges::views::join(' ') | ranges::to<std::string>();
      std::cout << s << "\n";
    }

range-v3 - generate
-------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/view/generate.hpp>
    #include <range/v3/view/take.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      auto fib = ranges::views::generate([i=0, j=1]() mutable {
        int tmp = i; i+= j; j = i; return tmp;
      });

      auto v = fib | ranges::views::take(5);
      std::cout << ranges::views::all(v) << std::endl;
      // [0,1,2,4,8]
    }

range-v3 - take
---------------

.. code-block:: cpp

    #include <iostream>
    #include <range/v3/view/iota.hpp>
    #include <range/v3/view/take.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      auto v = ranges::views::iota(5, 10) | ranges::views::take(3);
      std::cout << ranges::views::all(v) << "\n";
      // [5,6,7]
    }

range-v3 - take_while
---------------------

.. code-block:: cpp

    #include <iostream>
    #include <range/v3/view/iota.hpp>
    #include <range/v3/view/take_while.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      auto v = ranges::views::iota(5, 10)
          | ranges::views::take_while([](auto &&x) { return x < 8; });
      std::cout << ranges::views::all(v) << "\n";
    }


range-v3 - drop
---------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/action/drop.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{1, 2, 3, 4, 5, 6};
      v |= ranges::actions::drop(3);
      std::cout << ranges::views::all(v) << "\n";
    }

range-v3 - drop_while
---------------------

.. code-block:: cpp

    #include <iostream>
    #include <range/v3/view/iota.hpp>
    #include <range/v3/view/drop_while.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      auto v = ranges::views::iota(5, 10)
          | ranges::views::drop_while([](auto &&x) { return x < 8; });
      std::cout << ranges::views::all(v) << "\n";
    }

range-v3 - cycle
----------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <range/v3/view/cycle.hpp>
    #include <range/v3/view/take.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::vector<int> v{1, 2, 3};
      auto r = v | ranges::views::cycle | ranges::views::take(6);
      std::cout << ranges::views::all(r) << "\n";
    }

range-v3 - keys
---------------

.. code-block:: cpp

    #include <iostream>
    #include <unordered_map>
    #include <range/v3/view/map.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::unordered_map<int, int> m{{9, 5}, {2, 7}};
      auto keys = m | ranges::views::keys;
      for (auto &&k : keys) {
        std::cout << k << "\n";
      }
    }

range-v3 - values
-----------------

.. code-block:: cpp

    #include <iostream>
    #include <unordered_map>
    #include <range/v3/view/map.hpp>
    #include <range/v3/view/all.hpp>

    int main(int argc, char *argv[]) {
      std::unordered_map<int, int> m{{9, 5}, {2, 7}};
      auto values = m | ranges::views::values;
      for (auto &&v : values) {
        std::cout << v << "\n";
      }
    }

range-v3 - cartesian_product
----------------------------

.. code-block:: cpp

    #include <iostream>
    #include <vector>
    #include <string>
    #include <range/v3/view/cartesian_product.hpp>

    int main(int argc, char *argv[]) {
      std::string x = "ab";
      std::vector<int> y{1, 2};
      auto r = ranges::views::cartesian_product(x, y);
      for (auto &&[a, b] : r) {
        std::cout << a << b << "\n";
      }
      // a1 a2 b1 b2
    }

c++20 range - iota
------------------

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

c++20 range - transform
-----------------------

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

c++20 range - filter
--------------------

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


c++20 range - split
-------------------

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

c++20 range - join
------------------

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
