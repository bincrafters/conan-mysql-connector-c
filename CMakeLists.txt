cmake_minimum_required(VERSION 2.8.12)

project(cmake_wrapper)

message(WARNING "Conan MySQL Connector/C Wrapped CMake")

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

add_subdirectory("sources")
