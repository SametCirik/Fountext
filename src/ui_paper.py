import sys
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QApplication, QTextEdit
from PyQt6.QtGui import QFont, QColor, QBrush, QPen, QTextCursor, QFontMetricsF, QPainter, QTextBlockFormat
from PyQt6.QtCore import Qt, QTimer

import fountext_engine
from ui_title_dialog import TitlePageDialog
from ui_title import decorate_title_page

DEBUG_MODE = False 

class Workspace(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.engine = fountext_engine.LayoutEngine()
        
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        self.setBackgroundBrush(QBrush(QColor("#2b2b2b")))
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing | 
            QPainter.RenderHint.TextAntialiasing | 
            QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # --- NORMAL FONT ---
        self.fountain_font = QFont("Courier Prime", 12)
        self.fountain_font.setStyleHint(QFont.StyleHint.Monospace)
        self.fountain_font.setFixedPitch(True)
        
        # --- KALIN FONT (Sahne Başlıkları İçin) ---
        self.fountain_font_bold = QFont("Courier Prime", 12, QFont.Weight.Bold)
        self.fountain_font_bold.setStyleHint(QFont.StyleHint.Monospace)
        self.fountain_font_bold.setFixedPitch(True)
        
        if not self.fountain_font.exactMatch():
            self.fountain_font = QFont("Courier", 12)
            self.fountain_font.setStyleHint(QFont.StyleHint.Monospace)
            self.fountain_font.setFixedPitch(True)
            self.fountain_font_bold = QFont("Courier", 12, QFont.Weight.Bold)
            self.fountain_font_bold.setStyleHint(QFont.StyleHint.Monospace)
            self.fountain_font_bold.setFixedPitch(True)

        fm = QFontMetricsF(self.fountain_font)
        exact_char_width = fm.horizontalAdvance("A")
        
        self.engine.char_width = exact_char_width  
        self.engine.line_spacing = fm.lineSpacing() 
        
        self.title_text = "Title: [SENARYO ADI]\nCredit: Yazan\nAuthor: [İsim Soyisim]\nDate: 10 Nisan 2026\nCopyright: (c) 2026\nWatermark: \nContact: \nTelefon Numarası\nE-Posta Adresi\n\n"
        self.raw_text = ""
        
        self.cursor_pos = 0  
        
        self.hidden_editor = QTextEdit(self)
        self.hidden_editor.setGeometry(-1000, -1000, 10, 10)  
        self.hidden_editor.setPlainText(self.raw_text)  
        self.hidden_editor.textChanged.connect(self._sync_text)
        self.hidden_editor.cursorPositionChanged.connect(self._sync_cursor)

        self.cursor_visible = True
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_timer.start(500)  
        self.cursor_item = None
        
        self.update_layout()

    def set_zoom(self, zoom_percentage):
        scale_factor = zoom_percentage / 100.0
        self.resetTransform()
        self.scale(scale_factor, scale_factor)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            main_win = self.window()
            
            if hasattr(main_win, 'footer'):
                current_zoom = main_win.footer.zoom_slider.value()
                if delta > 0:
                    new_zoom = min(200, current_zoom + 10)
                else:
                    new_zoom = max(50, current_zoom - 10)
                main_win.footer.zoom_slider.setValue(new_zoom)
            event.accept()
        else:
            super().wheelEvent(event)

    def open_title_dialog(self):
        dialog = TitlePageDialog(self, self.title_text)
        if dialog.exec():
            new_title = dialog.get_fountain_format()
            if self.title_text != new_title:
                self.title_text = new_title
                self.update_layout()
                main_win = self.window()
                if hasattr(main_win, 'mark_unsaved'):
                    main_win.mark_unsaved()

    def _sync_text(self):
        new_text = self.hidden_editor.toPlainText()
        if self.raw_text != new_text:
            self.raw_text = new_text
            self.update_layout()
            
            main_win = self.window()
            if hasattr(main_win, 'mark_unsaved'):
                main_win.mark_unsaved()

    def _sync_cursor(self):
        self.cursor_pos = self.hidden_editor.textCursor().position()
        self.update_cursor_visual()

    def blink_cursor(self):
        if self.cursor_item:
            self.cursor_visible = not self.cursor_visible
            self.cursor_item.setVisible(self.cursor_visible)

    def update_cursor_visual(self, action="Hareket"):
        full_text = self.title_text + self.raw_text
        
        abs_char_index = len(self.title_text) + self.cursor_pos
        text_before_cursor = full_text[:abs_char_index]
        cursor_byte_pos = len(text_before_cursor.encode('utf-8'))
        
        result = self.engine.calculate_cursor_position(full_text, cursor_byte_pos)
        cx, cy, absolute_y = result[0], result[1], result[2]
        block_type_val = int(result[3]) if len(result) > 3 else 1 
        
        # Mevcut sayfayı matematiksel olarak (y koordinatı / sayfa yüksekliği) hesaplıyoruz
        current_page = int(absolute_y // (self.engine.page_height + 50)) + 1
        # -----------------------

        if self.cursor_item:
            self.cursor_item.setLine(cx + 1, absolute_y + 2, cx + 1, absolute_y + self.engine.line_spacing - 1)
            self.ensureVisible(self.cursor_item, 50, 50)
            
        main_win = self.window()
        if hasattr(main_win, 'toolbar'):
            main_win.toolbar.update_active_block(block_type_val)

        # Footer'a bulunduğumuz sayfayı bildiriyoruz
        if hasattr(main_win, 'footer'):
            main_win.footer.update_stats(current_page=current_page)
        # -----------------------

        if DEBUG_MODE:
            last_char = text_before_cursor[-1] if text_before_cursor else "BOŞ"
            print(f"[LOG: {action:15}] Byte İndeksi: {cursor_byte_pos:4} | Karakter: {repr(last_char):5} | Koordinat: ({cx:6.2f}, {absolute_y:7.2f}) | Tip: {block_type_val}")

    def update_layout(self):
        self.scene.clear()  
        full_text = self.title_text + self.raw_text
        pages = self.engine.paginate_text(full_text)
        
        page_spacing = 50  
        current_page_y = 0
        
        extracted_scenes = [] 
        
        for page in pages:
            paper_rect = QGraphicsRectItem(0, current_page_y, self.engine.page_width, self.engine.page_height)
            paper_rect.setBrush(QBrush(QColor("white")))
            paper_rect.setPen(QPen(Qt.PenStyle.NoPen))
            self.scene.addItem(paper_rect)
            
            if page.page_number == 1:
                decorate_title_page(self.scene, page, current_page_y, self.fountain_font, self.engine.page_width)
            
            for block in page.blocks:
                if block.type == fountext_engine.BlockType.SceneHeading and block.text.strip():
                    extracted_scenes.append((block.text, current_page_y + block.y))
                
                if block.text.strip() and block.type != fountext_engine.BlockType.Watermark:
                    text_item = QGraphicsTextItem()
                    
                    # YENİ: Sahne Başlıkları ve KARAKTERLER İçin Kalın Font Kullan
                    if block.type in (fountext_engine.BlockType.SceneHeading, fountext_engine.BlockType.Character):
                        text_item.setFont(self.fountain_font_bold)
                    else:
                        text_item.setFont(self.fountain_font)
                        
                    text_item.setDefaultTextColor(QColor("#1a1a1a"))
                    
                    display_text = block.text

                    if block.type in (fountext_engine.BlockType.TitleCenter, fountext_engine.BlockType.TitleLeft):
                        prefixes = ["title:", "credit:", "author:", "date:", "draft date:", "copyright:", "contact:"]
                        low_text = display_text.lower()
                        for p in prefixes:
                            if low_text.startswith(p):
                                display_text = display_text[len(p):].lstrip()
                                break
                                
                    text_item.setPlainText(display_text)  
                    text_item.document().setDocumentMargin(0)
                    
                    if block.type == fountext_engine.BlockType.TitleCenter:
                        text_item.setTextWidth(self.engine.page_width)
                        
                        fmt = QTextBlockFormat()
                        fmt.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                        cursor = text_item.textCursor()
                        cursor.select(QTextCursor.SelectionType.Document)
                        cursor.mergeBlockFormat(fmt)
                        
                        text_item.setPos(0, current_page_y + block.y)
                    else:
                        text_item.setPos(block.x, current_page_y + block.y)
                        
                    self.scene.addItem(text_item)
                
            current_page_y += self.engine.page_height + page_spacing

        self.cursor_item = self.scene.addLine(0, 0, 0, 0, QPen(QColor("black"), 1))
        self.update_cursor_visual(action="Layout_Yenile")
        self.scene.setSceneRect(0, 0, self.engine.page_width, current_page_y)
        
        # YENİ HALİ:
        main_win = self.window()
        if hasattr(main_win, 'footer'):
            total_pages = len(pages)
            total_chars = len(self.raw_text)
            # Parametre isimlerini (total_pages= , total_chars= ) ekledik:
            main_win.footer.update_stats(total_pages=total_pages, total_chars=total_chars)
            
        if hasattr(main_win, 'navigator'):
            main_win.navigator.update_scenes(extracted_scenes)
    
    def keyPressEvent(self, event):
        key_code = event.key()
        key_text = event.text()
        modifiers = QApplication.keyboardModifiers()
        
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_V:  
                clipboard_text = QApplication.clipboard().text()
                clipboard_text = clipboard_text.replace('\r\n', '\n').replace('\r', '')
                self.hidden_editor.insertPlainText(clipboard_text)
            elif event.key() == Qt.Key.Key_C:  
                selected_text = self.hidden_editor.textCursor().selectedText()
                selected_text = selected_text.replace('\u2029', '\n')
                QApplication.clipboard().setText(selected_text)
            elif event.key() == Qt.Key.Key_X:  
                selected_text = self.hidden_editor.textCursor().selectedText()
                selected_text = selected_text.replace('\u2029', '\n')
                QApplication.clipboard().setText(selected_text)
                self.hidden_editor.textCursor().removeSelectedText()
        elif event.key() == Qt.Key.Key_Tab:
            self.hidden_editor.insertPlainText("   ")  
        else:
            self.hidden_editor.keyPressEvent(event)
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        click_pos = self.mapToScene(event.pos())
        cx, cy = click_pos.x(), click_pos.y()
        
        if cy < self.engine.page_height:
            self.open_title_dialog()
            return
            
        if not self.raw_text:
            return super().mousePressEvent(event)

        low, high = 0, len(self.raw_text)
        best_idx = 0
        full_text = self.title_text + self.raw_text
        
        while low <= high:
            mid = (low + high) // 2
            abs_char_index = len(self.title_text) + mid
            text_before = full_text[:abs_char_index]
            byte_pos = len(text_before.encode('utf-8'))
            
            _, _, abs_y, _ = self.engine.calculate_cursor_position(full_text, byte_pos)
            
            if abs_y - self.engine.line_spacing <= cy <= abs_y + (self.engine.line_spacing / 2):
                best_idx = mid
                break
            elif abs_y < cy:
                low = mid + 1
            else:
                high = mid - 1
                
        if best_idx == 0:
            best_idx = low if low < len(self.raw_text) else len(self.raw_text)

        start_idx = best_idx
        while start_idx > 0 and self.raw_text[start_idx - 1] != '\n':
            start_idx -= 1
            
        end_idx = best_idx
        while end_idx < len(self.raw_text) and self.raw_text[end_idx] != '\n':
            end_idx += 1
            
        closest_idx = start_idx
        min_dist = float('inf')
        
        for i in range(start_idx, end_idx + 1):
            abs_char_index = len(self.title_text) + i
            text_before = full_text[:abs_char_index]
            byte_pos = len(text_before.encode('utf-8'))
            
            px, _, p_abs_y, _ = self.engine.calculate_cursor_position(full_text, byte_pos)
            
            dist = abs(px - cx) + abs(p_abs_y - cy) * 2  
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
                
        cursor = self.hidden_editor.textCursor()
        cursor.setPosition(closest_idx)
        self.hidden_editor.setTextCursor(cursor)
        self._sync_cursor()  
        
        super().mousePressEvent(event)