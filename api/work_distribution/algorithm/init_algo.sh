#!/bin/sh

set -e


DIR=$(find . -name "hungarian_algorithm_cpp")

cd $DIR
if [ $(find .. -maxdepth 1 -name *.so | wc -l) -eq 1 ]
then
  echo "Library already compiled.";
  exit 0;
fi

mkdir -p build
cd build
cmake ..
make
cd ../../
cp ./hungarian_algorithm_cpp/build/*.so .
