====
Time
====

Timestamp
---------

.. code-block:: cpp

    // g++ -std=c++17 -Wall -Werror -O3 a.cc

    #include <iostream>
    #include <chrono>

    using milliseconds = std::chrono::milliseconds;
    namespace chrono = std::chrono;

    int main(int argc, char *argv[])
    {
      auto now = std::chrono::system_clock::now();
      auto t = now.time_since_epoch();
      std::cout << chrono::duration_cast<milliseconds>(t).count() << "\n";
    }

Profiling
---------

.. code-block:: cpp

    #include <iostream>
    #include <chrono>

    #include <unistd.h>

    using milliseconds = std::chrono::milliseconds;
    namespace chrono = std::chrono;

    int main(int argc, char *argv[])
    {
      auto start = std::chrono::steady_clock::now();
      sleep(3);
      auto end = std::chrono::steady_clock::now();
      auto d = end - start;
      std::cout << chrono::duration_cast<milliseconds>(d).count() << "\n";
    }

Literals
--------

.. code-block:: cpp

    #include <iostream>
    #include <chrono>

    using ms = std::chrono::milliseconds;
    namespace chrono = std::chrono;

    int main(int argc, char *argv[])
    {
      using namespace std::literals;
      auto t = 1602207217323ms;
      std::cout << std::chrono::duration_cast<ms>(t).count() << "\n";
    }

Format Time
-----------

.. code-block:: cpp

    #include <iostream>
    #include <iomanip>
    #include <ctime>
    #include <stdlib.h>

    int main(int argc, char *argv[])
    {
      std::time_t t = std::time(nullptr);
      constexpr char fmt[] = "%c %Z";
      std::cout << "UTC " << std::put_time(std::gmtime(&t), fmt) << "\n";
      std::cout << "Local " << std::put_time(std::localtime(&t), fmt) << "\n";

      std::string tz = "America/Chicago";
      putenv(tz.data());
      std::cout << "Chicago " << std::put_time(std::localtime(&t), fmt) << "\n";
    }

To ``time_t``
-------------

.. code-block:: cpp

    #include <iostream>
    #include <iomanip>
    #include <chrono>
    #include <ctime>

    namespace chrono = std::chrono;

    int main(int argc, char *argv[])
    {
      auto now = chrono::system_clock::now();
      std::time_t t = std::chrono::system_clock::to_time_t(now);
      std::cout << std::put_time(std::gmtime(&t), "%FT%TZ") << "\n";
    }

ISO 8601 format
---------------

.. code-block:: cpp

    #include <iostream>
    #include <iomanip>
    #include <chrono>
    #include <ctime>

    namespace chrono = std::chrono;

    int main(int argc, char *argv[])
    {
      auto now = chrono::system_clock::now();
      std::time_t t = std::chrono::system_clock::to_time_t(now);
      std::cout << std::put_time(std::gmtime(&t), "%Y-%m-%dT%H:%M:%SZ") << "\n";
      std::cout << std::put_time(std::gmtime(&t), "%FT%TZ") << "\n";
      std::cout << std::put_time(std::gmtime(&t), "%FT%TZ%z") << "\n";
    }
