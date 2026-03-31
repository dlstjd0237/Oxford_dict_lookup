import logging
import tkinter as tk
from tkinter import font as tkfont

import config
from dictionary.models import WordResult
from core.translator import translate_to_korean

logger = logging.getLogger(__name__)


class PopupWindow:
    def __init__(self, root: tk.Tk):
        self._root = root
        self._top = None

    def show(self, result: WordResult, on_save=None):
        """Display the result popup near the cursor."""
        self.close()
        self._top = top = tk.Toplevel(self._root)
        top.overrideredirect(True)
        top.attributes('-topmost', True)
        top.configure(bg=config.POPUP_BG_COLOR, highlightbackground=config.POPUP_BORDER_COLOR,
                      highlightthickness=1)

        # Position near mouse cursor
        x = self._root.winfo_pointerx() + 15
        y = self._root.winfo_pointery() + 15

        # Container frame with scrollbar
        container = tk.Frame(top, bg=config.POPUP_BG_COLOR)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=config.POPUP_BG_COLOR, highlightthickness=0,
                           width=config.POPUP_WIDTH - 20)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        frame = tk.Frame(canvas, bg=config.POPUP_BG_COLOR)

        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        top.bind('<MouseWheel>', _on_mousewheel)

        pad = 12
        fam = config.POPUP_FONT_FAMILY

        # Word title
        tk.Label(frame, text=result.word, font=(fam, 16, 'bold'),
                 bg=config.POPUP_BG_COLOR, fg='#1a1a1a', anchor='w').pack(
            fill='x', padx=pad, pady=(pad, 2))

        # Phonetic
        if result.phonetic:
            tk.Label(frame, text=result.phonetic, font=(fam, 11),
                     bg=config.POPUP_BG_COLOR, fg='#666666', anchor='w').pack(
                fill='x', padx=pad, pady=(0, 4))

        # Source
        tk.Label(frame, text=f'{config.t("source_label")}: {result.source}', font=(fam, 8),
                 bg=config.POPUP_BG_COLOR, fg='#999999', anchor='w').pack(
            fill='x', padx=pad, pady=(0, 6))

        # Separator
        tk.Frame(frame, bg='#E0E0E0', height=1).pack(fill='x', padx=pad, pady=4)

        # Meanings
        for meaning in result.meanings:
            if meaning.part_of_speech:
                tk.Label(frame, text=meaning.part_of_speech, font=(fam, 11, 'italic'),
                         bg=config.POPUP_BG_COLOR, fg='#2E7D32', anchor='w').pack(
                    fill='x', padx=pad, pady=(6, 2))

            for i, defn in enumerate(meaning.definitions, 1):
                text = f'{i}. {defn.definition}'
                lbl = tk.Label(frame, text=text, font=(fam, 10),
                               bg=config.POPUP_BG_COLOR, fg='#333333', anchor='w',
                               wraplength=config.POPUP_WIDTH - 50, justify='left')
                lbl.pack(fill='x', padx=(pad + 10, pad), pady=(2, 0))

                if defn.example:
                    ex_lbl = tk.Label(frame, text=f'  "{defn.example}"', font=(fam, 9, 'italic'),
                                      bg=config.POPUP_BG_COLOR, fg='#888888', anchor='w',
                                      wraplength=config.POPUP_WIDTH - 60, justify='left')
                    ex_lbl.pack(fill='x', padx=(pad + 20, pad), pady=(0, 2))

                if defn.synonyms:
                    syn_text = 'Synonyms: ' + ', '.join(defn.synonyms[:5])
                    tk.Label(frame, text=syn_text, font=(fam, 8),
                             bg=config.POPUP_BG_COLOR, fg='#7986CB', anchor='w',
                             wraplength=config.POPUP_WIDTH - 60, justify='left').pack(
                        fill='x', padx=(pad + 20, pad), pady=(0, 2))

        # Korean translation section
        tk.Frame(frame, bg='#E0E0E0', height=1).pack(fill='x', padx=pad, pady=6)
        tk.Label(frame, text=config.t('korean_title'), font=(fam, 11, 'bold'),
                 bg=config.POPUP_BG_COLOR, fg='#1565C0', anchor='w').pack(
            fill='x', padx=pad, pady=(2, 4))

        # Collect all definitions for translation
        all_defs = []
        for meaning in result.meanings:
            pos = meaning.part_of_speech or ''
            for defn in meaning.definitions:
                all_defs.append(f'({pos}) {defn.definition}')
        en_text = '\n'.join(all_defs)

        kr_label = tk.Label(frame, text=config.t('translating'), font=(fam, 10),
                            bg='#F5F5F5', fg='#333333', anchor='w',
                            wraplength=config.POPUP_WIDTH - 50, justify='left',
                            padx=6, pady=4, relief='flat')
        kr_label.pack(fill='x', padx=pad, pady=(0, 4))

        def _do_translate():
            translated = translate_to_korean(en_text)
            if translated:
                self._root.after(0, lambda: kr_label.configure(text=translated))
            else:
                self._root.after(0, lambda: kr_label.configure(text=config.t('translation_failed'), fg='#999999'))

        import threading
        threading.Thread(target=_do_translate, daemon=True).start()

        # Save to wordbook button
        if on_save:
            btn_frame = tk.Frame(frame, bg=config.POPUP_BG_COLOR)
            btn_frame.pack(fill='x', padx=pad, pady=(8, pad))

            def _do_save(btn):
                on_save(result)
                btn.configure(text=config.t('saved_btn'), state='disabled', bg='#C8E6C9')

            save_btn = tk.Button(btn_frame, text=config.t('save_btn'), font=(fam, 9),
                                 relief='groove', bg='#E3F2FD', cursor='hand2')
            save_btn.configure(command=lambda: _do_save(save_btn))
            save_btn.pack(side='right')

        # Update geometry after rendering
        top.update_idletasks()
        req_h = frame.winfo_reqheight() + 4
        h = min(req_h, config.POPUP_MAX_HEIGHT)
        w = config.POPUP_WIDTH

        # Keep on screen
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()
        if x + w > sw:
            x = sw - w - 10
        if y + h > sh:
            y = sh - h - 10

        top.geometry(f'{w}x{h}+{x}+{y}')

        # Close on focus out / Escape
        top.bind('<Escape>', lambda e: self.close())
        top.bind('<FocusOut>', lambda e: self._schedule_close())
        top.focus_force()

    def _schedule_close(self):
        if self._top:
            self._top.after(200, self._check_focus)

    def _check_focus(self):
        try:
            if self._top and self._root.focus_get() is None:
                self.close()
        except Exception:
            logger.debug("Focus check failed, closing popup", exc_info=True)
            self.close()

    def show_error(self, word: str, message: str):
        self.close()
        self._top = top = tk.Toplevel(self._root)
        top.overrideredirect(True)
        top.attributes('-topmost', True)
        top.configure(bg=config.POPUP_BG_COLOR, highlightbackground='#FF5252',
                      highlightthickness=1)

        x = self._root.winfo_pointerx() + 15
        y = self._root.winfo_pointery() + 15

        fam = config.POPUP_FONT_FAMILY
        tk.Label(top, text=f'"{word}" {config.t("not_found")}', font=(fam, 12, 'bold'),
                 bg=config.POPUP_BG_COLOR, fg='#D32F2F').pack(padx=12, pady=(10, 4))
        tk.Label(top, text=message, font=(fam, 9),
                 bg=config.POPUP_BG_COLOR, fg='#666666').pack(padx=12, pady=(0, 10))

        top.update_idletasks()
        w = max(top.winfo_reqwidth(), 250)
        h = top.winfo_reqheight()
        top.geometry(f'{w}x{h}+{x}+{y}')

        top.bind('<Escape>', lambda e: self.close())
        top.bind('<FocusOut>', lambda e: self.close())
        top.focus_force()
        top.after(3000, self.close)

    def close(self):
        if self._top:
            try:
                self._top.destroy()
            except Exception:
                logger.debug("Failed to destroy popup window", exc_info=True)
            self._top = None
