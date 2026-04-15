#include "layout_engine.hpp"
#include <sstream>
#include <algorithm>
#include <cctype>

static inline void trim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) { return !std::isspace(ch); }));
    s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) { return !std::isspace(ch); }).base(), s.end());
}
static inline bool starts_with(const std::string& str, const std::string& prefix) {
    if (str.length() < prefix.length()) return false;
    return str.compare(0, prefix.length(), prefix) == 0;
}
static inline bool ends_with(const std::string& str, const std::string& suffix) {
    if (str.length() < suffix.length()) return false;
    return str.compare(str.length() - suffix.length(), suffix.length(), suffix) == 0;
}
static inline bool is_all_caps(const std::string& str) {
    bool has_alpha = false;
    int upper_count = 0;
    for (char c : str) {
        if (c >= 'a' && c <= 'z') return false;  
        if (c >= 'A' && c <= 'Z') {
            has_alpha = true;
            upper_count++;
        }
    }
    return has_alpha && upper_count > 1;  
}
static inline size_t utf8_length(const std::string& str) {
    size_t len = 0;
    for (char c : str) {  
        if ((c & 0xC0) != 0x80) len++;  
    }
    return len;
}

static inline std::vector<std::string> wrap_text(const std::string& text, float max_width, float char_width) {
    std::vector<std::string> lines;
    if (text.empty()) {
        lines.push_back("");
        return lines;
    }
    int max_chars = std::max(1, (int)(max_width / char_width));
    std::string current_line = "";
    int current_char_count = 0;
    for (size_t i = 0; i < text.length(); ) {
        size_t char_len = 1;
        unsigned char c = text[i];
        if ((c & 0xE0) == 0xC0) char_len = 2;
        else if ((c & 0xF0) == 0xE0) char_len = 3;
        else if ((c & 0xF8) == 0xF0) char_len = 4;
        if (i + char_len > text.length()) char_len = text.length() - i;  

        std::string utf8_char = text.substr(i, char_len);
        i += char_len;
        current_line += utf8_char;
        current_char_count++;

        if (current_char_count >= max_chars) {
            size_t last_space = current_line.find_last_of(' ');
            if (last_space != std::string::npos && last_space > 0) {
                lines.push_back(current_line.substr(0, last_space + 1));
                current_line = current_line.substr(last_space + 1);
                current_char_count = utf8_length(current_line);  
            } else {
                lines.push_back(current_line);
                current_line = "";
                current_char_count = 0;
            }
        }
    }
    if (!current_line.empty()) lines.push_back(current_line);
    return lines;
}

LayoutEngine::LayoutEngine() {}

std::vector<TextBlock> LayoutEngine::parse_fountain(const std::string& text) {
    std::vector<TextBlock> blocks;
    size_t pos = 0;
    BlockType last_type = BlockType::Action;
    
    bool in_title_page = true;
    bool has_title_data = false;
    bool script_started = false;
    BlockType current_title_type = BlockType::TitleCenter;

    while (pos <= text.length()) {
        size_t current_start = pos;
        size_t next_pos = text.find('\n', pos);
        std::string line;
        size_t consumed = 0;

        if (next_pos == std::string::npos) {
            line = text.substr(pos);
            consumed = line.length();
            pos = text.length() + 1; // Çıkış
        } else {
            line = text.substr(pos, next_pos - pos);
            consumed = next_pos - pos + 1; // +1 newline karakteri için
            pos = next_pos + 1;
        }

        if (!line.empty() && line.back() == '\r') line.pop_back();

        std::string clean = line;
        trim(clean);

        if (in_title_page) {
            if (clean.empty()) {
                if (has_title_data) in_title_page = false;
                TextBlock b; b.text = line; b.type = BlockType::Action;
                b.source_start = current_start; b.source_length = consumed;
                blocks.push_back(b);
                continue;
            }
            size_t colon_pos = clean.find(':');
            if (colon_pos != std::string::npos && colon_pos < 15) {
                has_title_data = true;
                std::string key = clean.substr(0, colon_pos);
                std::transform(key.begin(), key.end(), key.begin(), ::tolower);
                if (key == "contact" || key == "copyright" || key == "date" || key == "draft date" || key == "notes") current_title_type = BlockType::TitleLeft;
                else if (key == "watermark") current_title_type = BlockType::Watermark;
                else current_title_type = BlockType::TitleCenter;

                TextBlock b; b.text = line; b.type = current_title_type;
                b.source_start = current_start; b.source_length = consumed;
                blocks.push_back(b);
                continue;
            } else if (has_title_data) {
                TextBlock b; b.text = line; b.type = current_title_type;
                b.source_start = current_start; b.source_length = consumed;
                blocks.push_back(b);
                continue;
            } else {
                in_title_page = false;
            }
        }

        if (clean.empty()) {
            TextBlock b; b.text = line; b.type = BlockType::Action;
            b.source_start = current_start; b.source_length = consumed;
            blocks.push_back(b);
            if (script_started) last_type = BlockType::Action;
            continue;
        }
        script_started = true;

        size_t p_start = clean.find('(');
        if (p_start != std::string::npos && p_start > 0 && clean.back() == ')') {
            std::string name = clean.substr(0, p_start);
            trim(name);
            if (is_all_caps(name) && !starts_with(name, "INT.") && !starts_with(name, "EXT.")) {
                size_t actual_p_start = line.find('(');
                TextBlock b1; b1.text = line.substr(0, actual_p_start); b1.type = BlockType::Character;
                b1.source_start = current_start; b1.source_length = actual_p_start;
                blocks.push_back(b1);

                TextBlock b2; b2.text = line.substr(actual_p_start); b2.type = BlockType::Parenthetical;
                b2.source_start = current_start + actual_p_start; b2.source_length = consumed - actual_p_start;
                blocks.push_back(b2);
                last_type = BlockType::Parenthetical;
                continue;
            }
        }

        TextBlock block;
        block.text = line;
        block.source_start = current_start;
        block.source_length = consumed;

        // YENİ: INT/EXT. ve I/E. gibi diğer tüm Sahne Başlığı ihtimalleri eklendi
        if (starts_with(clean, "INT.") || starts_with(clean, "EXT.") || 
            starts_with(clean, "INT/EXT.") || starts_with(clean, "EXT/INT.") || 
            starts_with(clean, "I/E.") || starts_with(clean, "EST.")) {
            block.type = BlockType::SceneHeading;
        }
        else if (is_all_caps(clean) && (ends_with(clean, " TO:") || starts_with(clean, "FADE "))) block.type = BlockType::Transition;
        else if (is_all_caps(clean)) block.type = BlockType::Character;
        else if (starts_with(clean, "(")) block.type = BlockType::Parenthetical;
        else if (last_type == BlockType::Character || last_type == BlockType::Parenthetical || last_type == BlockType::Dialogue) block.type = BlockType::Dialogue;
        else block.type = BlockType::Action;

        last_type = block.type;
        blocks.push_back(block);
    }
    return blocks;
}

std::vector<Page> LayoutEngine::paginate_text(const std::string& raw_text) {
    std::vector<Page> pages;
    auto parsed_blocks = parse_fountain(raw_text);

    Page title_page; title_page.page_number = 1;
    Page script_page; script_page.page_number = 2;

    float inch = 96.0f;
    
    float title_left_total_h = 0.0f;
    for (auto& block : parsed_blocks) {
        if (block.type == BlockType::TitleLeft) {
            auto wrapped = wrap_text(block.text, page_width - (2.5f * inch), char_width);
            title_left_total_h += std::max(1, (int)wrapped.size()) * line_spacing;
        }
    }

    float title_center_y = 3.5f * inch;  
    float title_left_y = page_height - margin_bottom - title_left_total_h;  

    float script_y = margin_top;
    bool has_last_non_empty = false;
    BlockType last_type = BlockType::Action;
    float last_y = margin_top;
    float last_h = 0.0f;

    for (auto& block : parsed_blocks) {
        float allowed_w = 0.0f;

        if (block.type == BlockType::TitleCenter || block.type == BlockType::TitleLeft || block.type == BlockType::Watermark) {
            if (block.type == BlockType::TitleCenter) {
                block.x = 2.5f * inch; allowed_w = page_width - (4.0f * inch);
                auto wrapped = wrap_text(block.text, allowed_w, char_width);
                block.wrapped_lines = wrapped;
                block.height = std::max(1, (int)wrapped.size()) * line_spacing;
                std::string final_t = ""; for(size_t j=0; j<wrapped.size(); ++j) { final_t += wrapped[j]; if(j < wrapped.size()-1) final_t += "\n"; }
                block.text = final_t;
                block.y = title_center_y; title_center_y += block.height;
            } 
            else if (block.type == BlockType::TitleLeft) {
                block.x = 1.5f * inch; allowed_w = page_width - (2.5f * inch);  
                auto wrapped = wrap_text(block.text, allowed_w, char_width);
                block.wrapped_lines = wrapped;
                block.height = std::max(1, (int)wrapped.size()) * line_spacing;
                std::string final_t = ""; for(size_t j=0; j<wrapped.size(); ++j) { final_t += wrapped[j]; if(j < wrapped.size()-1) final_t += "\n"; }
                block.text = final_t;
                block.y = title_left_y; title_left_y += block.height;
            } 
            else if (block.type == BlockType::Watermark) {
                block.x = 1.5f * inch; allowed_w = page_width; block.y = page_height / 2.0f; block.height = line_spacing;
                block.wrapped_lines = {block.text};
            }
            block.width = allowed_w;
            title_page.blocks.push_back(block);
        }
        else {
            if (block.type == BlockType::SceneHeading || block.type == BlockType::Action) { block.x = 1.5f * inch; allowed_w = page_width - (2.5f * inch); }
            else if (block.type == BlockType::Character) { block.x = 3.5f * inch; allowed_w = page_width - block.x - inch; }
            else if (block.type == BlockType::Parenthetical) { block.x = 3.1f * inch; allowed_w = 2.0f * inch; }
            else if (block.type == BlockType::Dialogue) { block.x = 2.5f * inch; allowed_w = page_width - (5.0f * inch); }
            else if (block.type == BlockType::Transition) { block.x = 6.0f * inch; allowed_w = page_width - block.x - inch; }

            auto wrapped = wrap_text(block.text, allowed_w, char_width);
            block.wrapped_lines = wrapped;

            // BU KISIM DÜZELTİLDİ: Boş satırlar 0 değil, normal satır yüksekliği alır.
            if (block.text.empty()) { 
                block.height = line_spacing; 
                block.text = ""; 
                block.wrapped_lines = {""}; 
            }  
            else {
                block.height = wrapped.size() * line_spacing;
                std::string final_t = "";
                for(size_t j=0; j<wrapped.size(); ++j) { final_t += wrapped[j]; if(j < wrapped.size()-1) final_t += "\n"; }
                block.text = final_t;
            }

            block.width = allowed_w;

            if (!block.text.empty() && has_last_non_empty) {
                bool needs_gap = true;  
                if (last_type == BlockType::Character && block.type == BlockType::Dialogue) needs_gap = false;
                if (last_type == BlockType::Character && block.type == BlockType::Parenthetical) needs_gap = false;
                if (last_type == BlockType::Parenthetical && block.type == BlockType::Dialogue) needs_gap = false;
                if (last_type == BlockType::Action && block.type == BlockType::Action) needs_gap = false;
                if (last_type == BlockType::Dialogue && block.type == BlockType::Dialogue) needs_gap = false;
                
                if (needs_gap) {
                    float required_min_y = last_y + last_h + line_spacing;
                    if (script_y < required_min_y) script_y = required_min_y;
                }
            }

            if (script_y + block.height > page_height - margin_bottom) {
                pages.push_back(script_page);
                script_page = Page(); script_page.page_number = pages.back().page_number + 1; script_y = margin_top;
                has_last_non_empty = false;  
            }

            block.y = script_y;
            script_page.blocks.push_back(block);
            script_y += block.height;  
            
            if (!block.text.empty()) {
                has_last_non_empty = true;
                last_type = block.type;
                last_y = block.y;
                last_h = block.height;
            }
        }
    }
    pages.insert(pages.begin(), title_page);  
    pages.push_back(script_page);  
    return pages;
}

std::vector<float> LayoutEngine::calculate_cursor_position(const std::string& full_text, int cursor_byte_pos) {
    auto pages = paginate_text(full_text);

    Page* target_page = nullptr;
    TextBlock* target_block = nullptr;

    // DÜZELTİLEN KISIM: Aceleci 'break' kaldırıldı, son eşleşen (yeni satır) kazanır.
    for (auto& page : pages) {
        for (auto& block : page.blocks) {
            // Durum 1: İmleç bloğun metin sınırları içindeyse (boşluklar dahil)
            if (cursor_byte_pos >= block.source_start && cursor_byte_pos < block.source_start + block.source_length) {
                target_page = &page;
                target_block = &block;
            }
            // Durum 2: Blok tamamen boşsa (Enter ile açılmış yeni satır) ve imleç tam oradaysa
            else if (block.source_length == 0 && cursor_byte_pos == block.source_start) {
                target_page = &page;
                target_block = &block;
            }
            // Durum 3: Dosyanın en sonundaysak ve imleç bu bloğun bitişine dayanmışsa
            else if (cursor_byte_pos == full_text.length() && cursor_byte_pos == block.source_start + block.source_length) {
                target_page = &page;
                target_block = &block;
            }
        }
    }

    if (!target_block) {
        if (pages.size() > 1) return {1.5f * 96.0f, margin_top, (page_height + 50.0f) + margin_top, static_cast<float>(BlockType::Action)};
        return {1.5f * 96.0f, margin_top, margin_top, static_cast<float>(BlockType::Action)};
    }

    int rel_byte_pos = cursor_byte_pos - target_block->source_start;
    float cy = target_block->y;
    float cx = target_block->x;
    int current_byte_sum = 0;

    for (size_t i = 0; i < target_block->wrapped_lines.size(); ++i) {
        const auto& w_line = target_block->wrapped_lines[i];
        int w_len_bytes = w_line.length();
        bool is_last_line = (i == target_block->wrapped_lines.size() - 1);
        
        if (rel_byte_pos <= current_byte_sum + w_len_bytes || is_last_line) {
            int bytes_in_this_line = rel_byte_pos - current_byte_sum;
            if (bytes_in_this_line > w_len_bytes) bytes_in_this_line = w_len_bytes; 
            
            std::string sub = w_line.substr(0, bytes_in_this_line);
            int chars_in = utf8_length(sub);
            cx = target_block->x + (chars_in * char_width);
            break; // Sadece satır içi kelime kaydırma döngüsünü kırıyoruz
        }
        current_byte_sum += w_len_bytes;
        cy += line_spacing;
    }

    float abs_y = ((target_page->page_number - 1) * (page_height + 50.0f)) + cy;
    // YENİ: BlockType'ı float'a çevirip 4. eleman olarak yolluyoruz
    float block_type_float = static_cast<float>(target_block->type);
    return {cx, cy, abs_y, block_type_float};
}