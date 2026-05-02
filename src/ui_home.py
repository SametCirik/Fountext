import os
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, pyqtSignal
from lang_controller import LanguageController, tr

DATA_DIR = "user_data/recent_projects"
PROJECTS_FILE = "user_data/projects.json"

# --- MEVCUT KARTLAR ---
class ProjectCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, name, path, img_path, is_guide=False):
        super().__init__()
        self.path = path
        self.setFixedSize(160, 250)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.setStyleSheet("""
            ProjectCard {
                background-color: #2b2b2b;
                border-radius: 8px;
                border: 2px solid #3b3b3b;
            }
            ProjectCard:hover {
                border: 2px solid #e5a040;
                background-color: #333333;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            self.img_label.setPixmap(pixmap)
        else:
            if is_guide:
                self.img_label.setText("i")
                self.img_label.setStyleSheet("color: #555555; font-size: 80px; font-weight: bold; font-family: 'Courier Prime', monospace;")
            else:
                self.img_label.setText("?")
                self.img_label.setStyleSheet("color: #555555; font-size: 80px; font-weight: bold; font-family: sans-serif;")

        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.name_label.setStyleSheet("color: #d3d3d3; font-weight: bold; font-family: sans-serif;")
        self.name_label.setWordWrap(True)
        self.name_label.setMinimumHeight(35)

        layout.addWidget(self.img_label, stretch=1)
        layout.addWidget(self.name_label, stretch=0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.path)

class BrowseCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.setFixedSize(160, 250)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.setStyleSheet("""
            BrowseCard {
                background-color: transparent;
                border-radius: 8px;
                border: 2px dashed #555555;
            }
            BrowseCard:hover {
                border: 2px dashed #e5a040;
                background-color: #2b2b2b;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.icon_label = QLabel("+")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("color: #555555; font-size: 72px; font-weight: normal;")
        
        self.name_label = QLabel(text)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.name_label.setStyleSheet("color: #a0a0a0; font-weight: bold; font-family: sans-serif;")
        self.name_label.setWordWrap(True)
        self.name_label.setMinimumHeight(35)

        layout.addWidget(self.icon_label, stretch=1)
        layout.addWidget(self.name_label, stretch=0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

class ProjectFolderCard(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, name, folder_path, poster_path=""):
        super().__init__()
        self.folder_path = folder_path
        self.setFixedSize(160, 250)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.setStyleSheet("""
            ProjectFolderCard {
                background-color: #2b2b2b;
                border-radius: 8px;
                border: 2px solid #3b3b3b;
            }
            ProjectFolderCard:hover {
                border: 2px solid #e5a040; 
                background-color: #333333;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if os.path.exists(poster_path):
            pixmap = QPixmap(poster_path)
            self.img_label.setPixmap(pixmap.scaled(140, 198, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.img_label.setText("📁")
            self.img_label.setStyleSheet("font-size: 64px;")

        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.name_label.setStyleSheet("color: #e5a040; font-weight: bold; font-family: sans-serif;")
        self.name_label.setWordWrap(True)
        self.name_label.setMinimumHeight(35)

        layout.addWidget(self.img_label, stretch=1)
        layout.addWidget(self.name_label, stretch=0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.folder_path)

class AddProjectCard(QFrame):
    clicked = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.setFixedSize(160, 250)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.setStyleSheet("""
            AddProjectCard {
                background-color: transparent;
                border-radius: 8px;
                border: 2px dashed #e5a040;
            }
            AddProjectCard:hover {
                background-color: #2b2b2b;
                border: 2px solid #e5a040;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.icon_label = QLabel("+")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("color: #e5a040; font-size: 72px; font-weight: normal;")
        
        self.name_label = QLabel(text)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        self.name_label.setStyleSheet("color: #e5a040; font-weight: bold; font-family: sans-serif;")
        self.name_label.setWordWrap(True)
        self.name_label.setMinimumHeight(35)

        layout.addWidget(self.icon_label, stretch=1)
        layout.addWidget(self.name_label, stretch=0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

# --- ANA MENÜ ARAYÜZÜ ---
class HomeMenu(QWidget):
    open_project_requested = pyqtSignal(str)
    new_project_requested = pyqtSignal()
    browse_project_requested = pyqtSignal()
    open_folder_requested = pyqtSignal(str) 
    create_folder_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ==========================================
        # DİNAMİK STICKY HEADER
        # ==========================================
        self.header_widget = QWidget()
        self.header_widget.setObjectName("HeaderWidget")
        self.header_widget.setStyleSheet("QWidget#HeaderWidget { background-color: #1e1e1e; border: none; }")
        
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(40, 40, 40, 35) 
        header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.title_label = QLabel(tr("app_title"))
        self.title_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold; font-family: 'Courier Prime', monospace; border: none; padding: 0; margin: 0;")
        
        # TAM İSTEDİĞİN GİBİ TEK BİR DİL BUTONU (SAĞ TARAFTA)
        self.btn_lang = QPushButton(LanguageController().current_lang.upper())
        self.btn_lang.setFixedSize(40, 40)
        self.btn_lang.setStyleSheet("""
            QPushButton { 
                background-color: transparent; color: #e5a040; font-weight: bold; 
                font-size: 16px; border: 2px solid #e5a040; border-radius: 5px; 
            } 
            QPushButton:hover { background-color: #e5a040; color: #1e1e1e; }
        """)
        self.btn_lang.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_lang.clicked.connect(self.toggle_lang)

        self.btn_new = QPushButton(tr("new_script_btn"))
        self.btn_new.setFixedSize(150, 40)
        self.btn_new.setStyleSheet("""
            QPushButton {
                background-color: #e5a040; 
                color: #3a3a3a; 
                font-weight: bold; 
                border-radius: 5px; 
                border: none;
            }
            QPushButton:hover { background-color: #f6b65a; }
        """)
        self.btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_new.clicked.connect(self.new_project_requested.emit)
        
        # DOĞRU SIRALAMA: Başlık -> Boşluk(Stretch) -> Dil Butonu -> Yeni Senaryo Butonu
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_lang)
        header_layout.addWidget(self.btn_new)
        
        main_layout.addWidget(self.header_widget)

        # ==========================================
        # KAYDIRMA ALANI (İÇERİK)
        # ==========================================
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background-color: #1e1e1e; }
            QScrollBar:vertical { background: #1e1e1e; width: 12px; }
            QScrollBar::handle:vertical { background: #3b3b3b; border-radius: 6px; }
            QScrollBar::handle:vertical:hover { background: #555555; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: none; border: none; }
        """)

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #1e1e1e;")
        
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(40, 5, 40, 40) 
        content_layout.setSpacing(30)

        def create_horizontal_scroll_row(title_text, title_color):
            title_lbl = QLabel(title_text)
            title_lbl.setStyleSheet(f"color: {title_color}; font-size: 18px; font-weight: bold;")
            content_layout.addWidget(title_lbl)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(290)
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll.setStyleSheet("""
                QScrollArea { border: none; background-color: transparent; }
                QScrollBar:horizontal { background: #1e1e1e; height: 10px; }
                QScrollBar::handle:horizontal { background: #3b3b3b; border-radius: 5px; }
                QScrollBar::handle:horizontal:hover { background: #555555; }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { background: none; border: none; }
            """)
            
            container = QWidget()
            container.setStyleSheet("background-color: transparent;")
            layout = QHBoxLayout(container)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(20)
            
            scroll.setWidget(container)
            content_layout.addWidget(scroll)
            return layout, title_lbl

        self.recent_layout, self.lbl_recent = create_horizontal_scroll_row(tr("recent_files_title"), "#a0a0a0")
        self.projects_layout, self.lbl_projects = create_horizontal_scroll_row(tr("projects_title"), "#e5a040")
        self.guide_layout, self.lbl_guides = create_horizontal_scroll_row(tr("guides_title"), "#a0a0a0")

        content_layout.addStretch()
        self.scroll_area.setWidget(self.content_widget)
        
        main_layout.addWidget(self.scroll_area)

        # --- DİNAMİK SCROLL DİNLEYİCİSİ ---
        self._is_scrolled = False
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_header_style)

        self.load_projects()
        LanguageController().language_changed.connect(self.update_texts)

    def toggle_lang(self):
        LanguageController().toggle_language()
        import sys, os
        # Yeni dille uygulamayı anında yeniden başlat
        os.execl(sys.executable, sys.executable, *sys.argv)

    def update_texts(self):
        self.title_label.setText(tr("app_title"))
        self.btn_lang.setText(LanguageController().current_lang.upper())
        self.btn_new.setText(tr("new_script_btn"))
        self.lbl_recent.setText(tr("recent_files_title"))
        self.lbl_projects.setText(tr("projects_title"))
        self.lbl_guides.setText(tr("guides_title"))
        self.load_projects()

    def update_header_style(self, value):
        if value > 0 and not self._is_scrolled:
            self.header_widget.setStyleSheet("QWidget#HeaderWidget { background-color: #181818; border-bottom: 1px solid #333; }")
            self._is_scrolled = True
        elif value == 0 and self._is_scrolled:
            self.header_widget.setStyleSheet("QWidget#HeaderWidget { background-color: #1e1e1e; border: none; }")
            self._is_scrolled = False

    def load_projects(self):
        self._clear_layout(self.recent_layout)
        
        recent_files_data = []
        if os.path.exists(DATA_DIR):
            for file in os.listdir(DATA_DIR):
                if file.endswith('.json'):
                    data_path = os.path.join(DATA_DIR, file)
                    img_path = data_path.replace('.json', '.png')
                    
                    with open(data_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    target_path = data.get('path', '')
                    if os.path.exists(target_path):
                        try:
                            mtime = os.path.getmtime(target_path)
                        except:
                            mtime = 0
                        recent_files_data.append((mtime, data['name'], target_path, img_path))

        recent_files_data.sort(key=lambda x: x[0], reverse=True)

        for _, name, path, img_path in recent_files_data:
            card = ProjectCard(name, path, img_path)
            card.clicked.connect(self.open_project_requested.emit)
            self.recent_layout.addWidget(card)

        browse_card = BrowseCard(tr("browse_pc"))
        browse_card.clicked.connect(self.browse_project_requested.emit)
        self.recent_layout.addWidget(browse_card)

        self._clear_layout(self.projects_layout)
        
        if os.path.exists(PROJECTS_FILE):
            with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
                try:
                    registered_projects = json.load(f)
                except json.JSONDecodeError:
                    registered_projects = []
            
            for folder_path in registered_projects:
                fountext_dir = os.path.join(folder_path, ".fountext")
                metadata_path = os.path.join(fountext_dir, "project.json")
                poster_path = os.path.join(fountext_dir, "poster.png")
                
                if os.path.exists(folder_path) and os.path.exists(metadata_path):
                    with open(metadata_path, 'r', encoding='utf-8') as mf:
                        try:
                            meta = json.load(mf)
                            name = meta.get("title", os.path.basename(folder_path))
                        except:
                            name = tr("untitled_project")
                            
                    card = ProjectFolderCard(name, folder_path, poster_path)
                    card.clicked.connect(self.open_folder_requested.emit)
                    self.projects_layout.addWidget(card)

        add_project_card = AddProjectCard(tr("new_project_folder"))
        add_project_card.clicked.connect(self.create_folder_requested.emit)
        self.projects_layout.addWidget(add_project_card)

        self._clear_layout(self.guide_layout)
        
        guide_tr = os.path.abspath("guide_TR.fountain")
        if os.path.exists(guide_tr):
            card = ProjectCard(tr("tr_guide"), guide_tr, "", is_guide=True)
            card.clicked.connect(self.open_project_requested.emit)
            self.guide_layout.addWidget(card)

        guide_en = os.path.abspath("guide_EN.fountain")
        if os.path.exists(guide_en):
            card = ProjectCard(tr("en_guide"), guide_en, "", is_guide=True)
            card.clicked.connect(self.open_project_requested.emit)
            self.guide_layout.addWidget(card)

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
