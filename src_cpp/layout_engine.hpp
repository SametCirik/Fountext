#pragma once
#include <string>
#include <vector>

enum class BlockType {
    SceneHeading,
    Action,
    Character,
    Dialogue,
    Parenthetical,
    Transition,
    TitleCenter,
    TitleLeft,
    TitleRight,
    Watermark
};

struct TextBlock {
    std::string text;
    BlockType type;
    
    float x;
    float y;
    float width;
    float height;
    
    // YENİ: Orjinal metin üzerindeki mutlak konumu ve kelime kaydırma verisi
    size_t source_start;
    size_t source_length;
    std::vector<std::string> wrapped_lines;
};

struct Page {
    int page_number;
    std::vector<TextBlock> blocks;
};

class LayoutEngine {
public:
    LayoutEngine();
    
    float page_width = 794.0f;
    float page_height = 1123.0f;
    
    float margin_top = 96.0f;
    float margin_bottom = 96.0f;
    float margin_left = 144.0f;
    float margin_right = 96.0f;

    float char_width = 8.0f;  
    float line_spacing = 24.0f; // YENİ: Python'dan alınacak satır yüksekliği

    std::vector<Page> paginate_text(const std::string& raw_fountain_text);

// YENİ: Artık X, Y, Abs_Y, ve BlockType_INT dönüyor!
    std::vector<float> calculate_cursor_position(const std::string& full_text, int cursor_byte_pos);

private:
    std::vector<TextBlock> parse_fountain(const std::string& text);
};