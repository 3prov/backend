#!/bin/bash

DIR=$(find . -name "hungarian_algorithm_cpp")
cd $DIR &&
mkdir -p build &&
cd build &&
cmake .. &&
make &&
cd ../../ &&
cp ./hungarian_algorithm_cpp/build/*.so .
