=========
Container
=========

.. contents:: Table of Contents
    :backlinks: none

.. code-block:: cpp

    // profile.h
    #include <iostream>
    #include <chrono>

    using milliseconds = std::chrono::milliseconds;

    template <typename T, typename F>
    void profile(T &t, F &func) {
      const auto start = std::chrono::steady_clock::now();
      func(t);
      const auto end = std::chrono::steady_clock::now();
      const auto d = end - start;
      const auto mill = std::chrono::duration_cast<milliseconds>(d).count();
      std::cout << mill << " ms\n";
    }

Push Front
----------

.. code-block:: cpp

    // g++ -O3 -std=c++17 -Wall -Werror -I${HDR} a.cpp

    #include <vector>
    #include <deque>
    #include <list>
    #include <range/v3/view/iota.hpp>
    #include "profile.h"

    template <typename T>
    void insert(T &t) {
      for (auto i : ranges::views::iota(0, 300000)) {
        t.insert(t.begin(), i);
      }
    }

    int main(int argc, char *argv[]) {
      std::vector<int> v;
      std::deque<int> q;
      std::list<int> l;
      profile(v, insert<decltype(v)>);
      profile(q, insert<decltype(q)>);
      profile(l, insert<decltype(l)>);
    }

.. code-block:: bash

    $ ./a.out
    16045 ms
    1 ms
    6 ms


Push Back
---------

.. code-block:: cpp

    #include <vector>
    #include <deque>
    #include <list>
    #include <range/v3/view/iota.hpp>
    #include "profile.h"

    template <typename T>
    void insert(T &t) {
      for (auto i : ranges::views::iota(0, 1000000)) {
        t.push_back(i);
      }
    }

    int main(int argc, char *argv[]) {
      std::vector<int> v;
      std::deque<int> q;
      std::list<int> l;
      profile(v, insert<decltype(v)>);
      profile(q, insert<decltype(q)>);
      profile(l, insert<decltype(l)>);
    }

.. code-block:: bash

    ./a.out
    7 ms
    2 ms
    39 ms

Pop Front
---------

.. code-block:: cpp

    #include <vector>
    #include <deque>
    #include <list>
    #include <range/v3/view/iota.hpp>
    #include "profile.h"

    template <typename T>
    void insert(T &t) {
      for (auto i : ranges::views::iota(0, 300000)) {
        t.push_back(i);
      }
    }

    template <typename T>
    void pop_front(T &t) {
      while (!t.empty()) {
        t.pop_front();
      }
    }

    template <typename T>
    void erase(T &v) {
      while(!v.empty()) {
        v.erase(v.begin());
      }
    }

    int main(int argc, char *argv[]) {
      std::vector<int> v;
      std::deque<int> q;
      std::list<int> l;
      insert(v); insert(q); insert(l);
      profile(v, erase<decltype(v)>);
      profile(q, pop_front<decltype(q)>);
      profile(l, pop_front<decltype(l)>);
    }


.. code-block:: bash

    $ ./a.out
    22923 ms
    0 ms
    12 ms

Pop Back
--------

.. code-block:: cpp

    #include <vector>
    #include <deque>
    #include <list>
    #include <range/v3/view/iota.hpp>
    #include "profile.h"

    template <typename T>
    void insert(T &t) {
      for (auto i : ranges::views::iota(0, 1000000)) {
        t.push_back(i);
      }
    }

    template <typename T>
    void pop_back(T &t) {
      while (!t.empty()) {
        t.pop_back();
      }
    }

    int main(int argc, char *argv[]) {
      std::vector<int> v;
      std::deque<int> q;
      std::list<int> l;
      insert(v); insert(q); insert(l);
      profile(v, pop_back<decltype(v)>);
      profile(q, pop_back<decltype(q)>);
      profile(l, pop_back<decltype(l)>);
    }

.. code-block:: bash

    $ ./a.out
    0 ms
    0 ms
    30 ms


Position after Erasing
----------------------

.. code-block:: cpp

    // deque
	#include <iostream>
	#include <deque>
	#include <range/v3/view/all.hpp>

	int main(int argc, char *argv[]) {
	  std::deque<int> q{1, 2, 3, 4, 5};
	  auto it = q.begin() + 2;

	  std::cout << *it << "\n";
	  std::cout << ranges::views::all(q) << "\n";

	  q.erase(it);
	  std::cout << *it << "\n";
	  std::cout << ranges::views::all(q) << "\n";

	  // output
	  //   3
	  //   [1,2,3,4,5]
	  //   4
	  //   [1,2,4,5]
	}

.. code-block:: cpp

	#include <iostream>
	#include <vector>
	#include <range/v3/view/all.hpp>

	int main(int argc, char *argv[]) {
	  std::vector<int> v{1, 2, 3, 4, 5};
	  auto it = v.begin() + 2;

	  std::cout << *it << "\n";
	  std::cout << ranges::views::all(v) << "\n";

	  v.erase(it);
	  std::cout << *it << "\n";
	  std::cout << ranges::views::all(v) << "\n";

	  // output
	  //   3
	  //   [1,2,3,4,5]
	  //   4
	  //   [1,2,4,5]
	}


.. code-block:: cpp

	#include <iostream>
	#include <list>
	#include <range/v3/view/all.hpp>

	int main(int argc, char *argv[]) {
	  std::list<int> l{1, 2, 3, 4, 5};
	  auto it = l.begin();
	  ++it;

	  std::cout << *it << "\n";
	  std::cout << ranges::views::all(l) << "\n";

	  // Note that Iterators, pointers and references referring to elements
	  // removed by the function are invalidated. This is an example to show
	  // that an iterator do not point to the next element after erasing.
	  l.erase(it);
	  std::cout << *it << "\n";
	  std::cout << ranges::views::all(l) << "\n";
	  // output
	  //   2
	  //   [1,2,3,4,5]
	  //   2
	  //   [1,3,4,5]
	}
