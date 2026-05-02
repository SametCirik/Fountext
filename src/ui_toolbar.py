import os
from PyQt6.QtWidgets import QToolBar, QComboBox, QStyle
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt
from lang_controller import LanguageController, tr

class EditorToolBar(QToolBar):
    def __init__(self, main_window, editor):
        super().__init__("Format Araç Çubuğu", main_window)
        self.main_window = main_window
        self.editor = editor
        self.setMovable(False)  
        self._setup_toolbar()
        LanguageController().language_changed.connect(self.update_texts)

    def get_icon(self, icon_name, fallback_standard=None):
        custom_path = f"assets/icons/{icon_name}.svg"  
        if os.path.exists(custom_path):
            icon = QIcon(custom_path)
            pixmap = icon.pixmap(24, 24)
            painter = QPainter(pixmap)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor("#d3d3d3"))
            painter.end()
            return QIcon(pixmap)
        if fallback_standard:
            return self.style().standardIcon(fallback_standard)
        return QIcon()

    def _setup_toolbar(self):
        self.toggle_nav_action = QAction(self.get_icon("menu", QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton), tr("toolbar_scenes"), self)
        self.toggle_nav_action.setToolTip(tr("toolbar_nav_tooltip"))
        self.toggle_nav_action.triggered.connect(self.main_window.toggle_navigator)
        self.addAction(self.toggle_nav_action)

        self.addSeparator()

        self.undo_action = QAction(self.get_icon("undo", QStyle.StandardPixmap.SP_ArrowBack), tr("menu_undo"), self)
        self.undo_action.triggered.connect(self._dummy_undo)
        self.addAction(self.undo_action)

        self.redo_action = QAction(self.get_icon("redo", QStyle.StandardPixmap.SP_ArrowForward), tr("menu_redo"), self)
        self.redo_action.triggered.connect(self._dummy_redo)
        self.addAction(self.redo_action)

        self.addSeparator()

        self.format_combo = QComboBox()
        self.update_combo_items()
        self.addWidget(self.format_combo)

    def update_combo_items(self):
        current_idx = self.format_combo.currentIndex()
        self.format_combo.clear()
        self.format_combo.addItems([tr("block_action"), tr("block_scene"), tr("block_character"), tr("block_parenthetical"), tr("block_dialogue")])
        if current_idx >= 0:
            self.format_combo.setCurrentIndex(current_idx)

    def update_texts(self):
        self.toggle_nav_action.setText(tr("toolbar_scenes"))
        self.toggle_nav_action.setToolTip(tr("toolbar_nav_tooltip"))
        self.undo_action.setText(tr("menu_undo"))
        self.redo_action.setText(tr("menu_redo"))
        self.update_combo_items()

    def _dummy_undo(self):
        self.editor.hidden_editor.undo()

    def _dummy_redo(self):
        self.editor.hidden_editor.redo()

    def update_active_block(self, block_type_int):
        type_mapping = {
            0: tr("block_scene"),   
            1: tr("block_action"),            
            2: tr("block_character"),        
            3: tr("block_dialogue"),         
            4: tr("block_parenthetical"),    
            5: tr("block_action"),            
        }
        target_text = type_mapping.get(block_type_int, tr("block_action"))
        index = self.format_combo.findText(target_text)
        if index >= 0:
            self.format_combo.blockSignals(True)
            self.format_combo.setCurrentIndex(index)
            self.format_combo.blockSignals(False)
