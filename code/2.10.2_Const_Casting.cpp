#include <iostream>

void f(const int &x) { const_cast<int &>(x) = 0; }

int main(int argc, char *argv[]) {
  int x = 123;
  f(x);
  std::cout << x << "\n";
}