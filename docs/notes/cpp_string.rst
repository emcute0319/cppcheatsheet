======
String
======


Split a String
--------------

.. code-block:: cpp

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
