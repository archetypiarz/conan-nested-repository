cmake_minimum_required(VERSION 3.25)
project(some_binary)

add_executable(some_binary)

target_sources(some_binary
    PRIVATE
        main.cpp
)

# For some reason we dont add_subdirectory for that lib, and we dont link it.
# We just use its sources and headers.
target_sources(some_binary
    PRIVATE
        ../some_library/print.cpp
    PUBLIC
        FILE_SET print
        TYPE HEADERS
        BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/../some_library/include/
        FILES
            ../some_library/include/print.h
)

find_package(fmt CONFIG REQUIRED)
target_link_libraries(some_binary
    PRIVATE
        fmt::fmt
)
