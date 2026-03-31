import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime

import config
from storage.wordbook import Wordbook


class WordbookWindow:
    def __init__(self, root: tk.Tk, wordbook: Wordbook, on_lookup=None):
        self._root = root
        self._wordbook = wordbook
        self._on_lookup = on_lookup
        self._win = None

    def show(self):
        if self._win and self._win.winfo_exists():
            self._win.lift()
            return

        self._win = win = tk.Toplevel(self._root)
        win.title('Wordbook')
        win.geometry('400x500')
        win.configure(bg=config.POPUP_BG_COLOR)

        fam = config.POPUP_FONT_FAMILY

        header = tk.Frame(win, bg='#1565C0')
        header.pack(fill='x')
        tk.Label(header, text='My Wordbook', font=(fam, 14, 'bold'),
                 bg='#1565C0', fg='white').pack(padx=10, pady=10)

        # Word list
        list_frame = tk.Frame(win, bg=config.POPUP_BG_COLOR)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        columns = ('word', 'date')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        tree.heading('word', text='Word')
        tree.heading('date', text='Added')
        tree.column('word', width=200)
        tree.column('date', width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Populate
        for word, ts in self._wordbook.get_all():
            dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
            tree.insert('', 'end', values=(word, dt))

        # Buttons
        btn_frame = tk.Frame(win, bg=config.POPUP_BG_COLOR)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))

        def on_delete():
            sel = tree.selection()
            if sel:
                item = tree.item(sel[0])
                word = item['values'][0]
                self._wordbook.remove(word)
                tree.delete(sel[0])

        def on_lookup():
            sel = tree.selection()
            if sel and self._on_lookup:
                item = tree.item(sel[0])
                word = item['values'][0]
                threading.Thread(target=self._on_lookup, args=(word,), daemon=True).start()

        tk.Button(btn_frame, text='Look Up', font=(fam, 9), command=on_lookup,
                  relief='groove', bg='#E3F2FD', cursor='hand2').pack(side='left', padx=(0, 5))
        tk.Button(btn_frame, text='Delete', font=(fam, 9), command=on_delete,
                  relief='groove', bg='#FFEBEE', cursor='hand2').pack(side='left')
