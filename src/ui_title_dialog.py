from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                             QTextEdit, QPushButton, QDialogButtonBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt

class TitlePageDialog(QDialog):
    def __init__(self, parent=None, current_title_data=""):
        super().__init__(parent)
        self.setWindowTitle("Kapak Sayfası Ayarları")
        self.setMinimumWidth(450)
        self.setMinimumHeight(500) # İdeal bir başlangıç yüksekliği
        
        self.layout = QVBoxLayout(self)
        
        # --- KAYDIRMA ALANI (SCROLL AREA) ---
        # 10 Title ve diğer kutular ekrana sığsın diye formu kaydırılabilir yapıyoruz
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame) # Kenarlıkları kaldır, şık dursun
        
        self.scroll_content = QWidget()
        self.form_layout = QFormLayout(self.scroll_content)
        
        # 10 Adet Title Input (Liste olarak tutuyoruz)
        self.title_inputs = [QLineEdit() for _ in range(10)]
        for i, t_input in enumerate(self.title_inputs):
            self.form_layout.addRow(f"Title {i+1}:", t_input)
            
        # Diğer standart girişler (Varsayılan Credit metnini sildim ki eski projelerde çakışmasın)
        self.credit_input = QLineEdit()
        self.author_input = QLineEdit()
        self.date_input = QLineEdit()
        self.copyright_input = QLineEdit()
        self.watermark_input = QLineEdit()
        self.contact_input = QTextEdit()
        self.contact_input.setMaximumHeight(80)
        
        self.form_layout.addRow("Credit (Unvan):", self.credit_input)
        self.form_layout.addRow("Author (Yazar):", self.author_input)
        self.form_layout.addRow("Date (Tarih):", self.date_input)
        self.form_layout.addRow("Copyright (Telif):", self.copyright_input)
        self.form_layout.addRow("Watermark (Filigran):", self.watermark_input)
        self.form_layout.addRow("Contact (İletişim):", self.contact_input)
        
        # Formu kaydırma alanının içine oturtuyoruz
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        
        # Butonlar (Kaydet / İptal)
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)
        
        # Verileri okuyup doldur
        self._parse_current_data(current_title_data)

    def _parse_current_data(self, data):
        """Mevcut Fountain kapak verisini okuyup forma doldurur."""
        lines = data.split('\n')
        contact_lines = []
        in_contact = False
        title_idx = 0 # Kaçıncı Title inputundayız?
        
        for line in lines:
            lower_line = line.lower()
            if lower_line.startswith("title:"):
                if title_idx < 10: # LİMİT 10'A ÇIKARILDI
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

    def get_fountain_format(self):
        """Formdaki verileri tekrar standart Fountain formatına çevirir."""
        fountain_text = ""
        
        # Sadece içi dolu olan Title'ları ekle
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
                
        # Fountain başlık sayfasının bittiğini belirtmek için en sona fazladan bir boşluk (\n) atılır
        return fountain_text + "\n"