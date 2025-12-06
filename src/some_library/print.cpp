#include "print.h"
#include <iostream>
namespace some_library {
    void print(std::string_view textToPrint) {
        std::cout << textToPrint << "\n"; 
    }
}
