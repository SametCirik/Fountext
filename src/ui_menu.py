from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction
from lang_controller import LanguageController, tr

class EditorMenuBar(QMenuBar):
    def __init__(self, main_window, editor):
        super().__init__(main_window)
        self.main_window = main_window
        self.editor = editor 
        self._setup_menu()
        LanguageController().language_changed.connect(self.update_texts)

    def _setup_menu(self):
        self.file_menu = self.addMenu(tr("menu_file"))

        self.new_action = QAction(tr("menu_new"), self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.main_window.new_file)
        self.file_menu.addAction(self.new_action)

        self.open_action = QAction(tr("menu_open"), self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.main_window.open_file)
        self.file_menu.addAction(self.open_action)

        self.save_action = QAction(tr("menu_save"), self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.main_window.save_file)
        self.file_menu.addAction(self.save_action)

        self.export_pdf_action = QAction(tr("menu_export_pdf"), self)
        self.export_pdf_action.setShortcut("Ctrl+E")
        self.export_pdf_action.triggered.connect(self.main_window.export_pdf)
        self.file_menu.addAction(self.export_pdf_action)

        self.file_menu.addSeparator()

        self.home_action = QAction(tr("menu_home"), self)
        self.home_action.setShortcut("Ctrl+H")
        self.home_action.triggered.connect(self.main_window.show_home_screen)
        self.file_menu.addAction(self.home_action)

        self.file_menu.addSeparator()

        self.exit_action = QAction(tr("menu_exit"), self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.main_window.close)
        self.file_menu.addAction(self.exit_action)

        self.edit_menu = self.addMenu(tr("menu_edit"))
        
        self.undo_action = QAction(tr("menu_undo"), self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self._dummy_undo) 
        self.edit_menu.addAction(self.undo_action)

        self.redo_action = QAction(tr("menu_redo"), self)
        self.redo_action.setShortcut("Ctrl+Shift+Z")
        self.redo_action.triggered.connect(self._dummy_redo)
        self.edit_menu.addAction(self.redo_action)

        self.view_menu = self.addMenu(tr("menu_view"))
        
        self.toggle_navigator_action = QAction(tr("menu_navigator"), self)
        self.toggle_navigator_action.setCheckable(True)
        self.toggle_navigator_action.setChecked(True)
        self.toggle_navigator_action.triggered.connect(self.main_window.toggle_navigator)
        self.view_menu.addAction(self.toggle_navigator_action)
        
        self.toggle_view_action = QAction(tr("menu_plain_text"), self)
        self.toggle_view_action.setCheckable(True)  
        self.toggle_view_action.setShortcut("Ctrl+T")
        self.view_menu.addAction(self.toggle_view_action)

    def update_texts(self):
        self.file_menu.setTitle(tr("menu_file"))
        self.new_action.setText(tr("menu_new"))
        self.open_action.setText(tr("menu_open"))
        self.save_action.setText(tr("menu_save"))
        self.export_pdf_action.setText(tr("menu_export_pdf"))
        self.home_action.setText(tr("menu_home"))
        self.exit_action.setText(tr("menu_exit"))
        
        self.edit_menu.setTitle(tr("menu_edit"))
        self.undo_action.setText(tr("menu_undo"))
        self.redo_action.setText(tr("menu_redo"))
        
        self.view_menu.setTitle(tr("menu_view"))
        self.toggle_navigator_action.setText(tr("menu_navigator"))
        self.toggle_view_action.setText(tr("menu_plain_text"))

    def _dummy_undo(self):
        print(tr("dummy_undo"))

    def _dummy_redo(self):
        print(tr("dummy_redo"))
