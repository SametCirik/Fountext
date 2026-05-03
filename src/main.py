import sys
import os
import hashlib
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QStackedWidget
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtGui import QFontDatabase, QCloseEvent, QPainter, QPageSize, QPageLayout, QPixmap
from PyQt6.QtCore import Qt, QRectF, QMarginsF

from ui_paper import Workspace
from ui_menu import EditorMenuBar
from ui_toolbar import EditorToolBar
from ui_footer import EditorFooterBar
from ui_navigator import SceneNavigator  
from ui_home import HomeMenu, DATA_DIR
from ui_projects import ProjectDashboard
from ui_schema import SchemaEditor
from lang_controller import LanguageController, tr

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.base_title = "Fountext"
        self.is_saved = True  
        self.resize(1100, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # ==========================================
        # EKRAN 0: Ana Menü
        # ==========================================
        self.home_menu = HomeMenu()
        
        self.home_menu.open_project_requested.connect(self.open_file_from_path)
        self.home_menu.new_project_requested.connect(self.new_file)
        self.home_menu.browse_project_requested.connect(self.open_file)
        
        self.home_menu.create_folder_requested.connect(self.create_project_folder)
        self.home_menu.open_folder_requested.connect(self.open_project_dashboard)

        self.stacked_widget.addWidget(self.home_menu)

        # ==========================================
        # EKRAN 1: Çalışma Alanı (Editör)
        # ==========================================
        self.workspace = Workspace()
        self.stacked_widget.addWidget(self.workspace)
        
        # ==========================================
        # EKRAN 2: Proje Yönetim Paneli
        # ==========================================
        self.project_dashboard = ProjectDashboard()
        self.project_dashboard.back_requested.connect(self.show_home_screen)
        self.project_dashboard.open_episode_requested.connect(self.open_file_from_path)
        
        self.stacked_widget.addWidget(self.project_dashboard)

        # ==========================================
        # EKRAN 3: Şema (Dedektif Panosu)
        # ==========================================
        self.schema_editor = SchemaEditor()
        self.schema_editor.back_requested.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        
        self.stacked_widget.addWidget(self.schema_editor)
        
        self.project_dashboard.open_schema_requested.connect(self.open_schema_board)

        self.navigator = SceneNavigator(self.workspace, self.workspace)
        self.navigator.hide()  
        
        editor_reference = self.workspace

        self.menu_bar = EditorMenuBar(self, editor_reference)
        self.setMenuBar(self.menu_bar)

        self.toolbar = EditorToolBar(self, editor_reference)
        self.addToolBar(self.toolbar)

        self.footer = EditorFooterBar(self, editor_reference)
        self.setStatusBar(self.footer)

        self.footer.zoom_requested.connect(self.workspace.set_zoom)

        self.current_file_path = None   
        
        self.show_home_screen()
        LanguageController().language_changed.connect(self.update_texts_on_lang_change)

    # --- PROJE KAYIT (REGISTRY) SİSTEMİ ---
    def register_project(self, folder_path):
        projects_file = "user_data/projects.json"
        if not os.path.exists("user_data"):
            os.makedirs("user_data")
            
        projects = []
        if os.path.exists(projects_file):
            with open(projects_file, 'r', encoding='utf-8') as f:
                try:
                    projects = json.load(f)
                except:
                    pass
                    
        if folder_path not in projects:
            projects.append(folder_path)
            with open(projects_file, 'w', encoding='utf-8') as f:
                json.dump(projects, f, ensure_ascii=False, indent=4)

    def open_project_dashboard(self, folder_path=None):
        if not folder_path:
            folder_path = QFileDialog.getExistingDirectory(self, "Fountext Proje Klasörünü Seç")
            
        if folder_path:
            self.register_project(folder_path)
            self.project_dashboard.load_project(folder_path)
            self.stacked_widget.setCurrentIndex(2)

    def create_project_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Yeni Proje İçin Boş Bir Klasör Seç")
        if folder_path:
            self.open_project_dashboard(folder_path)

    # --- PENCERE VE EKRAN YÖNETİM FONKSİYONLARI ---

    def toggle_navigator(self):
        if self.navigator.isVisible():
            self.navigator.hide()
        else:
            self.navigator.show()

    def resizeEvent(self, event: QCloseEvent):
        super().resizeEvent(event)
        if hasattr(self, 'navigator') and self.workspace:
            self.navigator.setGeometry(0, 0, self.navigator.width(), self.workspace.height())

    def update_texts_on_lang_change(self):
        if not self.current_file_path and self.base_title.startswith(tr("untitled_filename", default="İsimsiz")):
            self.base_title = tr("untitled_filename") + ".fountain"
        self.update_window_title()

    def update_window_title(self):
        prefix = "*" if not self.is_saved else ""
        self.setWindowTitle(f"{prefix}{self.base_title} - Fountext Editor v1.2")

    def show_home_screen(self):
        self.stacked_widget.setCurrentIndex(0)
        self.menu_bar.hide()
        self.toolbar.hide()
        self.footer.hide()
        if self.navigator.isVisible():
            self.navigator.hide()
        self.home_menu.load_projects()  
        self.setWindowTitle("Fountext - Ana Menü")

    def show_editor_screen(self):
        self.stacked_widget.setCurrentIndex(1)
        self.menu_bar.show()
        self.toolbar.show()
        self.footer.show()
        self.update_window_title()

    # --- DOSYA İŞLEMLERİ (AÇMA / YÜKLEME) ---

    def open_file_from_path(self, path):
        if self._load_file(path):
            self.show_editor_screen()

    def _load_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().replace('\r\n', '\n').replace('\r', '').replace('\t', '   ')
            
            lines = content.split('\n')
            title_lines = []
            script_lines = []
            in_title = True
            has_title_data = False

            for line in lines:
                if in_title:
                    if line.strip() == "":
                        if has_title_data:
                            in_title = False  
                        else:
                            title_lines.append(line)
                    elif ":" in line and line.find(":") < 15:
                        has_title_data = True
                        title_lines.append(line)
                    elif has_title_data:
                        title_lines.append(line)
                    else:
                        in_title = False
                        script_lines.append(line)
                else:
                    script_lines.append(line)

            self.workspace.hidden_editor.blockSignals(True)  
            if not has_title_data:
                self.workspace.title_text = ""
                self.workspace.hidden_editor.setPlainText(content)
            else:
                self.workspace.title_text = "\n".join(title_lines) + "\n\n"
                self.workspace.hidden_editor.setPlainText("\n".join(script_lines))
            self.workspace.hidden_editor.blockSignals(False)
            
            self.current_file_path = file_path
            self.base_title = os.path.basename(file_path)
            
            self.workspace._sync_text()  
            self.mark_saved()  
            
            print(f"Dosya açıldı: {file_path}")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Dosya açılamadı:\n{str(e)}")
            return False

    def new_file(self):
        if not self.check_unsaved_changes():
            return

        self.workspace.hidden_editor.blockSignals(True)
        self.workspace.hidden_editor.clear()
        self.workspace.raw_text = ""
        self.workspace.title_text = "Title: [SENARYO ADI]\nCredit: Yazan\nAuthor: [İsim Soyisim]\nDate: 10 Nisan 2026\nCopyright: (c) 2026\nWatermark: \nContact: \nTelefon Numarası\nE-Posta Adresi\n\n"
        self.workspace.hidden_editor.blockSignals(False)

        self.current_file_path = None
        self.base_title = tr("untitled_filename") + ".fountain"
        self.workspace.update_layout()
        
        self.mark_saved()
        print("Yeni dosya açıldı.")
        
        self.show_editor_screen()

    def open_file(self):
        if not self.check_unsaved_changes():
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Fountain Dosyası Aç", "", "Fountain Dosyaları (*.fountain);;Tüm Dosyalar (*)"
        )
        
        if file_path:
            if self._load_file(file_path):
                self.show_editor_screen()

    # --- DOSYA İŞLEMLERİ (KAYDETME / DIŞA AKTARMA) ---

    def save_thumbnail(self):
        if not self.current_file_path: return
        
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            
        file_hash = hashlib.md5(self.current_file_path.encode('utf-8')).hexdigest()
        img_path = os.path.join(DATA_DIR, f"{file_hash}.png")
        data_path = os.path.join(DATA_DIR, f"{file_hash}.json")
        
        engine = self.workspace.engine
        rect = QRectF(0, 0, engine.page_width, engine.page_height)
        pixmap = QPixmap(int(engine.page_width), int(engine.page_height))
        pixmap.fill(Qt.GlobalColor.white)
        
        painter = QPainter(pixmap)
        self.workspace.scene.render(painter, target=QRectF(pixmap.rect()), source=rect)
        painter.end()
        
        pixmap.scaled(140, 198, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation).save(img_path, "PNG")
        
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump({
                "path": self.current_file_path,  
                "name": self.base_title.replace('.fountain', '')
            }, f)

    def mark_unsaved(self):
        if self.is_saved:
            self.is_saved = False
            self.update_window_title()
            self.footer.set_saved_status(False)

    def mark_saved(self):
        self.is_saved = True
        self.update_window_title()
        self.footer.set_saved_status(True)

    def check_unsaved_changes(self):
        if self.is_saved:
            return True
            
        reply = QMessageBox.warning(
            self, 'Kaydedilmemiş Değişiklikler',
            f"'{self.base_title}' belgesinde kaydedilmemiş değişiklikler var.\nKaydetmek ister misiniz?",
            QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Save
        )

        if reply == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif reply == QMessageBox.StandardButton.Discard:
            return True
        else:
            return False

    def closeEvent(self, event: QCloseEvent):
        if self.check_unsaved_changes():
            event.accept()
        else:
            event.ignore()

    def save_file(self):
        if not self.current_file_path:
            self.current_file_path, _ = QFileDialog.getSaveFileName(
                self, "Fountain Kaydet", "", "Fountain Dosyaları (*.fountain)"
            )

        if self.current_file_path:
            try:
                if not self.current_file_path.endswith('.fountain'):
                    self.current_file_path += '.fountain'

                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    file.write(self.workspace.title_text + self.workspace.raw_text)
                
                self.base_title = os.path.basename(self.current_file_path)
                self.mark_saved()  
                
                self.save_thumbnail()
                
                print(f"Başarıyla kaydedildi: {self.current_file_path}")
                return True
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{str(e)}")
                return False
        return False  

    def export_pdf(self):
        default_name = self.base_title.replace('.fountain', '') + ".pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "PDF Olarak Dışa Aktar", default_name, "PDF Dosyaları (*.pdf)"
        )

        if not file_path:
            return

        try:
            # 1. İmleci gizle
            if self.workspace.cursor_item:
                self.workspace.cursor_item.setVisible(False)
                
            # 2. Seçimi tamamen iptal et ve sahnedeki renkleri anında temizle
            cursor = self.workspace.hidden_editor.textCursor()
            cursor.clearSelection()
            self.workspace.hidden_editor.setTextCursor(cursor)
            self.workspace.update_selection_highlights()
            QApplication.processEvents() # Tüm silme işlemlerinin render edildiğinden emin ol

            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(file_path)
            
            printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            
            layout = printer.pageLayout()
            layout.setMargins(QMarginsF(0, 0, 0, 0))
            printer.setPageLayout(layout)

            painter = QPainter(printer)
            
            engine = self.workspace.engine
            page_height = engine.page_height
            page_width = engine.page_width
            spacing = 50  
            
            full_text = self.workspace.title_text + self.workspace.raw_text
            pages = engine.paginate_text(full_text)
            total_pages = len(pages)

            for i in range(total_pages):
                if i > 0:
                    printer.newPage()  
                    
                y_offset = i * (page_height + spacing)
                source_rect = QRectF(0, y_offset, page_width, page_height)
                
                target_rect = QRectF(0, 0, printer.width(), printer.height())
                
                self.workspace.scene.render(painter, target_rect, source_rect)

            painter.end()

            # 3. İşlem bittikten sonra imleci geri aç (seçimi getirme)
            if self.workspace.cursor_item:
                self.workspace.cursor_item.setVisible(True)
                self.workspace.cursor_timer.start(500)

            QMessageBox.information(self, "Başarılı", f"PDF başarıyla oluşturuldu:\n{file_path}")
            
        except Exception as e:
            if self.workspace.cursor_item:
                self.workspace.cursor_item.setVisible(True)
                self.workspace.cursor_timer.start(500)
                
            QMessageBox.critical(self, "Hata", f"PDF oluşturulurken bir hata meydana geldi:\n{str(e)}")  

    def open_schema_board(self, project_path):
        self.schema_editor.load_schema(project_path)
        self.stacked_widget.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from PyQt6.QtGui import QIcon
    app.setWindowIcon(QIcon("Fountext_Logo.png"))
    
    QFontDatabase.addApplicationFont("assets/fonts/CourierPrime-Regular.ttf")
    QFontDatabase.addApplicationFont("assets/fonts/CourierPrime-Bold.ttf")
    QFontDatabase.addApplicationFont("assets/fonts/CourierPrime-Italic.ttf")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
