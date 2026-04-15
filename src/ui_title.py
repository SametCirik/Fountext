from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QColor, QTextBlockFormat, QTextCursor
import fountext_engine

def decorate_title_page(scene, page, current_page_y, fountain_font, page_width):
    """
    Başlık sayfasını analiz eder ve boşsa şık, matematiksel bir filigran çizer.
    """
    has_real_title = False
    
    for block in page.blocks:
        if block.text.strip() and block.type != fountext_engine.BlockType.Watermark:
            has_real_title = True
            
        if block.type == fountext_engine.BlockType.Watermark:
            watermark_text = block.text.replace("Watermark:", "").strip()
            if watermark_text:
                wm_item = QGraphicsTextItem(watermark_text)
                wm_font = QFont("Courier Prime", 60, QFont.Weight.Bold)
                wm_item.setFont(wm_font)
                wm_item.setDefaultTextColor(QColor(150, 150, 150, 50)) 
                
                wm_item.setPos(150.0, current_page_y + 800.0)
                wm_item.setRotation(-45)
                scene.addItem(wm_item)

    if not has_real_title:
        # 1. Merkez Bloğu (Title, Credit, Author)
        center_text = "Title: SENARYO ADI\nCredit: Yazan\nAuthor: İsim Soyisim"
        c_item = QGraphicsTextItem()
        c_item.setPlainText(center_text)
        c_item.setFont(fountain_font)
        c_item.setDefaultTextColor(QColor(200, 200, 200)) 
        
        # YENİ: Tam kağıt genişliğine yayıp matematiksel ortalıyoruz
        c_item.setTextWidth(page_width)
        fmt = QTextBlockFormat()
        fmt.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        cursor = c_item.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeBlockFormat(fmt)
        
        # X=0'dan başlatıyoruz ki tam ortaya otursun
        c_item.setPos(0, current_page_y + 336.0) 
        scene.addItem(c_item)
        
        # 2. İletişim Bloğu (Sol Alt) - Sola yaslı kalması doğru olandır
        left_text = "Contact:\nTelefon Numarası\nE-Posta Adresi"
        l_item = QGraphicsTextItem(left_text)
        l_item.setFont(fountain_font)
        l_item.setDefaultTextColor(QColor(200, 200, 200))
        # 1.5 inç (144px) sağdan (Senaryo standart sol marjı)
        l_item.setPos(144.0, current_page_y + 900.0) 
        scene.addItem(l_item)