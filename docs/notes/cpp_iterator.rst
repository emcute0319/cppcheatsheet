========
Iterator
========

Iterate an Internal Vector
--------------------------

.. code-block:: cpp

    #include <iostream>
    #include <utility>
    #include <vector>

    template<typename T>
    class Vector {
    public:
        using iterator = typename std::vector<T>::iterator;
        using const_iterator = typename std::vector<T>::const_iterator;

        inline iterator begin() noexcept {return v.begin();}
        inline iterator end() noexcept {return v.end();}
        inline const_iterator cbegin() const noexcept {return v.cbegin();}
        inline const_iterator cend() const noexcept {return v.cend();}

        template<class... Args>
        auto emplace_back(Args&&... args) {
            return v.emplace_back(std::forward<Args>(args)...);
        }
    private:
        std::vector<T> v;
    };


    int main(int argc, char *argv[]) {

        Vector<int> v;
        v.emplace_back(1);
        v.emplace_back(2);
        v.emplace_back(3);

        for (auto &it : v) {
            std::cout << it << std::endl;
        }
        return 0;
    }
