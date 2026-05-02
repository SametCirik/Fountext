import sys
import datetime
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QApplication, QTextEdit
from PyQt6.QtGui import QFont, QColor, QBrush, QPen, QTextCursor, QFontMetricsF, QPainter, QTextBlockFormat, QTextCharFormat
from PyQt6.QtCore import Qt, QTimer

import fountext_engine
from ui_title_dialog import TitlePageDialog
from ui_title import decorate_title_page
from lang_controller import LanguageController, tr

DEBUG_MODE = False

class Workspace(QGraphicsView):
    @property
    def title_text(self):
        return getattr(self, '_title_text', '')

    @title_text.setter
    def title_text(self, value):
        self._title_text = self._apply_normalization(value)

    def _apply_normalization(self, text):
        for dt in ["[SENARYO ADI]", "[SCRIPT TITLE]", "[TÍTULO DEL GUION]", "[TITRE DU SCÉNARIO]", "[НАЗВАНИЕ СЦЕНАРИЯ]"]:
            text = text.replace(f"Title: {dt}", "Title: " + tr('tp_default_title'))
            
        for dc in ["Yazan", "Written by", "Escrito por", "Écrit par", "Автор сценария"]:
            text = text.replace(f"Credit: {dc}", "Credit: " + tr('tp_default_credit'))
            
        for da in ["[İsim Soyisim]", "[Name Surname]", "[Nombre Apellido]", "[Nom Prénom]", "[Имя Фамилия]"]:
            text = text.replace(f"Author: {da}", "Author: " + tr('tp_default_author'))
            
        current_date_str = datetime.datetime.now().strftime("%d-%m-%Y")
        for dd in ["10 Nisan 2026", "10 April 2026", "10 Abril 2026", "10 Avril 2026", "10 Апреля 2026"]:
            text = text.replace(f"Date: {dd}", f"Date: {current_date_str}")
            
        contacts = [
            ("Telefon Numarası", "E-Posta Adresi"),
            ("Phone Number", "Email Address"),
            ("Número de Teléfono", "Correo Electrónico"),
            ("Numéro de Téléphone", "Adresse Email"),
            ("Номер телефона", "Электронная почта")
        ]
        for c1, c2 in contacts:
            search_str = c1 + "\n" + c2
            replace_str = tr('tp_default_contact1') + "\n" + tr('tp_default_contact2')
            text = text.replace(search_str, replace_str)
            
        return text

    def normalize_on_lang_change(self):
        self.title_text = getattr(self, '_title_text', '')
        self.update_layout()

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
        
        self.fountain_font = QFont("Courier Prime", 12)
        self.fountain_font.setStyleHint(QFont.StyleHint.Monospace)
        self.fountain_font.setFixedPitch(True)
        
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
        
        current_year = datetime.datetime.now().year
        current_date_str = datetime.datetime.now().strftime("%d-%m-%Y")
        
        initial_title = f"Title: {tr('tp_default_title')}\nCredit: {tr('tp_default_credit')}\nAuthor: {tr('tp_default_author')}\nDate: {current_date_str}\nCopyright: (c) {current_year}\nWatermark: \nContact: \n{tr('tp_default_contact1')}\n{tr('tp_default_contact2')}\n\n"
        
        self.title_text = initial_title
        self.raw_text = ""
        
        self.cursor_pos = 0  
        self.is_selecting = False
        self.rendered_blocks = []
        
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
        LanguageController().language_changed.connect(self.normalize_on_lang_change)
        self.verticalScrollBar().valueChanged.connect(self._update_visible_page)

    def _update_visible_page(self):
        visible_rect = self.mapToScene(self.viewport().rect()).boundingRect()
        center_y = visible_rect.center().y()
        page_step = self.engine.page_height + 50
        current_page = int(max(0, center_y) // page_step) + 1
        main_win = self.window()
        if hasattr(main_win, "footer"):
            main_win.footer.update_stats(current_page=current_page)

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
        self.update_selection_highlights()

    def blink_cursor(self):
        if self.cursor_item and not self.hidden_editor.textCursor().hasSelection():
            self.cursor_visible = not self.cursor_visible
            self.cursor_item.setVisible(self.cursor_visible)
        elif self.cursor_item:
            self.cursor_item.setVisible(False)

    def update_cursor_visual(self, action="Hareket"):
        full_text = self.title_text + self.raw_text
        
        abs_char_index = len(self.title_text) + self.cursor_pos
        text_before_cursor = full_text[:abs_char_index]
        cursor_byte_pos = len(text_before_cursor.encode('utf-8'))
        
        result = self.engine.calculate_cursor_position(full_text, cursor_byte_pos)
        cx, cy, absolute_y = result[0], result[1], result[2]
        block_type_val = int(result[3]) if len(result) > 3 else 1  

        if self.cursor_item:
            self.cursor_item.setLine(cx + 1, absolute_y + 2, cx + 1, absolute_y + self.engine.line_spacing - 1)
            if not self.hidden_editor.textCursor().hasSelection():
                self.ensureVisible(self.cursor_item, 50, 50)
            
        main_win = self.window()
        if hasattr(main_win, 'toolbar'):
            main_win.toolbar.update_active_block(block_type_val)

    def update_selection_highlights(self):
        sel_start = self.hidden_editor.textCursor().selectionStart() + len(self.title_text)
        sel_end = self.hidden_editor.textCursor().selectionEnd() + len(self.title_text)
        has_sel = self.hidden_editor.textCursor().hasSelection()
        
        for item, b_start, b_end in self.rendered_blocks:
            if b_start == -1: continue 
            
            cursor = item.textCursor()
            cursor.select(QTextCursor.SelectionType.Document)
            
            clear_fmt = QTextCharFormat()
            clear_fmt.setBackground(Qt.GlobalColor.transparent)
            clear_fmt.setForeground(QColor("#1a1a1a"))
            cursor.setCharFormat(clear_fmt)
            
            if has_sel:
                overlap_start = max(sel_start, b_start)
                overlap_end = min(sel_end, b_end)
                if overlap_start < overlap_end:
                    raw_local_start = overlap_start - b_start
                    raw_local_end = overlap_end - b_start
                    
                    cpp_text = item.toPlainText()
                    def map_idx(raw_idx):
                        mapped = 0
                        r = 0
                        for char in cpp_text:
                            if r == raw_idx: break
                            if char == '\n': mapped += 1
                            else: mapped += 1; r += 1
                        return mapped
                        
                    local_start = map_idx(raw_local_start)
                    local_end = map_idx(raw_local_end)
                    
                    text_len = item.document().characterCount() - 1
                    local_start = max(0, min(local_start, text_len))
                    local_end = max(0, min(local_end, text_len))
                    
                    sel_fmt = QTextCharFormat()
                    sel_fmt.setBackground(QColor(229, 160, 64, 130)) 
                    sel_fmt.setForeground(QColor("black"))
                    
                    cursor.setPosition(local_start)
                    cursor.setPosition(local_end, QTextCursor.MoveMode.KeepAnchor)
                    cursor.mergeCharFormat(sel_fmt)

    def update_layout(self):
        self.scene.clear()   
        self.rendered_blocks.clear()
        
        full_text = self.title_text + self.raw_text
        full_text_bytes = full_text.encode('utf-8')
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
                    
                    if block.type in (fountext_engine.BlockType.TitleCenter, fountext_engine.BlockType.TitleLeft, fountext_engine.BlockType.Watermark):
                        self.rendered_blocks.append((text_item, -1, -1))
                    else:
                        b_char_start = len(full_text_bytes[:block.source_start].decode('utf-8', errors='ignore'))
                        b_char_end = len(full_text_bytes[:block.source_start + block.source_length].decode('utf-8', errors='ignore'))
                        self.rendered_blocks.append((text_item, b_char_start, b_char_end))
                
            current_page_y += self.engine.page_height + page_spacing

        self.cursor_item = self.scene.addLine(0, 0, 0, 0, QPen(QColor("black"), 1))
        self.update_cursor_visual(action="Layout_Yenile")
        self.update_selection_highlights()
        self.scene.setSceneRect(0, 0, self.engine.page_width, current_page_y)
        
        main_win = self.window()
        if hasattr(main_win, 'footer'):
            main_win.footer.update_stats(total_pages=len(pages), total_chars=len(self.raw_text))
            
        if hasattr(main_win, 'navigator'):
            main_win.navigator.update_scenes(extracted_scenes)
            self._update_visible_page()
    
    def keyPressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        
        if event.key() == Qt.Key.Key_Up:
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - 50)
                return
            else:
                cursor = self.hidden_editor.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Up)
                self.hidden_editor.setTextCursor(cursor)
                self._sync_cursor()
                return

        elif event.key() == Qt.Key.Key_Down:
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + 50)
                return
            else:
                cursor = self.hidden_editor.textCursor()
                cursor.movePosition(QTextCursor.MoveOperation.Down)
                self.hidden_editor.setTextCursor(cursor)
                self._sync_cursor()
                return

        if modifiers == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_V:   
                clipboard_text = QApplication.clipboard().text()
                clipboard_text = clipboard_text.replace('\r\n', '\n').replace('\r', '')
                self.hidden_editor.insertPlainText(clipboard_text)
            elif event.key() == Qt.Key.Key_C:   
                selected_text = self.hidden_editor.textCursor().selectedText().replace('\u2029', '\n')
                QApplication.clipboard().setText(selected_text)
            elif event.key() == Qt.Key.Key_X:   
                selected_text = self.hidden_editor.textCursor().selectedText().replace('\u2029', '\n')
                QApplication.clipboard().setText(selected_text)
                self.hidden_editor.textCursor().removeSelectedText()
            else:
                self.hidden_editor.keyPressEvent(event)
        elif event.key() == Qt.Key.Key_Tab:
            self.hidden_editor.insertPlainText("   ")   
        else:
            self.hidden_editor.keyPressEvent(event)
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return super().mousePressEvent(event)
            
        click_pos = self.mapToScene(event.pos())
        cx, cy = click_pos.x(), click_pos.y()
        
        if cy < self.engine.page_height:
            self.open_title_dialog()
            return
            
        if not self.raw_text:
            return super().mousePressEvent(event)

        full_text = self.title_text + self.raw_text
        full_text_bytes = full_text.encode('utf-8')
        
        byte_idx = self.engine.calculate_index_from_position(full_text, cx, cy)
        char_idx = len(full_text_bytes[:byte_idx].decode('utf-8', errors='ignore'))
        text_idx = max(0, char_idx - len(self.title_text))
        
        cursor = self.hidden_editor.textCursor()
        cursor.setPosition(text_idx)
        self.hidden_editor.setTextCursor(cursor)
        self._sync_cursor()
        
        self.is_selecting = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if getattr(self, 'is_selecting', False):
            click_pos = self.mapToScene(event.pos())
            cx, cy = click_pos.x(), click_pos.y()
            
            full_text = self.title_text + self.raw_text
            full_text_bytes = full_text.encode('utf-8')
            
            byte_idx = self.engine.calculate_index_from_position(full_text, cx, cy)
            char_idx = len(full_text_bytes[:byte_idx].decode('utf-8', errors='ignore'))
            text_idx = max(0, char_idx - len(self.title_text))
            
            cursor = self.hidden_editor.textCursor()
            cursor.setPosition(text_idx, QTextCursor.MoveMode.KeepAnchor)
            self.hidden_editor.setTextCursor(cursor)
            self._sync_cursor()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_selecting = False
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            cursor = self.hidden_editor.textCursor()
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            self.hidden_editor.setTextCursor(cursor)
            self._sync_cursor()
        super().mouseDoubleClickEvent(event)
