import os
from PyQt6.QtWidgets import QToolBar, QComboBox, QStyle
from PyQt6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor # YENİ EKLENENLER
from PyQt6.QtCore import Qt

class EditorToolBar(QToolBar):
    def __init__(self, main_window, editor):
        super().__init__("Format Araç Çubuğu", main_window)
        self.main_window = main_window
        self.editor = editor
        
        self.setMovable(False)  
        self._setup_toolbar()

    def get_icon(self, icon_name, fallback_standard=None):
        custom_path = f"assets/icons/{icon_name}.svg"  
        if os.path.exists(custom_path):
            # 1. SVG'den 24x24 (standart araç çubuğu boyutu) net bir resim (pixmap) oluştur
            icon = QIcon(custom_path)
            pixmap = icon.pixmap(24, 24)
            
            # 2. Üzerine boya yapacağımız fırçayı (Painter) hazırla
            painter = QPainter(pixmap)
            # Sadece çizili (saydam olmayan) pikselleri boyama modunu aç
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            
            # 3. İkonu temanın metin rengine (açık gri/beyaz) boya
            painter.fillRect(pixmap.rect(), QColor("#d3d3d3"))
            painter.end()
            
            # Boyanmış resmi tekrar ikona çevirip gönder
            return QIcon(pixmap)
            
        if fallback_standard:
            return self.style().standardIcon(fallback_standard)
        return QIcon()

    def _setup_toolbar(self):
        # Hamburger Menü Butonu (Navigator Toggle)
        self.toggle_nav_action = QAction(self.get_icon("menu", QStyle.StandardPixmap.SP_ToolBarHorizontalExtensionButton), "☰ Sahneler", self)
        self.toggle_nav_action.setToolTip("Sahne Gezginini Aç/Kapat")
        self.toggle_nav_action.triggered.connect(self.main_window.toggle_navigator)
        self.addAction(self.toggle_nav_action)

        self.addSeparator()

        undo_action = QAction(self.get_icon("undo", QStyle.StandardPixmap.SP_ArrowBack), "Geri Al", self)
        undo_action.triggered.connect(self._dummy_undo)
        self.addAction(undo_action)

        redo_action = QAction(self.get_icon("redo", QStyle.StandardPixmap.SP_ArrowForward), "Yinele", self)
        redo_action.triggered.connect(self._dummy_redo)
        self.addAction(redo_action)

        self.addSeparator()

        self.format_combo = QComboBox()
        self.format_combo.addItems(["Eylem", "Sahne Başlığı", "Karakter", "Parantez İçi", "Diyalog"])
        self.addWidget(self.format_combo)

    def _dummy_undo(self):
        self.editor.hidden_editor.undo()

    def _dummy_redo(self):
        self.editor.hidden_editor.redo()

    def update_active_block(self, block_type_int):
        type_mapping = {
            0: "Sahne Başlığı",   
            1: "Eylem",           
            2: "Karakter",        
            3: "Diyalog",         
            4: "Parantez İçi",    
            5: "Eylem",           
        }
        
        target_text = type_mapping.get(block_type_int, "Eylem")
        
        index = self.format_combo.findText(target_text)
        if index >= 0:
            self.format_combo.blockSignals(True)
            self.format_combo.setCurrentIndex(index)
            self.format_combo.blockSignals(False)
            
        # Terminal kirliliği yaratmaması için log print'ini kaldırabilir veya yorum satırına alabilirsin
        # print(f"[TOOLBAR] Aktif Blok Tipi Güncellendi: {target_text}")
            
        # print(f"[TOOLBAR] Aktif Blok Tipi Güncellendi: {target_text}")