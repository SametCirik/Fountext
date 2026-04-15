from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction

class EditorMenuBar(QMenuBar):
    def __init__(self, main_window, editor):
        super().__init__(main_window)
        self.main_window = main_window
        self.editor = editor 
        self._setup_menu()

    def _setup_menu(self):
        file_menu = self.addMenu("&Dosya")

        new_action = QAction("Yeni", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.main_window.new_file)
        file_menu.addAction(new_action)

        open_action = QAction("Aç...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.main_window.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Kaydet", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.main_window.save_file)
        file_menu.addAction(save_action)

        # --- YENİ: PDF Dışa Aktar Butonu ---
        export_pdf_action = QAction("PDF Olarak Dışa Aktar...", self)
        export_pdf_action.setShortcut("Ctrl+E")
        export_pdf_action.triggered.connect(self.main_window.export_pdf)
        file_menu.addAction(export_pdf_action)
        # -----------------------------------

        file_menu.addSeparator()

        exit_action = QAction("Çıkış", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)

        edit_menu = self.addMenu("Düz&enle")
        
        undo_action = QAction("Geri Al", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self._dummy_undo) 
        edit_menu.addAction(undo_action)

        redo_action = QAction("Yinele", self)
        redo_action.setShortcut("Ctrl+Shift+Z")
        redo_action.triggered.connect(self._dummy_redo)
        edit_menu.addAction(redo_action)

        view_menu = self.addMenu("&Görünüm")
        
        # --- YENİ: Sahne Gezgini Menü Seçeneği ---
        self.toggle_navigator_action = QAction("Sahne Gezgini", self)
        self.toggle_navigator_action.setCheckable(True)
        self.toggle_navigator_action.setChecked(True) # Başlangıçta açık gelsin
        self.toggle_navigator_action.triggered.connect(self.main_window.toggle_navigator)
        view_menu.addAction(self.toggle_navigator_action)
        
        toggle_view_action = QAction("Fountain Düz Metin Modu - ÇOK YAKINDA!", self)
        toggle_view_action.setCheckable(True)  
        toggle_view_action.setShortcut("Ctrl+T")
        view_menu.addAction(toggle_view_action)

    def _dummy_undo(self):
        print("Geri Al: Daha sonra C++ motoruna eklenecek.")

    def _dummy_redo(self):
        print("Yinele: Daha sonra C++ motoruna eklenecek.")