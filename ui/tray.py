import os
import sys
import threading
from PIL import Image
import pystray


def _get_icon_path():
    """Get the path to the icon file, works both in dev and PyInstaller."""
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, 'assets', 'icon.png')
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'icon.png')


def _create_icon_image():
    """Load the app icon from file."""
    icon_path = _get_icon_path()
    if os.path.exists(icon_path):
        return Image.open(icon_path).resize((64, 64))
    # Fallback: simple blue square
    from PIL import ImageDraw
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([8, 8, 56, 56], radius=6, fill='#1565C0')
    return img


class SystemTray:
    def __init__(self, on_wordbook=None, on_guide=None, on_hotkey=None, on_quit=None):
        self._on_wordbook = on_wordbook
        self._on_guide = on_guide
        self._on_hotkey = on_hotkey
        self._on_quit = on_quit
        self._icon = None

    def start(self):
        import config
        image = _create_icon_image()
        menu = pystray.Menu(
            pystray.MenuItem(config.t('tray_wordbook'), self._open_wordbook),
            pystray.MenuItem(config.t('tray_hotkey'), self._open_hotkey),
            pystray.MenuItem(config.t('tray_guide'), self._open_guide),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(config.t('tray_quit'), self._quit),
        )
        self._icon = pystray.Icon('oxford-dict-lookup', image, config.t('app_title'), menu)
        t = threading.Thread(target=self._icon.run, daemon=True)
        t.start()

    def _open_wordbook(self, icon, item):
        if self._on_wordbook:
            self._on_wordbook()

    def _open_guide(self, icon, item):
        if self._on_guide:
            self._on_guide()

    def _open_hotkey(self, icon, item):
        if self._on_hotkey:
            self._on_hotkey()

    def _quit(self, icon, item):
        icon.stop()
        if self._on_quit:
            self._on_quit()

    def stop(self):
        if self._icon:
            self._icon.stop()
