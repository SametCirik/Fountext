import json
import os
from PyQt6.QtCore import QObject, pyqtSignal

CONFIG_FILE = "user_data/settings.json"

class LanguageController(QObject):
    language_changed = pyqtSignal()
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageController, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        self.locales = {}
        self.current_lang = "tr"  # Varsayılan dil
        self.load_config()
        self.load_locales()

    def load_config(self):
        # Kayıtlı dil ayarı varsa oku
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.current_lang = data.get("lang", "tr")
                except:
                    pass
        else:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            self.save_config()

    def save_config(self):
        # Dil ayarını user_data klasörüne kaydet
        data = {"lang": self.current_lang}
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load_locales(self):
        locales_dir = os.path.join(os.path.dirname(__file__), "locales")
        for lang_code in ["tr", "en"]:
            file_path = os.path.join(locales_dir, f"{lang_code}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    self.locales[lang_code] = json.load(f)
            else:
                self.locales[lang_code] = {}

    def set_language(self, lang_code):
        if lang_code in self.locales and self.current_lang != lang_code:
            self.current_lang = lang_code
            self.save_config()  # Ayarı diske yaz
            self.language_changed.emit()

    def toggle_language(self):
        new_lang = "en" if self.current_lang == "tr" else "tr"
        self.set_language(new_lang)

    def get(self, key, default=""):
        return self.locales.get(self.current_lang, {}).get(key, default or key)

def tr(key, default=""):
    return LanguageController().get(key, default)
