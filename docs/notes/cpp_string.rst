======
String
======

.. contents:: Table of Contents
    :backlinks: none

Char to a string
----------------

.. code-block:: cpp

    #include <string>

    int main(int argc, char *argv[]) {
      // string(size_t n, char c)
      std::string a(1, 'a');
    }

.. code-block:: cpp

    #include <string>

    int main(int argc, char *argv[]) {
      std::string s;
      s += 'a';
    }

.. code-block:: cpp

    #include <string>

    int main(int argc, char *argv[]) {
      std::string s;
      s = 'a';
    }

C String to a String
--------------------

.. code-block:: cpp

    #include <string>

    int main(int argc, char *argv[]) {
      char cstr[] = "hello cstr";
      std::string s = cstr;
    }

Split a String
--------------

.. code-block:: cpp

    // $ g++ --std=c++14 -Wall -Werror -g -O3 split.cpp
    // $ ./a.out
    // abc
    // def
    // ghi

    #include <iostream>
    #include <string>
    #include <vector>

    using namespace std;

    vector<string> split(const string &str, char delimeter) {

        string s = str;
        vector<string> out;
        size_t pos = 0;

        while((pos = s.find(delimeter)) != string::npos) {
            string token = s.substr(0, pos);
            out.emplace_back(token);
            s.erase(0, pos + 1);
        }
        out.emplace_back(s);
        return out;
    }

    int main(int argc, char *argv[]) {

        string s = "abc,def,ghi";
        vector<string> v = split(s, ',');
        for (const auto &c : v) {
            cout << c << "\n";
        }
    }

Using istream

.. code-block:: cpp

    #include <iostream>
    #include <sstream>
    #include <string>
    #include <vector>

    using namespace std;

    template<char delimiter>
    class String : public string
    {
        friend istream &operator>>( istream  &is, String &out) {
            std::getline(is, out, delimiter);
            return is;
        }
    };

    int main(int argc, char *argv[]) {
        std::string text = "abc,def,ghi";

        istringstream iss(text);
        vector<string> out((istream_iterator<String<','>>(iss)),
                            istream_iterator<String<','>>());

        for (const auto &c : out) {
            cout << c << "\n";
        }
    }



Using ``std::getline``

.. code-block:: cpp

    #include <iostream>
    #include <sstream>
    #include <string>
    #include <vector>

    using namespace std;

    int main(int argc, char *argv[])
    {
        string in = "abc,def,ghi";
        vector<string> out;
        string token;
        std::istringstream stream(in);

        while (std::getline(stream, token, ',')) {
            out.emplace_back(token);
        }
        for (const auto &c : out) {
            cout << c << "\n";
        }
    }

Using boost

.. code-block:: cpp

    #include <iostream>
    #include <string>
    #include <vector>
    #include <boost/algorithm/string.hpp>

    using namespace std;

    int main(int argc, char *argv[]) {
        string in = "abc,def,ghi";
        vector<string> out;

        boost::split(out, in, [](char c) { return c == ','; });
        for (const auto &s : out) {
            cout << s << "\n";
        }
    }

Upper & Lower
-------------

.. code-block:: cpp

    // cc -std=c++17 -Wall -Werror -O3 a.cpp

    #include <iostream>
    #include <string>
    #include <algorithm>

    int main(int argc, char *argv[])
    {
      std::string s = "Hello World";
      // to upper
      std::transform(s.begin(), s.end(), s.begin(), ::toupper);
      std::cout << s << "\n";

      // to lower
      std::transform(s.begin(), s.end(), s.begin(), ::tolower);
      std::cout << s << "\n";
    }
