#!/bin/bash

cd hungarian_algorithm_cpp &&
mkdir -p build &&
cd build &&
cmake .. &&
make &&
cd .. &&
cp "hungarian_algorithm_cpp/build/*.so" .  # не работает
