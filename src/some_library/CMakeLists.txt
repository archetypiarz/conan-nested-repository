add_library(STATIC some_library)

target_sources(some_library
    PRIVATE
        print.cpp
    PUBLIC
        FILE_SET print
        TYPE HEADERS
        BASE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}
        FILES
            print.h
)
