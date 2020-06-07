cmake_minimum_required(VERSION 3.10)
project(Pandora'sBox)

set(CMAKE_CXX_STANDARD 14)
#set(CMAKE_BUILD_TYPE "release")
set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g -ggdb" )
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O2 -fvisibility=hidden -s -Wall")
add_executable(pandora main.cpp)