from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,  
                             QTextEdit, QPushButton, QDialogButtonBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from lang_controller import tr

class TitlePageDialog(QDialog):
    def __init__(self, parent=None, current_title_data=""):
        super().__init__(parent)
        self.setWindowTitle(tr("tp_dialog_title"))
        self.setMinimumWidth(450)
        self.setMinimumHeight(500)
        
        self.layout = QVBoxLayout(self)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        self.scroll_content = QWidget()
        self.form_layout = QFormLayout(self.scroll_content)
        
        self.title_inputs = [QLineEdit() for _ in range(10)]
        self.title_inputs[0].setPlaceholderText(tr("tp_default_title"))
        for i, t_input in enumerate(self.title_inputs):
            self.form_layout.addRow(f"Title {i+1}:", t_input)
            
        self.credit_input = QLineEdit()
        self.credit_input.setPlaceholderText(tr("tp_default_credit"))
        
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText(tr("tp_default_author"))
        
        self.date_input = QLineEdit()
        self.copyright_input = QLineEdit()
        self.watermark_input = QLineEdit()
        
        self.contact_input = QTextEdit()
        self.contact_input.setMaximumHeight(80)
        self.contact_input.setPlaceholderText(f"{tr('tp_default_contact1')}\n{tr('tp_default_contact2')}")
        
        self.form_layout.addRow(tr("tp_credit_label"), self.credit_input)
        self.form_layout.addRow(tr("tp_author_label"), self.author_input)
        self.form_layout.addRow(tr("tp_date_label"), self.date_input)
        self.form_layout.addRow(tr("tp_copyright_label"), self.copyright_input)
        self.form_layout.addRow(tr("tp_watermark_label"), self.watermark_input)
        self.form_layout.addRow(tr("tp_contact_label"), self.contact_input)
        
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText(tr("btn_save"))
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText(tr("btn_cancel"))
        
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
        
        self._parse_current_data(current_title_data)

    def _parse_current_data(self, data):
        lines = data.split('\n')
        contact_lines = []
        in_contact = False
        title_idx = 0
        
        for line in lines:
            lower_line = line.lower()
            if lower_line.startswith("title:"):
                if title_idx < 10:
                    self.title_inputs[title_idx].setText(line.split(":", 1)[1].strip())
                    title_idx += 1
            elif lower_line.startswith("credit:"):
                self.credit_input.setText(line.split(":", 1)[1].strip())
            elif lower_line.startswith("author:"):
                self.author_input.setText(line.split(":", 1)[1].strip())
            elif lower_line.startswith("date:"):
                self.date_input.setText(line.split(":", 1)[1].strip())
            elif lower_line.startswith("copyright:"):
                self.copyright_input.setText(line.split(":", 1)[1].strip())
            elif lower_line.startswith("watermark:"):
                self.watermark_input.setText(line.split(":", 1)[1].strip())
            elif lower_line.startswith("contact:"):
                in_contact = True
                val = line.split(":", 1)[1].strip()
                if val: contact_lines.append(val)
            elif in_contact:
                if line.strip() == "" or ":" in line:
                    in_contact = False  
                else:
                    contact_lines.append(line.strip())
                    
        self.contact_input.setPlainText("\n".join(contact_lines))
        self._normalize_defaults()

    def _normalize_defaults(self):
        # Eğer metin hiçbir şekilde değiştirilmemiş ham şablonsa, güncel dilin şablonuna çevir
        default_titles = ["[SENARYO ADI]", "[SCRIPT TITLE]", "[TÍTULO DEL GUION]", "[TITRE DU SCÉNARIO]", "[НАЗВАНИЕ СЦЕНАРИЯ]"]
        if self.title_inputs[0].text() in default_titles:
            self.title_inputs[0].setText(tr("tp_default_title"))
            
        default_credits = ["Yazan", "Written by", "Escrito por", "Écrit par", "Автор сценария"]
        if self.credit_input.text() in default_credits:
            self.credit_input.setText(tr("tp_default_credit"))
            
        default_authors = ["[İsim Soyisim]", "[Name Surname]", "[Nombre Apellido]", "[Nom Prénom]", "[Имя Фамилия]"]
        if self.author_input.text() in default_authors:
            self.author_input.setText(tr("tp_default_author"))
            
        contact_text = self.contact_input.toPlainText().strip()
        default_contacts = [
            "Telefon Numarası\nE-Posta Adresi",
            "Phone Number\nEmail Address",
            "Número de Teléfono\nCorreo Electrónico",
            "Numéro de Téléphone\nAdresse Email",
            "Номер телефона\nЭлектронная почта"
        ]
        if contact_text in default_contacts:
            self.contact_input.setPlainText(f"{tr('tp_default_contact1')}\n{tr('tp_default_contact2')}")

    def get_fountain_format(self):
        fountain_text = ""
        for t_input in self.title_inputs:
            if t_input.text():
                fountain_text += f"Title: {t_input.text()}\n"
        if self.credit_input.text(): fountain_text += f"Credit: {self.credit_input.text()}\n"
        if self.author_input.text(): fountain_text += f"Author: {self.author_input.text()}\n"
        if self.date_input.text(): fountain_text += f"Date: {self.date_input.text()}\n"
        if self.copyright_input.text(): fountain_text += f"Copyright: {self.copyright_input.text()}\n"
        if self.watermark_input.text(): fountain_text += f"Watermark: {self.watermark_input.text()}\n"
        
        contact_text = self.contact_input.toPlainText().strip()
        if contact_text:
            fountain_text += "Contact:\n"
            for line in contact_text.split('\n'):
                fountain_text += f"    {line}\n"
                
        return fountain_text + "\n"
