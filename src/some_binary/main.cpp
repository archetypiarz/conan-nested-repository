#include "print.h"
#include <fmt/format.h>

int main(int args, char **argv) {
  some_library::print(fmt::format("Hello world from {} app!", argv[0]));
  return 0;
}
