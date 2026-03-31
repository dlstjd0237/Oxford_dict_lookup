import logging
import json
import os
import tkinter as tk

import config

logger = logging.getLogger(__name__)


def _should_show_guide():
    try:
        with open(config.SETTINGS_PATH, 'r', encoding='utf-8') as f:
            return not json.load(f).get('hide_guide', False)
    except Exception:
        return True


def _set_hide_guide(val):
    os.makedirs(os.path.dirname(config.SETTINGS_PATH), exist_ok=True)
    data = {}
    try:
        with open(config.SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        pass
    data['hide_guide'] = val
    with open(config.SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


class GuideWindow:
    def __init__(self, root: tk.Tk, on_lang_change=None):
        self._root = root
        self._on_lang_change = on_lang_change
        self._win = None

    def show_if_first(self):
        if _should_show_guide():
            self.show()

    def show(self):
        if self._win and self._win.winfo_exists():
            self._win.lift()
            return
        self._build()

    def _build(self):
        win = tk.Toplevel(self._root)
        self._win = win
        win.title(config.t('app_title'))
        win.configure(bg='#FAFAFA')
        win.resizable(False, False)
        win.attributes('-topmost', True)

        fam = config.POPUP_FONT_FAMILY
        w, h = 520, 540
        sx = (win.winfo_screenwidth() - w) // 2
        sy = (win.winfo_screenheight() - h) // 2
        win.geometry(f'{w}x{h}+{sx}+{sy}')

        main_frame = tk.Frame(win, bg='#FAFAFA')
        main_frame.pack(fill='both', expand=True, padx=24, pady=18)

        # Language toggle at top-right
        lang_frame = tk.Frame(main_frame, bg='#FAFAFA')
        lang_frame.pack(fill='x', pady=(0, 8))

        tk.Label(lang_frame, text=config.t('lang_label') + ':', font=(fam, 9),
                 bg='#FAFAFA', fg='#666').pack(side='left')

        lang_var = tk.StringVar(value=config.load_lang())

        def _on_lang_toggle():
            new_lang = lang_var.get()
            config.save_lang(new_lang)
            win.destroy()
            self._build()
            if self._on_lang_change:
                self._on_lang_change(new_lang)

        en_rb = tk.Radiobutton(lang_frame, text='English', variable=lang_var, value='en',
                               font=(fam, 9), bg='#FAFAFA', activebackground='#FAFAFA',
                               command=_on_lang_toggle, cursor='hand2')
        en_rb.pack(side='left', padx=(8, 2))

        ko_rb = tk.Radiobutton(lang_frame, text='한국어', variable=lang_var, value='ko',
                               font=(fam, 9), bg='#FAFAFA', activebackground='#FAFAFA',
                               command=_on_lang_toggle, cursor='hand2')
        ko_rb.pack(side='left', padx=2)

        # Title
        tk.Label(main_frame, text=config.t('welcome_title'),
                 font=(fam, 16, 'bold'), bg='#FAFAFA', fg='#1565C0').pack(pady=(0, 16))

        # Hotkey highlight
        hotkey_frame = tk.Frame(main_frame, bg='#E3F2FD', highlightbackground='#90CAF9',
                                highlightthickness=1)
        hotkey_frame.pack(fill='x', pady=(0, 14))
        current_hotkey = config.hotkey_display(config.load_hotkey())
        tk.Label(hotkey_frame, text=config.t('hotkey_label') + ':  ' + current_hotkey,
                 font=(fam, 14, 'bold'), bg='#E3F2FD', fg='#1565C0').pack(pady=10)

        # How to use
        tk.Label(main_frame, text=config.t('welcome_how_title'),
                 font=(fam, 12, 'bold'), bg='#FAFAFA', fg='#333', anchor='w').pack(fill='x', pady=(0, 4))

        for step_key in ('welcome_step1', 'welcome_step2', 'welcome_step3'):
            tk.Label(main_frame, text=config.t(step_key), font=(fam, 10),
                     bg='#FAFAFA', fg='#444', anchor='w', wraplength=460, justify='left').pack(
                fill='x', padx=(8, 0), pady=2)

        # Features
        tk.Label(main_frame, text=config.t('welcome_features_title'),
                 font=(fam, 12, 'bold'), bg='#FAFAFA', fg='#333', anchor='w').pack(
            fill='x', pady=(12, 4))

        for feat_key in ('welcome_feat1', 'welcome_feat2', 'welcome_feat3', 'welcome_feat4'):
            tk.Label(main_frame, text='\u2022 ' + config.t(feat_key), font=(fam, 9),
                     bg='#FAFAFA', fg='#555', anchor='w', wraplength=460, justify='left').pack(
                fill='x', padx=(8, 0), pady=1)

        # Tray info
        tk.Frame(main_frame, bg='#E0E0E0', height=1).pack(fill='x', pady=10)
        tk.Label(main_frame, text=config.t('welcome_tray'), font=(fam, 9),
                 bg='#FAFAFA', fg='#777', wraplength=460, justify='left').pack(fill='x')

        # Bottom: don't show + start button
        bottom = tk.Frame(main_frame, bg='#FAFAFA')
        bottom.pack(fill='x', pady=(14, 0))

        dont_show_var = tk.BooleanVar(value=False)
        tk.Checkbutton(bottom, text=config.t('welcome_dont_show'), variable=dont_show_var,
                       font=(fam, 9), bg='#FAFAFA', activebackground='#FAFAFA',
                       fg='#888', cursor='hand2').pack(side='left')

        def _close():
            if dont_show_var.get():
                _set_hide_guide(True)
            win.destroy()

        tk.Button(bottom, text=config.t('welcome_start'), font=(fam, 11, 'bold'),
                  bg='#1565C0', fg='white', relief='flat', padx=20, pady=6,
                  cursor='hand2', command=_close).pack(side='right')

        win.protocol('WM_DELETE_WINDOW', _close)
