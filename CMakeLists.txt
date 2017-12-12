cmake_minimum_required(VERSION 2.8.12)

project(cmake_wrapper)

message(WARNING "Conan MySQL Connector/C Wrapped CMake")

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")

# Instead the full conan_basic_setup, just these, so avoid messing with the output paths.
conan_check_compiler()
conan_flags_setup()

include("CMakeListsOriginal.cmake")

# Turn off -Werror in GCC debug builds.
if(CMAKE_COMPILER_IS_GNUCC AND CMAKE_COMPILER_IS_GNUCXX)
    target_compile_options(mysys
	PUBLIC -Wno-error)
endif()
