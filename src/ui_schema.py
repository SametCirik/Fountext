import os
import json
import shutil
import uuid
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QGraphicsView, QGraphicsScene, QGraphicsRectItem, 
                             QGraphicsLineItem, QGraphicsTextItem, QInputDialog, 
                             QFileDialog, QMenu, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QBrush, QColor, QPen, QCursor, QFont, QPainter, QPixmap, QPainterPath

# ==========================================
# İP VE RAPTİYE (Daima En Üstte)
# ==========================================
class StringEdge(QGraphicsLineItem):
    def __init__(self, source, dest, color_hex, editor):
        super().__init__()
        self.source = source
        self.dest = dest
        self.color_hex = color_hex
        self.editor = editor

        self.setZValue(1000)
        self.setPen(QPen(QColor(self.color_hex), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        self.source.edges.append(self)
        self.dest.edges.append(self)
        self.update_position()

    def update_position(self):
        p1 = self.source.sceneBoundingRect().center()
        p2 = self.dest.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        
        painter.setBrush(QBrush(QColor("#d3d3d3"))) 
        painter.setPen(QPen(QColor("#1e1e1e"), 1.5))
        line = self.line()
        painter.drawEllipse(line.p1(), 5, 5)
        painter.drawEllipse(line.p2(), 5, 5)

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setStyleSheet("QMenu { background-color: #2b2b2b; color: white; border: 1px solid #555; } QMenu::item:selected { background-color: #e53935; color: white; }")
        
        del_action = menu.addAction("✂️ İpi Kes")
        action = menu.exec(event.screenPos())
        
        if action == del_action:
            self.delete_edge()

    def delete_edge(self):
        if self in self.source.edges: self.source.edges.remove(self)
        if self in self.dest.edges: self.dest.edges.remove(self)
        if self in self.editor.edges: self.editor.edges.remove(self)
        self.scene().removeItem(self)

# ==========================================
# BÖLGE/GRUP KUTUSU (En Arkada - Yarı Saydam)
# ==========================================
class GroupBoxNode(QGraphicsRectItem):
    def __init__(self, node_id, x, y, w, h, color_hex, editor):
        super().__init__(0, 0, w, h)
        self.node_id = node_id if node_id else uuid.uuid4().hex
        self.setPos(x, y)
        self.editor = editor
        self.color_hex = color_hex
        self.w = w
        self.h = h

        self.setZValue(-100)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)

        self._update_style()

    def _update_style(self):
        bg_color = QColor(self.color_hex)
        bg_color.setAlpha(30)
        self.setBrush(QBrush(bg_color))

    def paint(self, painter, option, widget):
        self._update_style()
        pen_color = QColor("#ffffff") if self.isSelected() else QColor(self.color_hex)
        painter.setPen(QPen(pen_color, 4, Qt.PenStyle.DashLine))
        painter.drawRect(self.boundingRect())

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setStyleSheet("QMenu { background-color: #2b2b2b; color: white; border: 1px solid #555; } QMenu::item:selected { background-color: #6c9aed; color: #1e1e1e; }")

        resize_action = menu.addAction("📐 Boyutlandır")
        color_action = menu.addAction("🎨 Rengini Değiştir")
        del_action = menu.addAction("🗑️ Bölgeyi Sil")

        action = menu.exec(event.screenPos())

        if action == resize_action:
            text, ok = QInputDialog.getText(None, "Bölge Boyutu", "Yeni genişlik ve yüksekliği araya virgül koyarak yazın:\nÖrn: 1200,800", text=f"{int(self.w)},{int(self.h)}")
            if ok and "," in text:
                try:
                    parts = text.split(",")
                    w, h = int(parts[0].strip()), int(parts[1].strip())
                    self.w, self.h = w, h
                    self.setRect(0, 0, w, h)
                    self.update()
                except ValueError:
                    pass
        elif action == color_action:
            colors = {"Kan Kırmızısı": "#e53935", "Derin Mavi": "#1e88e5", "Zehir Yeşili": "#43a047", "Altın Sarısı": "#fdd835", "Mor": "#8e24aa", "Karanlık Gri": "#555555"}
            color_name, ok = QInputDialog.getItem(None, "Bölge Rengi", "Hangi renk olsun?", list(colors.keys()), 0, False)
            if ok and color_name:
                self.color_hex = colors[color_name]
                self.update()
        elif action == del_action:
            self.scene().removeItem(self)

# ==========================================
# KARAKTER KARTI (Resimli ve Ön Bellekli - Caching)
# ==========================================
class CharacterNode(QGraphicsRectItem):
    def __init__(self, node_id, text, x, y, schema_dir, editor, image_file=""):
        super().__init__(0, 0, 140, 200)
        self.node_id = node_id if node_id else uuid.uuid4().hex
        self.setPos(x, y)
        self.schema_dir = schema_dir
        self.editor = editor
        self.image_file = image_file
        self.text = text
        
        self.edges = [] 
        self.is_link_source = False 
        
        self.cached_pixmap = None 
        self.load_image_to_cache() 
        
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def load_image_to_cache(self):
        if self.image_file:
            full_img_path = os.path.join(self.schema_dir, "images", self.image_file)
            if os.path.exists(full_img_path):
                self.cached_pixmap = QPixmap(full_img_path).scaled(
                    120, 140, 
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                    Qt.TransformationMode.SmoothTransformation
                )
            else:
                self.cached_pixmap = None
        else:
            self.cached_pixmap = None

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.GraphicsItemChange.ItemPositionChange:
            for edge in self.edges:
                edge.update_position()
        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(QColor("#2b2b2b")))
        
        if self.is_link_source:
            painter.setPen(QPen(QColor("#ffffff"), 3, Qt.PenStyle.DashLine))
        else:
            pen_color = QColor("#e5a040") if self.isSelected() else QColor("#555555")
            painter.setPen(QPen(pen_color, 2))
            
        painter.drawRoundedRect(self.boundingRect(), 8, 8)

        img_rect = QRectF(10, 10, 120, 140)

        if self.cached_pixmap:
            path = QPainterPath()
            path.addRoundedRect(img_rect, 4, 4)
            painter.setClipPath(path)
            
            px_x = img_rect.x() + (img_rect.width() - self.cached_pixmap.width()) / 2
            px_y = img_rect.y() + (img_rect.height() - self.cached_pixmap.height()) / 2
            painter.drawPixmap(int(px_x), int(px_y), self.cached_pixmap)
            painter.setClipping(False)
        else:
            painter.setBrush(QBrush(QColor("#1e1e1e")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(img_rect, 4, 4)
            
            painter.setPen(QPen(QColor("#555555")))
            painter.setFont(QFont("Courier Prime", 48, QFont.Weight.Bold))
            painter.drawText(img_rect, int(Qt.AlignmentFlag.AlignCenter), "?")

        text_rect = QRectF(5, 155, 130, 40)
        painter.setPen(QPen(QColor("#d3d3d3")))
        painter.setFont(QFont("sans-serif", 11, QFont.Weight.Bold))
        flags = int(Qt.AlignmentFlag.AlignCenter) | int(Qt.TextFlag.TextWordWrap)
        painter.drawText(text_rect, flags, self.text)

    def mousePressEvent(self, event):
        if self.editor.linking_mode:
            if self.editor.link_source is None:
                self.editor.link_source = self
                self.is_link_source = True
                self.update()
            else:
                if self.editor.link_source != self:
                    self.editor.create_edge(self.editor.link_source, self)
                self.editor.end_linking_mode()
            return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        new_text, ok = QInputDialog.getText(None, "Karakter Kartı", "Karakter İsmi:", text=self.text)
        if ok and new_text:
            self.text = new_text
            self.update()
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setStyleSheet("QMenu { background-color: #2b2b2b; color: white; border: 1px solid #555; } QMenu::item:selected { background-color: #e5a040; color: #1e1e1e; }")
        
        edit_action = menu.addAction("✏️ İsmi Düzenle")
        img_action = menu.addAction("🖼️ Resmi Değiştir")
        del_action = menu.addAction("🗑️ Kartı Sil")

        action = menu.exec(event.screenPos())
        
        if action == edit_action:
            self.mouseDoubleClickEvent(event)
        elif action == img_action:
            file_path, _ = QFileDialog.getOpenFileName(None, "Karakter Resmi Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)")
            if file_path:
                img_dir = os.path.join(self.schema_dir, "images")
                if not os.path.exists(img_dir): os.makedirs(img_dir)
                
                filename = os.path.basename(file_path)
                new_path = os.path.join(img_dir, filename)
                shutil.copy2(file_path, new_path)
                self.image_file = filename
                
                self.load_image_to_cache() 
                self.update()
        elif action == del_action:
            self.delete_node()

    def delete_node(self):
        for edge in list(self.edges):
            edge.delete_edge()
        self.scene().removeItem(self)

# ==========================================
# NOT KARTI (Sadece Metin)
# ==========================================
class NoteNode(QGraphicsRectItem):
    def __init__(self, node_id, text, x, y, editor):
        super().__init__(0, 0, 160, 160)
        self.node_id = node_id if node_id else uuid.uuid4().hex
        self.setPos(x, y)
        self.editor = editor
        self.text = text
        
        self.edges = []
        self.is_link_source = False
        
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsRectItem.GraphicsItemChange.ItemPositionChange:
            for edge in self.edges:
                edge.update_position()
        return super().itemChange(change, value)

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(QColor("#222222")))
        
        if self.is_link_source:
            painter.setPen(QPen(QColor("#ffffff"), 3, Qt.PenStyle.DashLine))
        else:
            pen_color = QColor("#f6b65a") if self.isSelected() else QColor("#e5a040")
            painter.setPen(QPen(pen_color, 2))
            
        painter.drawRect(self.boundingRect())

        text_rect = QRectF(10, 10, 140, 140)
        painter.setPen(QPen(QColor("#e5a040")))
        painter.setFont(QFont("sans-serif", 10))
        flags = int(Qt.AlignmentFlag.AlignTop) | int(Qt.AlignmentFlag.AlignLeft) | int(Qt.TextFlag.TextWordWrap)
        painter.drawText(text_rect, flags, self.text)

    def mousePressEvent(self, event):
        if self.editor.linking_mode:
            if self.editor.link_source is None:
                self.editor.link_source = self
                self.is_link_source = True
                self.update()
            else:
                if self.editor.link_source != self:
                    self.editor.create_edge(self.editor.link_source, self)
                self.editor.end_linking_mode()
            return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.edit_note()
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.setStyleSheet("QMenu { background-color: #222222; color: #e5a040; border: 1px solid #e5a040; } QMenu::item:selected { background-color: #e5a040; color: #1e1e1e; }")
        
        edit_action = menu.addAction("✏️ Notu Düzenle")
        del_action = menu.addAction("🗑️ Notu Sil")

        action = menu.exec(event.screenPos())
        if action == edit_action:
            self.edit_note()
        elif action == del_action:
            self.delete_node()

    def edit_note(self):
        new_text, ok = QInputDialog.getMultiLineText(None, "Not Kartı", "Notunuzu yazın:", text=self.text)
        if ok and new_text:
            self.text = new_text
            self.update()

    def delete_node(self):
        for edge in list(self.edges):
            edge.delete_edge()
        self.scene().removeItem(self)

# ==========================================
# YENİ: ÖZELLEŞTİRİLMİŞ GÖRÜNÜM (VIEW) MANTIĞI
# ==========================================
class SchemaView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        
        # --- YENİ: Sol Tık ile Seçim Kutusu (Rubber Band) ---
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Orta tuş kaydırma takibi için değişkenler
        self._is_panning = False
        self._pan_start_pos = None
        
        self.setStyleSheet("""
            QGraphicsView { border: none; background-color: #1e1e1e; }
            QScrollBar:vertical { background: #1a1a1a; width: 12px; }
            QScrollBar::handle:vertical { background: #3b3b3b; border-radius: 6px; }
            QScrollBar::handle:vertical:hover { background: #555555; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: none; border: none; }
            
            QScrollBar:horizontal { background: #1a1a1a; height: 12px; }
            QScrollBar::handle:horizontal { background: #3b3b3b; border-radius: 6px; }
            QScrollBar::handle:horizontal:hover { background: #555555; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { background: none; border: none; }
        """)

    # --- YENİ: ORTA TUŞ (TEKERLEK) İLE KAYDIRMA ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._is_panning = True
            self._pan_start_pos = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_panning:
            delta = event.pos() - self._pan_start_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self._pan_start_pos = event.pos()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """CTRL + Fare Tekerleği ile Zoom"""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            zoom_in_factor = 1.15
            zoom_out_factor = 1 / zoom_in_factor
            
            if event.angleDelta().y() > 0:
                zoom_factor = zoom_in_factor
            else:
                zoom_factor = zoom_out_factor
                
            self.scale(zoom_factor, zoom_factor)
        else:
            super().wheelEvent(event)

# ==========================================
# ANA ŞEMA EDİTÖRÜ (TUVAL)
# ==========================================
class SchemaEditor(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.project_path = ""
        self.schema_dir = ""
        self.data_file = ""
        
        self.edges = [] 
        self.linking_mode = False 
        self.link_source = None 
        self.link_color_hex = "#e53935"
        
        self.setStyleSheet("background-color: #1a1a1a;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- ÜST ARAÇ ÇUBUĞU ---
        toolbar = QWidget()
        toolbar.setStyleSheet("background-color: #252525; border-bottom: 1px solid #3b3b3b;")
        toolbar.setFixedHeight(60)
        toolbar_layout = QHBoxLayout(toolbar)
        
        self.btn_back = QPushButton("← Projeye Dön")
        self.btn_back.setStyleSheet("QPushButton { background-color: transparent; font-size: 15px; color: #a0a0a0; font-weight: bold; border: none; } QPushButton:hover { color: white; }")
        self.btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_back.clicked.connect(self.back_requested.emit)
        
        self.btn_add_char = QPushButton("+ Karakter")
        self.btn_add_char.setStyleSheet("background-color: #3b3b3b; color: white; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        self.btn_add_char.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_char.clicked.connect(self.add_character_node)

        self.btn_add_note = QPushButton("+ Not")
        self.btn_add_note.setStyleSheet("background-color: #3b3b3b; color: #e5a040; border: 1px solid #e5a040; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        self.btn_add_note.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_note.clicked.connect(self.add_note_node)

        self.btn_add_group = QPushButton("🔲 Bölge Ekle")
        self.btn_add_group.setStyleSheet("background-color: #3b3b3b; color: #b388ff; border: 1px solid #b388ff; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        self.btn_add_group.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_group.clicked.connect(self.add_group_node)

        self.btn_add_link = QPushButton("🔗 İp Çek")
        self.btn_add_link.setStyleSheet("background-color: #3b3b3b; color: #6c9aed; border: 1px solid #6c9aed; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        self.btn_add_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_link.clicked.connect(self.start_linking)

        self.btn_save = QPushButton("💾 Panoyu Kaydet")
        self.btn_save.setStyleSheet("background-color: #8b1c1c; color: white; padding: 8px 15px; border-radius: 4px; font-weight: bold;")
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.clicked.connect(self.save_schema)

        toolbar_layout.addWidget(self.btn_back)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.btn_add_char)
        toolbar_layout.addWidget(self.btn_add_note)
        toolbar_layout.addWidget(self.btn_add_group)
        toolbar_layout.addWidget(self.btn_add_link)
        toolbar_layout.addWidget(self.btn_save)
        
        main_layout.addWidget(toolbar)

        # --- SONSUZ TUVAL (GRAPHICS VIEW) ---
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-5000, -5000, 10000, 10000) 
        self.view = SchemaView(self.scene)
        main_layout.addWidget(self.view)

    def start_linking(self):
        colors = {"Kan Kırmızısı": "#e53935", "Derin Mavi": "#1e88e5", "Zehir Yeşili": "#43a047", "Altın Sarısı": "#fdd835", "Beyaz": "#ffffff"}
        color_name, ok = QInputDialog.getItem(self, "İp Rengi", "Hangi renk ip çekmek istiyorsun?", list(colors.keys()), 0, False)
        
        if ok and color_name:
            self.link_color_hex = colors[color_name]
            self.linking_mode = True
            self.link_source = None
            self.view.setCursor(Qt.CursorShape.CrossCursor) 

    def end_linking_mode(self):
        self.linking_mode = False
        if self.link_source:
            self.link_source.is_link_source = False
            self.link_source.update() 
        self.link_source = None
        self.view.setCursor(Qt.CursorShape.ArrowCursor)

    def create_edge(self, source, dest, color=None):
        for edge in self.edges:
            if (edge.source == source and edge.dest == dest) or (edge.source == dest and edge.dest == source):
                return
                
        edge_color = color if color else self.link_color_hex
        new_edge = StringEdge(source, dest, edge_color, self)
        self.edges.append(new_edge)
        self.scene.addItem(new_edge)

    def load_schema(self, project_path):
        self.project_path = project_path
        self.schema_dir = os.path.join(project_path, ".fountext", "schema")
        self.data_file = os.path.join(self.schema_dir, "schema.json")
        
        if not os.path.exists(self.schema_dir): os.makedirs(self.schema_dir)
        if not os.path.exists(os.path.join(self.schema_dir, "images")): os.makedirs(os.path.join(self.schema_dir, "images"))
            
        self.scene.clear() 
        self.edges.clear()
        self.view.resetTransform()
        
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    node_map = {} 
                    
                    for node_data in data.get("nodes", []):
                        n_id = node_data.get("id", uuid.uuid4().hex)
                        if node_data.get("type") == "character":
                            node = CharacterNode(n_id, node_data.get("text", ""), node_data.get("x", 0), node_data.get("y", 0), self.schema_dir, self, node_data.get("image_file", ""))
                            self.scene.addItem(node)
                            node_map[n_id] = node
                        elif node_data.get("type") == "note":
                            node = NoteNode(n_id, node_data.get("text", ""), node_data.get("x", 0), node_data.get("y", 0), self)
                            self.scene.addItem(node)
                            node_map[n_id] = node
                        elif node_data.get("type") == "group":
                            node = GroupBoxNode(n_id, node_data.get("x", 0), node_data.get("y", 0), node_data.get("w", 500), node_data.get("h", 500), node_data.get("color", "#1e88e5"), self)
                            self.scene.addItem(node)
                            
                    for edge_data in data.get("edges", []):
                        source_node = node_map.get(edge_data["source_id"])
                        dest_node = node_map.get(edge_data["dest_id"])
                        if source_node and dest_node:
                            self.create_edge(source_node, dest_node, edge_data["color"])
                            
                except Exception as e:
                    print(f"Şema yüklenemedi: {e}")

    def add_character_node(self):
        center = self.view.mapToScene(self.view.viewport().rect().center())
        node = CharacterNode(None, "Karakter Adı", center.x() - 70, center.y() - 100, self.schema_dir, self)
        self.scene.addItem(node)

    def add_note_node(self):
        center = self.view.mapToScene(self.view.viewport().rect().center())
        node = NoteNode(None, "Yeni bir not, ipucu veya bölüm fikri...", center.x() - 80, center.y() - 80, self)
        self.scene.addItem(node)

    def add_group_node(self):
        colors = {"Kan Kırmızısı": "#e53935", "Derin Mavi": "#1e88e5", "Zehir Yeşili": "#43a047", "Altın Sarısı": "#fdd835", "Mor": "#8e24aa", "Karanlık Gri": "#555555"}
        color_name, ok = QInputDialog.getItem(self, "Bölge Rengi", "Hangi renk bir bölge eklemek istiyorsun?", list(colors.keys()), 1, False)
        
        if ok and color_name:
            center = self.view.mapToScene(self.view.viewport().rect().center())
            node = GroupBoxNode(None, center.x() - 300, center.y() - 250, 600, 500, colors[color_name], self)
            self.scene.addItem(node)

    def save_schema(self):
        nodes_data = []
        for item in self.scene.items():
            if isinstance(item, CharacterNode):
                nodes_data.append({
                    "id": item.node_id,
                    "type": "character",
                    "text": item.text,
                    "image_file": item.image_file,
                    "x": item.pos().x(),
                    "y": item.pos().y()
                })
            elif isinstance(item, NoteNode):
                nodes_data.append({
                    "id": item.node_id,
                    "type": "note",
                    "text": item.text,
                    "x": item.pos().x(),
                    "y": item.pos().y()
                })
            elif isinstance(item, GroupBoxNode):
                nodes_data.append({
                    "id": item.node_id,
                    "type": "group",
                    "x": item.pos().x(),
                    "y": item.pos().y(),
                    "w": item.w,
                    "h": item.h,
                    "color": item.color_hex
                })
                
        edges_data = []
        for edge in self.edges:
            edges_data.append({
                "source_id": edge.source.node_id,
                "dest_id": edge.dest.node_id,
                "color": edge.color_hex
            })
                
        data = {
            "nodes": nodes_data,
            "edges": edges_data
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        self.btn_save.setText("Kaydedildi ✓")
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.btn_save.setText("💾 Panoyu Kaydet"))