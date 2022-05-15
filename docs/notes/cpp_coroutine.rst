=========
coroutine
=========

.. contents:: Table of Contents
    :backlinks: none

Generator
---------

.. code-block:: cpp

    // g++ -O3 -std=c++20 -Wall -Werror co.cc

    #include <iostream>
    #include <coroutine>

    template <typename T>
    class generator {
    public:
      struct promise_type;
      using handle_type = std::coroutine_handle<promise_type>;
      handle_type h_;

      struct promise_type {
        T value_;
        std::exception_ptr exception_;
        generator<T> get_return_object() {
          return { handle_type::from_promise(*this) };
        }
        void unhandled_exception() { exception_ = std::current_exception(); }
        void return_void() {}
        std::suspend_always initial_suspend() noexcept { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }
        std::suspend_always yield_value(T v) noexcept {
          value_ = std::move(v);
          return {};
        }
      };

    public:

      generator(handle_type h) : h_(h) {}
      ~generator() { h_.destroy(); }
      explicit operator bool() {
        next();
        return !h_.done();
      }

      T operator() () {
        next();
        cached_ = false;
        return std::move(h_.promise().value_);
      }

    private:
      bool cached_ = false;
      void next() {
        if (cached_) {
          return;
        }
        h_();
        if (h_.promise().exception_) {
          std::rethrow_exception(h_.promise().exception_);
        }
        cached_ = true;
      }
    };

    generator<uint64_t> fib(uint64_t n) {
      uint64_t a = 0, b = 1;
      for (uint64_t i = 0; i <= n; ++i) {
        co_yield a;
        uint64_t t = b;
        b = a + b;
        a = t;
      }
    }

    int main(int argc, char *argv[]) {
      auto g = fib(10);
      while (g) {
        std::cout << g() << " ";
      }
      // ./a.out
      //  0 1 1 2 3 5 8 13 21 34 55
    }
