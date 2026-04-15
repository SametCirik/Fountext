from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt6.QtCore import Qt

class ResizeGrip(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_widget = parent
        self.setFixedWidth(2) # Çok da kalın olmayan, 2 piksellik ince bir çizgi
        self.setCursor(Qt.CursorShape.SplitHCursor)
        
        # YENİ: Menü barlarına uyumlu ince beyaz/açık gri sınır çizgisi
        self.setStyleSheet("""
            QWidget {
                background-color: #cccccc; /* İnce beyaz görünüm */
            }
            QWidget:hover {
                background-color: #6c9aed; /* Fareyle üzerine gelince etkileşim mavisini koruduk */
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_x = event.globalPosition().x()
            self.start_width = self.parent_widget.width()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta_x = event.globalPosition().x() - self.drag_start_x
            new_width = max(150, min(self.start_width + delta_x, 600))
            self.parent_widget.setFixedWidth(int(new_width))

class SceneNavigator(QWidget):
    def __init__(self, parent_widget, workspace):
        super().__init__(parent_widget)
        self.workspace = workspace

        self.setFixedWidth(260)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.list_widget = QListWidget()
        
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #b0b0b0;
                border: none;
                font-family: 'Courier Prime', Courier, monospace;
                font-size: 10pt;
            }
            QListWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #282828;
            }
            QListWidget::item:selected {
                background-color: #2b2b2b;
                color: #ffffff;
                border-left: 3px solid #d4d4d4;
            }
            QListWidget::item:hover {
                background-color: #252525;
            }
        """)
        
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        
        self.grip = ResizeGrip(self)
        
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.grip)

    def update_scenes(self, scenes):
        self.list_widget.clear()
        for text, y_pos in scenes:
            item = QListWidgetItem(text.strip())
            item.setData(Qt.ItemDataRole.UserRole, y_pos)
            self.list_widget.addItem(item)

    def on_item_clicked(self, item):
        y_pos = item.data(Qt.ItemDataRole.UserRole)
        target_y = max(0, int(y_pos) - 50) 
        
        scrollbar = self.workspace.verticalScrollBar()
        scrollbar.setValue(target_y)