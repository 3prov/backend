set(MODULE_NAME "mcximings_HungarianAlgorithm")
set(CPP_FILE "Hungarian.cpp")

set(PYBIND11_GIT_REPOSITORY_URL "https://github.com/pybind/pybind11")
set(PYBIND11_GIT_REPOSITORY_VERSION "v2.9.2")


cmake_minimum_required(VERSION 3.4)
project(${MODULE_NAME})

include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY ${PYBIND11_GIT_REPOSITORY_URL}
    GIT_TAG        ${PYBIND11_GIT_REPOSITORY_VERSION}
)

FetchContent_GetProperties(pybind11)
if(NOT pybind11_POPULATED)
    FetchContent_Populate(pybind11)
    add_subdirectory(${pybind11_SOURCE_DIR} ${pybind11_BINARY_DIR})
endif()

pybind11_add_module(${MODULE_NAME} ${CPP_FILE})
