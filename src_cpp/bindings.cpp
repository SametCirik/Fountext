#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "layout_engine.hpp"

namespace py = pybind11;

PYBIND11_MODULE(fountext_engine, m) {
    m.doc() = "Fountext C++ Layout Engine Core";
    
    py::enum_<BlockType>(m, "BlockType")
        .value("SceneHeading", BlockType::SceneHeading)
        .value("Action", BlockType::Action)
        .value("Character", BlockType::Character)
        .value("Dialogue", BlockType::Dialogue)
        .value("Parenthetical", BlockType::Parenthetical)
        .value("Transition", BlockType::Transition)
        .value("TitleCenter", BlockType::TitleCenter)
        .value("TitleLeft", BlockType::TitleLeft)
        .value("TitleRight", BlockType::TitleRight)
        .value("Watermark", BlockType::Watermark)
        .export_values();

    py::class_<TextBlock>(m, "TextBlock")
        .def(py::init<>())
        .def_readwrite("text", &TextBlock::text)
        .def_readwrite("type", &TextBlock::type)
        .def_readwrite("x", &TextBlock::x)
        .def_readwrite("y", &TextBlock::y)
        .def_readwrite("width", &TextBlock::width)
        .def_readwrite("height", &TextBlock::height)
        .def_readwrite("source_start", &TextBlock::source_start)
        .def_readwrite("source_length", &TextBlock::source_length)
        .def_readwrite("wrapped_lines", &TextBlock::wrapped_lines);

    py::class_<Page>(m, "Page")
        .def(py::init<>())
        .def_readwrite("page_number", &Page::page_number)
        .def_readwrite("blocks", &Page::blocks);

    py::class_<LayoutEngine>(m, "LayoutEngine")
        .def(py::init<>())
        .def_readwrite("page_width", &LayoutEngine::page_width)
        .def_readwrite("page_height", &LayoutEngine::page_height)
        .def_readwrite("margin_top", &LayoutEngine::margin_top)
        .def_readwrite("margin_bottom", &LayoutEngine::margin_bottom)
        .def_readwrite("margin_left", &LayoutEngine::margin_left)
        .def_readwrite("margin_right", &LayoutEngine::margin_right)
        .def_readwrite("char_width", &LayoutEngine::char_width)
        .def_readwrite("line_spacing", &LayoutEngine::line_spacing) // YENİ
        .def("paginate_text", &LayoutEngine::paginate_text)
        .def("calculate_cursor_position", &LayoutEngine::calculate_cursor_position); // GÜNCELLENDİ
}