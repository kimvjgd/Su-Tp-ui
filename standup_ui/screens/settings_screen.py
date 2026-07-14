import tkinter as tk

from ..widgets import RoundButton, Card, RoundFrame
from ..theme import ON_DARK_TEXT


class SettingsScreen(tk.Frame):
    def __init__(self, parent, app):
        self.c = app.colors
        super().__init__(parent, bg=self.c["bg"])
        self.app = app
        c = self.c

        bar = tk.Frame(self, bg=c["bg"], height=58)
        bar.pack(fill="x", side="top", padx=12)
        bar.pack_propagate(False)
        tk.Label(bar, text="⚙  설정", font=app.f_title, bg=c["bg"],
                 fg=c["text"]).pack(side="left")
        RoundButton(bar, "← 뒤로", lambda: app.show("MainScreen"),
                    bg=c["panel2"], fg=c["text"], font=app.f_btn,
                    width=96, height=36).pack(side="right", pady=11)

        card = Card(self, app, "환경 설정")
        card.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        body = card.body

        self._row(body, "테마", self._theme_seg)
        self._row(body, "스캔 속도",
                  lambda p: tk.Label(p, text="보통", font=self.app.f_body,
                                     bg=self.c["panel"], fg=self.c["accent"]))

    def _row(self, parent, name, right_factory):
        c = self.c
        row = tk.Frame(parent, bg=c["panel"])
        row.pack(fill="x", pady=10)
        tk.Label(row, text=name, font=self.app.f_h2, bg=c["panel"],
                 fg=c["text"], anchor="w").pack(side="left")
        right_factory(row).pack(side="right")
        tk.Frame(parent, bg=c["line"], height=1).pack(fill="x")

    def _theme_seg(self, parent):
        c = self.c
        seg = RoundFrame(parent, bg=c["panel2"], width=184, height=42, radius=14)
        for label, key in (("Dark", "dark"), ("Light", "light")):
            active = (self.app.theme_name == key)
            RoundButton(seg.body, label, lambda k=key: self.app.set_theme(k),
                        bg=c["accent"] if active else c["panel2"],
                        fg=ON_DARK_TEXT if active else c["sub"],
                        font=self.app.f_btn, radius=11, width=87, height=36,
                        pad_bg=c["panel2"]).pack(side="left")
        return seg
