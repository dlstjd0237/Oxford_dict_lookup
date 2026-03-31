import time
import threading
import logging

import keyboard
import pyperclip

import config

logger = logging.getLogger(__name__)


class HotkeyListener:
    def __init__(self, callback):
        """callback receives the selected text string."""
        self._callback = callback
        self._lock = threading.Lock()
        self._current_hotkey = None

    def start(self):
        hotkey = config.load_hotkey()
        self._register(hotkey)

    def change_hotkey(self, new_hotkey):
        """Unregister old hotkey and register new one at runtime."""
        if self._current_hotkey:
            try:
                keyboard.remove_hotkey(self._current_hotkey)
            except Exception:
                logger.debug("Failed to remove old hotkey", exc_info=True)
            self._current_hotkey = None
        self._register(new_hotkey)

    def _register(self, hotkey):
        try:
            self._current_hotkey = keyboard.add_hotkey(hotkey, self._on_hotkey, suppress=True)
            logger.info("Registered hotkey: %s", hotkey)
        except Exception as e:
            logger.error("Failed to register hotkey (may require elevated privileges): %s", e)
            try:
                import tkinter.messagebox as mbox
                mbox.showwarning(
                    "Hotkey Registration Failed",
                    f"Could not register hotkey '{hotkey}'.\n"
                    "The keyboard library may require administrator privileges.\n"
                    f"Error: {e}"
                )
            except Exception:
                pass

    def _on_hotkey(self):
        if not self._lock.acquire(blocking=False):
            return
        try:
            text = self._grab_selected_text()
            if text:
                self._callback(text)
        finally:
            self._lock.release()

    def _grab_selected_text(self) -> str:
        # Backup clipboard
        try:
            backup = pyperclip.paste()
        except Exception:
            logger.debug("Failed to backup clipboard", exc_info=True)
            backup = ''

        max_retries = 3
        text = ''
        try:
            pyperclip.copy('')
            time.sleep(0.05)
            keyboard.send('ctrl+c')
            for attempt in range(max_retries):
                time.sleep(0.15)
                text = pyperclip.paste()
                if text:
                    break
                logger.debug("Clipboard empty on attempt %d, retrying", attempt + 1)
        except Exception:
            logger.debug("Failed to grab selected text", exc_info=True)
            text = ''
        finally:
            # Restore clipboard
            try:
                pyperclip.copy(backup)
            except Exception:
                pass

        return text.strip()
