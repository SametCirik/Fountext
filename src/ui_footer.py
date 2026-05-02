from PyQt6.QtWidgets import QStatusBar, QLabel, QSlider, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from lang_controller import LanguageController, tr

class EditorFooterBar(QStatusBar):
    zoom_requested = pyqtSignal(int)

    def __init__(self, main_window, editor):
        super().__init__(main_window)
        self.main_window = main_window
        self.editor = editor
        
        self.current_page = 1
        self.total_pages = 1
        self.total_chars = 0
        
        self.save_status_label = QLabel(" ✔ ")
        self.save_status_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 14px;")
        self.addWidget(self.save_status_label)
        
        self.page_label = QLabel(f" {tr('footer_page')}: 1/1 ")
        self.char_label = QLabel(f" | {tr('footer_char')}: 0 ")
        
        self.addWidget(self.page_label)
        self.addWidget(self.char_label)
        
        self.right_widget = QWidget()
        self.right_layout = QHBoxLayout(self.right_widget)
        self.right_layout.setContentsMargins(0, 0, 10, 0)
        
        self.zoom_label = QLabel("Zoom: 100%")
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(50, 200)  
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(150)
        
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        
        self.right_layout.addWidget(self.zoom_label)
        self.right_layout.addWidget(self.zoom_slider)
        
        self.addPermanentWidget(self.right_widget)
        
        # Dil değiştiğinde etiketleri yenile
        LanguageController().language_changed.connect(self.update_texts)

    def update_stats(self, current_page=None, total_pages=None, total_chars=None):
        if current_page is not None:
            self.current_page = current_page
        if total_pages is not None:
            self.total_pages = total_pages
        if total_chars is not None:
            self.total_chars = total_chars
            
        self.page_label.setText(f" {tr('footer_page')}: {self.current_page}/{self.total_pages} ")
        self.char_label.setText(f" | {tr('footer_char')}: {self.total_chars} ")

    def update_texts(self):
        # Sadece istatistik fonksiyonunu çağırarak metinleri güncel dille yeniden yazdırıyoruz
        self.update_stats()

    def set_saved_status(self, is_saved):
        if is_saved:
            self.save_status_label.setText(" ✔ ")
            self.save_status_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 14px;")
        else:
            self.save_status_label.setText(" ● ")
            self.save_status_label.setStyleSheet("color: #F44336; font-weight: bold; font-size: 14px;")

    def _on_zoom_changed(self, value):
        self.zoom_label.setText(f"Zoom: {value}%")
        self.zoom_requested.emit(value)
