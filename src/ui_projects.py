import os
import json
import shutil
import re
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QTextEdit, 
                             QFileDialog, QInputDialog, QMessageBox)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt, pyqtSignal
from lang_controller import LanguageController, tr

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

class ProjectDashboard(QWidget):
    back_requested = pyqtSignal()
    open_episode_requested = pyqtSignal(str) 
    # --- YENİ SİNYAL: Şema ekranına geçiş için ---
    open_schema_requested = pyqtSignal(str) 

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #1e1e1e;")
        self.project_path = ""
        self.metadata_path = ""
        self.poster_path = ""
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(40)

        # ==========================================
        # SOL PANEL: Afiş, Senaryo Adı ve Sinopsis
        # ==========================================
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        top_info_layout = QHBoxLayout()
        
        self.poster_label = ClickableLabel()
        self.poster_label.setFixedSize(240, 340)
        self.poster_label.setStyleSheet("background-color: #2b2b2b; border: 2px dashed #555; border-radius: 8px;")
        self.poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.poster_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.poster_label.clicked.connect(self.change_poster)
        
        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(0)
        
        self.btn_back = QPushButton(tr("proj_back_btn"))
        self.btn_back.setStyleSheet("QPushButton { background-color: transparent; font-size: 15px; border: none; color: #a0a0a0; font-weight: bold; text-align: left; padding: 0px; } QPushButton:hover { color: white; }")
        self.btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_back.clicked.connect(self.back_requested.emit)
        
        self.title_label = QLabel("Proje Adı")
        self.title_label.setStyleSheet("color: #e5a040; font-size: 42px; font-weight: bold; font-family: sans-serif; border: none; margin-top: 5px;") 
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.date_label = QLabel(f"{tr("proj_created")} -")
        self.date_label.setStyleSheet("color: #777; font-size: 14px; border: none; margin-bottom: 5px;")
        
        title_vbox.addWidget(self.btn_back)
        title_vbox.addWidget(self.title_label)
        title_vbox.addWidget(self.date_label)
        title_vbox.addStretch() 
        
        top_info_layout.addWidget(self.poster_label)
        top_info_layout.addLayout(title_vbox)
        left_layout.addLayout(top_info_layout)
        
        # --- Sol Alt Kısım: Sinopsis ---
        sinopsis_header = QHBoxLayout()
        sinopsis_label = QLabel(tr("proj_synopsis"))
        sinopsis_label.setStyleSheet("color: #a0a0a0; font-size: 20px; font-weight: bold; border: none;")
        
        self.btn_save_info = QPushButton(tr("proj_save_info"))
        self.btn_save_info.setStyleSheet("background-color: #3b3b3b; color: white; border-radius: 4px; border: none; padding: 5px 10px; font-weight:bold;")
        self.btn_save_info.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save_info.clicked.connect(self.save_metadata)
        
        sinopsis_header.addWidget(sinopsis_label)
        sinopsis_header.addStretch()
        sinopsis_header.addWidget(self.btn_save_info)
        
        left_layout.addLayout(sinopsis_header)
        left_layout.addSpacing(10)
        
        self.synopsis_text = QTextEdit()
        self.synopsis_text.setStyleSheet("""
            QTextEdit {
                background-color: #252525; color: #d3d3d3;
                border: 1px solid #3b3b3b; border-radius: 8px;
                padding: 15px; font-size: 16px; line-height: 1.5;
            }
            QScrollBar:vertical { background: #1e1e1e; width: 10px; }
            QScrollBar::handle:vertical { background: #3b3b3b; border-radius: 5px; }
        """)
        left_layout.addWidget(self.synopsis_text)
        
        # ==========================================
        # SAĞ PANEL: Şema ve Bölümler
        # ==========================================
        right_panel = QFrame()
        right_panel.setStyleSheet("background-color: #252525; border-radius: 12px; border: 1px solid #333;")
        right_panel.setFixedWidth(350)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)

        # --- YENİ: DEDEKTİF PANOSU BUTONU ---
        self.btn_schema = QPushButton(tr("proj_schema_btn"))
        self.btn_schema.setStyleSheet("""
            QPushButton {
                background-color: #8b1c1c; color: white; font-weight: bold; 
                border-radius: 5px; padding: 12px; border: 1px solid #a32222; font-size: 14px;
            }
            QPushButton:hover { background-color: #a32222; }
        """)
        self.btn_schema.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_schema.clicked.connect(lambda: self.open_schema_requested.emit(self.project_path))
        right_layout.addWidget(self.btn_schema)

        # Araya ince bir çizgi (Separator)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("border: 1px solid #3b3b3b;")
        right_layout.addWidget(line)
        
        episodes_title = QLabel(tr("proj_episodes"))
        episodes_title.setStyleSheet("color: white; font-size: 20px; font-weight: bold; border: none;")
        episodes_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(episodes_title)
        
        self.btn_add_episode = QPushButton(tr("proj_add_episode"))
        self.btn_add_episode.setStyleSheet("""
            QPushButton {
                background-color: #e5a040; color: #1e1e1e; font-weight: bold; 
                border-radius: 5px; padding: 10px; border: none; font-size: 14px;
            }
            QPushButton:hover { background-color: #f6b65a; }
        """)
        self.btn_add_episode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_episode.clicked.connect(self.create_new_episode)
        right_layout.addWidget(self.btn_add_episode) 
        
        self.episodes_scroll = QScrollArea()
        self.episodes_scroll.setWidgetResizable(True)
        self.episodes_scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { background: #252525; width: 8px; }
            QScrollBar::handle:vertical { background: #444; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #e5a040; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: none; border: none; }
        """)
        
        self.episodes_container = QWidget()
        self.episodes_container.setStyleSheet("background-color: transparent;")
        self.episodes_vbox = QVBoxLayout(self.episodes_container)
        self.episodes_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.episodes_vbox.setContentsMargins(0, 0, 10, 0)
        self.episodes_vbox.setSpacing(10)
        
        self.episodes_scroll.setWidget(self.episodes_container)
        right_layout.addWidget(self.episodes_scroll)
        
        main_layout.addWidget(left_panel, stretch=7)
        
        
        main_layout.addWidget(right_panel, stretch=3)
        LanguageController().language_changed.connect(self.update_texts)

    def update_texts(self):
        self.btn_back.setText(tr("proj_back_btn"))
        self.btn_save_info.setText(tr("proj_save_info"))
        self.btn_schema.setText(tr("proj_schema_btn"))
        self.btn_add_episode.setText(tr("proj_add_episode"))

        LanguageController().language_changed.connect(self.update_texts)

    def update_texts(self):
        self.btn_back.setText(tr("proj_back_btn"))
        self.btn_save_info.setText(tr("proj_save_info"))
        self.btn_schema.setText(tr("proj_schema_btn"))
        self.btn_add_episode.setText(tr("proj_add_episode"))


    def natural_keys(self, text):
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

    def load_project(self, folder_path):
        self.project_path = folder_path
        fountext_dir = os.path.join(folder_path, ".fountext")
        self.metadata_path = os.path.join(fountext_dir, "project.json")
        self.poster_path = os.path.join(fountext_dir, "poster.png")
        
        if not os.path.exists(fountext_dir):
            os.makedirs(fountext_dir)
            
        if not os.path.exists(self.metadata_path):
            default_data = {
                "title": os.path.basename(folder_path),
                "created_at": datetime.now().strftime("%Y-%m-%d"),
                "synopsis": "Bu hikayenin bir sinopsisi henüz yazılmadı..."
            }
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=4)
                
        with open(self.metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        self.title_label.setText(data.get("title", "Bilinmeyen Proje"))
        self.date_label.setText(f"Oluşturulma: {data.get('created_at', '-')}")
        self.synopsis_text.setText(data.get("synopsis", ""))
        
        if os.path.exists(self.poster_path):
            pixmap = QPixmap(self.poster_path)
            self.poster_label.setPixmap(pixmap.scaled(240, 340, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
            self.poster_label.setStyleSheet("border: none; border-radius: 8px;")
        else:
            self.poster_label.clear()
            self.poster_label.setText(tr("proj_add_poster"))
            self.poster_label.setStyleSheet("background-color: #2b2b2b; color: #a0a0a0; font-weight: bold; border: 2px dashed #555; border-radius: 8px;")
            
        self.scan_episodes()

    def scan_episodes(self):
        while self.episodes_vbox.count():
            child = self.episodes_vbox.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        fountain_files = []
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.endswith('.fountain'):
                    fountain_files.append(os.path.join(root, file))
                    
        if not fountain_files:
            empty_lbl = QLabel(tr("proj_no_episodes"))
            empty_lbl.setStyleSheet("color: #777; font-style: italic; border: none;")
            self.episodes_vbox.addWidget(empty_lbl)
        else:
            fountain_files.sort(key=lambda x: self.natural_keys(os.path.basename(x)))

            for file_path in fountain_files:
                file_name = os.path.basename(file_path).replace('.fountain', '')
                btn = QPushButton(file_name)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #333333; color: white; border-radius: 5px; 
                        padding: 15px; text-align: left; border: 1px solid #444;
                        font-size: 14px; font-weight: bold;
                    }
                    QPushButton:hover { background-color: #444444; border-color: #e5a040; }
                """)
                btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                btn.clicked.connect(lambda checked, p=file_path: self.open_episode_requested.emit(p))
                self.episodes_vbox.addWidget(btn)

    def create_new_episode(self):
        if not self.project_path: return
        
        text, ok = QInputDialog.getText(self, 'Yeni Bölüm', 'Bölüm Adını Girin:\n(Örn: 1-Pilot Bölüm)')
        
        if ok and text:
            clean_name = re.sub(r'[\\/*?:"<>|]', "", text)
            if not clean_name: return
            
            episodes_dir = os.path.join(self.project_path, "Episodes")
            if not os.path.exists(episodes_dir):
                os.makedirs(episodes_dir)
                
            new_file_path = os.path.join(episodes_dir, f"{clean_name}.fountain")
            
            if os.path.exists(new_file_path):
                QMessageBox.warning(self, "Hata", "Bu isimde bir bölüm zaten var!")
                return
                
            template = f"Title: {clean_name}\nCredit: {tr(tp_default_credit)}\nAuthor: {tr(tp_default_author)}\n\n{tr(proj_start_writing)}"
            
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(template)
                
            self.scan_episodes()

    def save_metadata(self):
        if not self.metadata_path: return
        
        with open(self.metadata_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        data["synopsis"] = self.synopsis_text.toPlainText()
        
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        self.btn_save_info.setText("Kaydedildi ✓")
        self.btn_save_info.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 4px; border: none; padding: 5px 10px; font-weight:bold;")
        
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.btn_save_info.setText(tr("proj_save_info")))
        QTimer.singleShot(2000, lambda: self.btn_save_info.setStyleSheet("background-color: #3b3b3b; color: white; border-radius: 4px; border: none; padding: 5px 10px; font-weight:bold;"))

    def change_poster(self):
        if not self.project_path: return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Afiş Resmi Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)"
        )
        
        if file_path:
            shutil.copy2(file_path, self.poster_path)
            pixmap = QPixmap(self.poster_path)
            self.poster_label.setPixmap(pixmap.scaled(240, 340, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
            self.poster_label.setStyleSheet("border: none; border-radius: 8px;")