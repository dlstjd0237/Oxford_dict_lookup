<p align="center">
  <img src="assets/icon.png" alt="Oxford Dict Lookup" width="128" height="128">
</p>

<h1 align="center">Oxford Dict Lookup</h1>

<p align="center">
  A Windows dictionary app that instantly shows definitions, pronunciation, and examples when you select a word and press a hotkey.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Windows-blue" alt="Windows">
  <img src="https://img.shields.io/badge/python-3.9%2B-brightgreen" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT License">
</p>

---

## Features

- **Instant Lookup** - Select any English word on screen and press `Ctrl+Shift+D` to get a popup with results
- **Dual Dictionary Sources** - [Free Dictionary API](https://dictionaryapi.dev/) + [Oxford Learner's Dictionaries](https://www.oxfordlearnersdictionaries.com/) scraping
- **Korean Translation** - Automatically translates English definitions to Korean
- **Wordbook** - Save words and review them later
- **Offline Cache** - Previously searched words load instantly
- **System Tray** - Runs in background, managed via tray icon
- **Custom Hotkey** - Change the hotkey to your preference
- **Bilingual UI** - English and Korean interface supported

## How to Use

1. Select (highlight) any English word on your screen
2. Press `Ctrl + Shift + D`
3. A popup appears with definitions, pronunciation, and examples

## Installation

### EXE (Recommended)

Download `OxfordDictLookup.exe` from the [Releases](../../releases) page and run it.

### Run from Source

```bash
git clone https://github.com/dlstjd0237/oxford-dict-lookup.git
cd oxford-dict-lookup
pip install -r requirements.txt
python main.py
```

## Build

```bash
pip install pyinstaller
pyinstaller OxfordDictLookup.spec --noconfirm
```

Output: `dist/OxfordDictLookup.exe`

## Project Structure

```
oxford-dict-lookup/
├── main.py                 # App entry point
├── config.py               # Settings & i18n texts
├── core/
│   ├── hotkey_listener.py  # Global hotkey listener
│   ├── text_processor.py   # Selected text processing
│   └── translator.py       # Korean translation
├── dictionary/
│   ├── models.py           # Data models
│   ├── free_dict_api.py    # Free Dictionary API client
│   └── oxford_scraper.py   # Oxford Learner's scraper
├── storage/
│   ├── cache.py            # SQLite cache
│   └── wordbook.py         # Wordbook storage
├── ui/
│   ├── popup.py            # Result popup
│   ├── tray.py             # System tray
│   ├── wordbook_window.py  # Wordbook window
│   ├── guide_window.py     # Usage guide
│   └── hotkey_window.py    # Hotkey settings
└── assets/
    ├── icon.ico            # App icon
    └── icon.png
```

## Requirements

- Windows 10/11
- Python 3.9+ (when running from source)

## License

[MIT](LICENSE)
