import sys
import os
import logging
import threading
import tkinter as tk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Windows DPI awareness
logger = logging.getLogger(__name__)
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    logger.debug("Could not set DPI awareness", exc_info=True)

from core.hotkey_listener import HotkeyListener
from core.text_processor import clean_word
from dictionary.free_dict_api import FreeDictAPI
from dictionary.oxford_scraper import OxfordScraper
from dictionary.models import WordResult
from storage.cache import Cache
from storage.wordbook import Wordbook
from ui.popup import PopupWindow
from ui.tray import SystemTray
from ui.wordbook_window import WordbookWindow
from ui.guide_window import GuideWindow
from ui.hotkey_window import HotkeyWindow


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide root window

        self.cache = Cache()
        self.wordbook = Wordbook()
        self.providers = [FreeDictAPI(), OxfordScraper()]
        self.popup = PopupWindow(self.root)
        self.wordbook_window = WordbookWindow(
            self.root, self.wordbook, on_lookup=self._lookup_word
        )

        self.guide = GuideWindow(self.root, on_lang_change=self._on_lang_change)
        self.hotkey_window = HotkeyWindow(self.root, on_hotkey_change=self._on_hotkey_change)

        self.tray = SystemTray(
            on_wordbook=lambda: self.root.after(0, self.wordbook_window.show),
            on_guide=lambda: self.root.after(0, self.guide.show),
            on_hotkey=lambda: self.root.after(0, self.hotkey_window.show),
            on_quit=lambda: self.root.after(0, self._quit),
        )

        self.hotkey_listener = HotkeyListener(callback=self._on_hotkey)

    def _on_lang_change(self, lang):
        # Restart tray to apply new language to menu
        self.tray.stop()
        self.tray.start()

    def _on_hotkey_change(self, new_hotkey):
        # Apply new hotkey at runtime without restart
        self.hotkey_listener.change_hotkey(new_hotkey)

    def run(self):
        self.tray.start()
        self.hotkey_listener.start()
        self.root.after(500, self.guide.show_if_first)
        self.root.mainloop()

    def _on_hotkey(self, text: str):
        word = clean_word(text)
        if not word:
            return
        self.root.after(0, lambda: self._show_loading(word))
        threading.Thread(target=self._lookup_word, args=(word,), daemon=True).start()

    def _show_loading(self, word: str):
        pass  # Could show a loading indicator

    def _lookup_word(self, word: str):
        word = clean_word(word) if ' ' in word else word.lower().strip()
        if not word:
            return

        # Check cache first
        result = self.cache.get(word)
        if result:
            self.root.after(0, lambda r=result: self.popup.show(r, on_save=self._save_to_wordbook))
            return

        # Try providers
        result = None
        for provider in self.providers:
            result = provider.lookup(word)
            if result:
                self.cache.put(result)
                break

        if result:
            self.root.after(0, lambda r=result: self.popup.show(r, on_save=self._save_to_wordbook))
        else:
            self.root.after(0, lambda: self.popup.show_error(word, 'Could not find this word in any dictionary.'))

    def _save_to_wordbook(self, result: WordResult):
        self.wordbook.add(result)

    def _quit(self):
        self.tray.stop()
        self.cache.close()
        self.wordbook.close()
        self.root.quit()
        self.root.destroy()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
