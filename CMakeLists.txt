cmake_minimum_required(VERSION 3.15)
project(fountext_layout_engine)

# Sanal ortamda kurduğumuz pybind11'i buluyoruz
find_package(pybind11 CONFIG REQUIRED)

# Oluşacak Python modülünün adı: fountext_engine
pybind11_add_module(fountext_engine
    src_cpp/bindings.cpp
    src_cpp/layout_engine.cpp
)

# C++17 standardını kullanıyoruz (modern dizgi algoritmaları için işimize yarayacak)
target_compile_features(fountext_engine PRIVATE cxx_std_17)