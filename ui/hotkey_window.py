import logging
import tkinter as tk
from tkinter import messagebox

import config

logger = logging.getLogger(__name__)

# Keys available for the non-modifier slot
REGULAR_KEYS = (
    [chr(c) for c in range(ord('a'), ord('z') + 1)]
    + [str(n) for n in range(10)]
    + [f'f{n}' for n in range(1, 13)]
)


class HotkeyWindow:
    def __init__(self, root: tk.Tk, on_hotkey_change=None):
        self._root = root
        self._on_hotkey_change = on_hotkey_change
        self._win = None

    def show(self):
        if self._win and self._win.winfo_exists():
            self._win.lift()
            return
        self._build()

    def _build(self):
        win = tk.Toplevel(self._root)
        self._win = win
        win.title(config.t('hotkey_setting'))
        win.configure(bg='#FAFAFA')
        win.resizable(False, False)
        win.attributes('-topmost', True)

        fam = config.POPUP_FONT_FAMILY
        w, h = 400, 320
        sx = (win.winfo_screenwidth() - w) // 2
        sy = (win.winfo_screenheight() - h) // 2
        win.geometry(f'{w}x{h}+{sx}+{sy}')

        frame = tk.Frame(win, bg='#FAFAFA')
        frame.pack(fill='both', expand=True, padx=24, pady=18)

        # Title
        tk.Label(frame, text=config.t('hotkey_change'), font=(fam, 14, 'bold'),
                 bg='#FAFAFA', fg='#1565C0').pack(pady=(0, 12))

        # Current hotkey display
        current = config.load_hotkey()
        tk.Label(frame, text=f'{config.t("hotkey_current")}:  {config.hotkey_display(current)}',
                 font=(fam, 11), bg='#FAFAFA', fg='#555').pack(pady=(0, 14))

        # Parse current hotkey into parts
        parts = current.split('+')
        cur_mod1 = parts[0] if len(parts) >= 3 else 'ctrl'
        cur_mod2 = parts[1] if len(parts) >= 3 else 'shift'
        cur_key = parts[2] if len(parts) >= 3 else 'd'

        # Modifier 1
        selector_frame = tk.Frame(frame, bg='#FAFAFA')
        selector_frame.pack(fill='x', pady=4)

        tk.Label(selector_frame, text=config.t('hotkey_mod1') + ':', font=(fam, 10),
                 bg='#FAFAFA', fg='#333', width=10, anchor='e').pack(side='left')
        mod1_var = tk.StringVar(value=cur_mod1)
        for m in config.MODIFIER_KEYS:
            tk.Radiobutton(selector_frame, text=m.capitalize(), variable=mod1_var, value=m,
                           font=(fam, 10), bg='#FAFAFA', activebackground='#FAFAFA',
                           command=lambda: self._update_preview(preview_label, mod1_var, mod2_var, key_var),
                           cursor='hand2').pack(side='left', padx=6)

        # Modifier 2
        selector_frame2 = tk.Frame(frame, bg='#FAFAFA')
        selector_frame2.pack(fill='x', pady=4)

        tk.Label(selector_frame2, text=config.t('hotkey_mod2') + ':', font=(fam, 10),
                 bg='#FAFAFA', fg='#333', width=10, anchor='e').pack(side='left')
        mod2_var = tk.StringVar(value=cur_mod2)
        for m in config.MODIFIER_KEYS:
            tk.Radiobutton(selector_frame2, text=m.capitalize(), variable=mod2_var, value=m,
                           font=(fam, 10), bg='#FAFAFA', activebackground='#FAFAFA',
                           command=lambda: self._update_preview(preview_label, mod1_var, mod2_var, key_var),
                           cursor='hand2').pack(side='left', padx=6)

        # Regular key
        key_frame = tk.Frame(frame, bg='#FAFAFA')
        key_frame.pack(fill='x', pady=4)

        tk.Label(key_frame, text=config.t('hotkey_key') + ':', font=(fam, 10),
                 bg='#FAFAFA', fg='#333', width=10, anchor='e').pack(side='left')
        key_var = tk.StringVar(value=cur_key)
        key_combo = tk.OptionMenu(key_frame, key_var, *REGULAR_KEYS,
                                  command=lambda _: self._update_preview(preview_label, mod1_var, mod2_var, key_var))
        key_combo.configure(font=(fam, 10), width=6, cursor='hand2')
        key_combo.pack(side='left', padx=6)

        # Preview
        tk.Frame(frame, bg='#E0E0E0', height=1).pack(fill='x', pady=10)
        preview_label = tk.Label(frame, text='', font=(fam, 13, 'bold'),
                                 bg='#E3F2FD', fg='#1565C0', pady=6)
        preview_label.pack(fill='x')
        self._update_preview(preview_label, mod1_var, mod2_var, key_var)

        # Buttons
        btn_frame = tk.Frame(frame, bg='#FAFAFA')
        btn_frame.pack(fill='x', pady=(14, 0))

        tk.Button(btn_frame, text=config.t('hotkey_cancel'), font=(fam, 10),
                  relief='groove', padx=14, pady=4, cursor='hand2',
                  command=win.destroy).pack(side='right', padx=(6, 0))

        tk.Button(btn_frame, text=config.t('hotkey_apply'), font=(fam, 10, 'bold'),
                  bg='#1565C0', fg='white', relief='flat', padx=14, pady=4, cursor='hand2',
                  command=lambda: self._apply(win, mod1_var, mod2_var, key_var)).pack(side='right')

        win.protocol('WM_DELETE_WINDOW', win.destroy)

    def _update_preview(self, label, mod1_var, mod2_var, key_var):
        combo = f'{mod1_var.get()}+{mod2_var.get()}+{key_var.get()}'
        label.configure(text=f'{config.t("hotkey_preview")}:  {config.hotkey_display(combo)}')

    def _apply(self, win, mod1_var, mod2_var, key_var):
        mod1 = mod1_var.get()
        mod2 = mod2_var.get()
        key = key_var.get()

        # Validate: 2 modifiers must be different
        if mod1 == mod2:
            messagebox.showwarning(config.t('hotkey_setting'), config.t('hotkey_invalid'),
                                   parent=win)
            return

        new_hotkey = f'{mod1}+{mod2}+{key}'
        config.save_hotkey(new_hotkey)
        messagebox.showinfo(config.t('hotkey_setting'), config.t('hotkey_success'),
                            parent=win)
        win.destroy()
        if self._on_hotkey_change:
            self._on_hotkey_change(new_hotkey)
