import os
import json

HOTKEY = 'ctrl+shift+d'
FREE_DICT_API_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
OXFORD_LEARNER_URL = 'https://www.oxfordlearnersdictionaries.com/definition/english/{word}'
REQUEST_TIMEOUT = 5
CACHE_DB_PATH = os.path.join(os.path.expanduser('~'), '.oxford-dict-lookup', 'cache.db')
CACHE_TTL_DAYS = 30
POPUP_WIDTH = 420
POPUP_MAX_HEIGHT = 500
POPUP_FONT_FAMILY = 'Segoe UI'
POPUP_BG_COLOR = '#FFFFFF'
POPUP_BORDER_COLOR = '#CCCCCC'

# Language setting
SETTINGS_PATH = os.path.join(os.path.expanduser('~'), '.oxford-dict-lookup', 'settings.json')
DEFAULT_LANG = 'en'  # 'en' or 'ko'

# Modifier keys allowed (user must pick exactly 2) + 1 regular key
MODIFIER_KEYS = ['ctrl', 'shift', 'alt']


def load_hotkey():
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f).get('hotkey', HOTKEY)
    except Exception:
        return HOTKEY


def save_hotkey(hotkey):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    data = {}
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        pass
    data['hotkey'] = hotkey
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def hotkey_display(hotkey_str):
    """Convert 'ctrl+shift+d' to 'Ctrl + Shift + D' for display."""
    return ' + '.join(part.capitalize() for part in hotkey_str.split('+'))


def load_lang():
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f).get('lang', DEFAULT_LANG)
    except Exception:
        return DEFAULT_LANG


def save_lang(lang):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    data = {}
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        pass
    data['lang'] = lang
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


# UI text translations
TEXTS = {
    'en': {
        'app_title': 'Oxford Dict Lookup',
        'welcome_title': 'Welcome to Oxford Dict Lookup',
        'welcome_how_title': 'How to use',
        'welcome_step1': '1. Select (highlight) any English word on your screen',
        'welcome_step2': '2. Press  Ctrl + Shift + D',
        'welcome_step3': '3. A popup will appear with the definition, pronunciation, and examples',
        'welcome_features_title': 'Features',
        'welcome_feat1': 'Dictionary lookup from Free Dictionary API + Oxford Learner\'s',
        'welcome_feat2': 'Korean translation of definitions',
        'welcome_feat3': 'Wordbook - save words for later review',
        'welcome_feat4': 'Offline cache - previously searched words load instantly',
        'welcome_tray': 'The app runs in the system tray (bottom-right of taskbar).\nRight-click the tray icon for Wordbook and Settings.',
        'welcome_start': 'Get Started',
        'welcome_dont_show': 'Don\'t show this again',
        'hotkey_label': 'Hotkey',
        'source_label': 'Source',
        'korean_title': 'Korean',
        'translating': 'Translating...',
        'translation_failed': '(Translation failed)',
        'save_btn': 'Save to Wordbook',
        'saved_btn': 'Saved \u2713',
        'not_found': 'not found',
        'not_found_msg': 'Could not find this word in any dictionary.',
        'tray_wordbook': 'Open Wordbook',
        'tray_guide': 'How to Use',
        'tray_quit': 'Quit',
        'lang_label': 'Language',
        'hotkey_setting': 'Hotkey Settings',
        'hotkey_change': 'Change Hotkey',
        'hotkey_mod1': 'Modifier 1',
        'hotkey_mod2': 'Modifier 2',
        'hotkey_key': 'Key',
        'hotkey_apply': 'Apply',
        'hotkey_cancel': 'Cancel',
        'hotkey_current': 'Current',
        'hotkey_preview': 'New Hotkey',
        'hotkey_invalid': 'Please select 2 different modifiers and a key (A-Z, 0-9, F1-F12).',
        'hotkey_success': 'Hotkey changed successfully! Restart the app to apply.',
        'tray_hotkey': 'Change Hotkey',
    },
    'ko': {
        'app_title': 'Oxford 영어사전 검색기',
        'welcome_title': 'Oxford 영어사전 검색기에 오신 것을 환영합니다',
        'welcome_how_title': '사용 방법',
        'welcome_step1': '1. 화면에서 영어 단어를 드래그하여 선택(블록)합니다',
        'welcome_step2': '2. Ctrl + Shift + D 를 누릅니다',
        'welcome_step3': '3. 팝업 창에 단어의 뜻, 발음, 예문이 표시됩니다',
        'welcome_features_title': '주요 기능',
        'welcome_feat1': 'Free Dictionary API + Oxford Learner\'s 사전에서 검색',
        'welcome_feat2': '영어 정의의 한국어 번역 제공',
        'welcome_feat3': '단어장 - 단어를 저장하여 나중에 복습',
        'welcome_feat4': '오프라인 캐시 - 이전에 검색한 단어는 즉시 로딩',
        'welcome_tray': '앱은 시스템 트레이(작업표시줄 오른쪽 하단)에서 실행됩니다.\n트레이 아이콘을 우클릭하면 단어장과 설정을 열 수 있습니다.',
        'welcome_start': '시작하기',
        'welcome_dont_show': '다시 표시하지 않기',
        'hotkey_label': '단축키',
        'source_label': '출처',
        'korean_title': '한국어 뜻',
        'translating': '번역 중...',
        'translation_failed': '(번역 실패)',
        'save_btn': '단어장에 저장',
        'saved_btn': '저장됨 \u2713',
        'not_found': '을(를) 찾을 수 없습니다',
        'not_found_msg': '어떤 사전에서도 이 단어를 찾을 수 없습니다.',
        'tray_wordbook': '단어장 열기',
        'tray_guide': '사용 방법',
        'tray_quit': '종료',
        'lang_label': '언어',
        'hotkey_setting': '단축키 설정',
        'hotkey_change': '단축키 변경',
        'hotkey_mod1': '조합키 1',
        'hotkey_mod2': '조합키 2',
        'hotkey_key': '키',
        'hotkey_apply': '적용',
        'hotkey_cancel': '취소',
        'hotkey_current': '현재 단축키',
        'hotkey_preview': '새 단축키',
        'hotkey_invalid': '서로 다른 조합키 2개와 일반 키(A-Z, 0-9, F1-F12) 1개를 선택해주세요.',
        'hotkey_success': '단축키가 변경되었습니다! 앱을 재시작하면 적용됩니다.',
        'tray_hotkey': '단축키 변경',
    },
}


def t(key):
    """Get translated text for current language."""
    lang = load_lang()
    return TEXTS.get(lang, TEXTS['en']).get(key, key)
