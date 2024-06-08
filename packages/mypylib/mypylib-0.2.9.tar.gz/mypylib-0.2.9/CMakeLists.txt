cmake_minimum_required(VERSION 3.10)

project(callback_example LANGUAGES C)

# Specify the C standard
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED True)

# Add the library target
add_library(callback_example SHARED mypylib/my_module/callback_example.c)

# Link pthread library
find_package(Threads REQUIRED)
target_link_libraries(callback_example PRIVATE Threads::Threads)

# Specify output directory
set_target_properties(callback_example PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/mypylib/my_module
)
