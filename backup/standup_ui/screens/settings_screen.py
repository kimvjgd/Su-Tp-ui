import tkinter as tk

from ..widgets import styled_button, panel
from ..theme import ON_DARK_TEXT


class SettingsScreen(tk.Frame):
    def __init__(self, parent, app):
        self.c = app.colors
        super().__init__(parent, bg=self.c["bg"])
        self.app = app
        c = self.c

        bar = tk.Frame(self, bg=c["panel"], height=46)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)
        tk.Label(bar, text="⚙  설정", font=app.f_title, bg=c["panel"],
                 fg=c["text"]).pack(side="left", padx=16)
        styled_button(bar, "← 뒤로", lambda: app.show("MainScreen"),
                      bg=c["panel2"], fg=c["text"], font=app.f_btn,
                      active=c["blue"]).pack(side="right", padx=12, ipadx=10, ipady=4)

        body = panel(self, app, "환경 설정")
        body.pack(fill="both", expand=True, padx=12, pady=12)

        theme_row = tk.Frame(body, bg=c["panel"])
        theme_row.pack(fill="x", padx=16, pady=(12, 8))
        tk.Label(theme_row, text="테마 (Dark / Light)", font=app.f_h2,
                 bg=c["panel"], fg=c["text"], anchor="w").pack(side="left")

        seg = tk.Frame(theme_row, bg=c["line"], highlightthickness=0)
        seg.pack(side="right")
        self._theme_btn("Dark", "dark", seg)
        self._theme_btn("Light", "light", seg)
        tk.Frame(body, bg=c["line"], height=1).pack(fill="x", padx=16)

        for name, val in [("스캔 속도", "보통")]:
            row = tk.Frame(body, bg=c["panel"])
            row.pack(fill="x", padx=16, pady=8)
            tk.Label(row, text=name, font=app.f_h2, bg=c["panel"],
                     fg=c["text"], anchor="w").pack(side="left")
            tk.Label(row, text=val, font=app.f_body, bg=c["panel"],
                     fg=c["accent"]).pack(side="right")
            tk.Frame(body, bg=c["line"], height=1).pack(fill="x", padx=16)

    def _theme_btn(self, text, theme_key, parent):
        c = self.c
        active = (self.app.theme_name == theme_key)
        btn = styled_button(
            parent, text, lambda: self.app.set_theme(theme_key),
            bg=c["accent"] if active else c["panel2"],
            fg=ON_DARK_TEXT if active else c["text"],
            font=self.app.f_btn, active=c["blue"])
        btn.pack(side="left", padx=1, ipadx=18, ipady=6)
        return btn
