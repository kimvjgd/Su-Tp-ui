import math
import tkinter as tk

from ..widgets import RoundButton, RoundEntry, Card, round_rect
from ..theme import ON_DARK_TEXT


class MainScreen(tk.Frame):
    def __init__(self, parent, app):
        self.c = app.colors
        super().__init__(parent, bg=self.c["bg"])
        self.app = app
        self.active_entry = None

        self._build_topbar()

        body = tk.Frame(self, bg=self.c["bg"])
        body.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        body.grid_columnconfigure(0, weight=3, uniform="col")
        body.grid_columnconfigure(1, weight=2, uniform="col")
        body.grid_rowconfigure(0, weight=1)

        self._build_user_panel(body)
        self._build_operator_panel(body)
        self._reflect_laser()

    # --- top bar -----------------------------------------------------------
    def _build_topbar(self):
        c = self.c
        bar = tk.Frame(self, bg=c["bg"], height=58)
        bar.pack(fill="x", side="top", padx=12)
        bar.pack_propagate(False)

        left = tk.Frame(bar, bg=c["bg"])
        left.pack(side="left")
        tk.Label(left, text="STANDUP", font=self.app.f_title,
                 bg=c["bg"], fg=c["text"]).pack(side="left")
        tk.Label(left, text="THERAPEUTICS", font=self.app.f_title,
                 bg=c["bg"], fg=c["accent"]).pack(side="left", padx=(6, 0))

        RoundButton(bar, "Exit", self.app.quit, bg=c["red"], fg="#ffffff",
                    font=self.app.f_btn, width=82, height=36).pack(
            side="right", padx=(8, 0), pady=11)
        RoundButton(bar, "⚙  Setting", lambda: self.app.show("SettingsScreen"),
                    bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                    width=112, height=36).pack(side="right", pady=11)

    # --- left panel --------------------------------------------------------
    def _build_user_panel(self, parent):
        c = self.c
        card = Card(parent, self.app)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        p = card.body

        ctrl = tk.Frame(p, bg=c["panel"])
        ctrl.pack(fill="x", pady=(0, 10))
        ctrl.grid_columnconfigure(0, weight=1, uniform="ctrl")
        ctrl.grid_columnconfigure(1, weight=0)
        ctrl.grid_columnconfigure(2, weight=0)
        ctrl.grid_columnconfigure(3, weight=1, uniform="ctrl")

        RoundButton(ctrl, "Home", lambda: self._log("Home: 모터/카트리지 원점 이동"),
                    bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                    height=38).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self._labeled_entry(ctrl, "ST.P", self.app.stp_var).grid(
            row=0, column=1, padx=6)
        self._labeled_entry(ctrl, "SC.D", self.app.scd_var).grid(
            row=0, column=2, padx=6)
        RoundButton(ctrl, "Start", lambda: self._log("Start: 전체 동작 시작"),
                    bg=c["green"], fg=ON_DARK_TEXT, font=self.app.f_btn,
                    height=38).grid(row=0, column=3, sticky="ew", padx=(8, 0))

        self.graph = tk.Canvas(p, bg=c["panel"], highlightthickness=0, bd=0)
        self.graph.pack(fill="both", expand=True)
        self.graph.bind("<Configure>", lambda e: self._draw_graph())

        bottom = tk.Frame(p, bg=c["panel"])
        bottom.pack(fill="x", pady=(8, 6))
        RoundButton(bottom, "Save", lambda: self._log("Save: 설정 셋팅 저장"),
                    bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                    height=36).pack(side="left", expand=True, fill="x", padx=(0, 5))
        RoundButton(bottom, "Output", lambda: self._log("Output: 그래프 값 데이터 출력"),
                    bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                    height=36).pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.status = tk.Label(p, text="● 준비됨", font=self.app.f_body,
                               bg=c["panel"], fg=c["sub"], anchor="w", height=1,
                               pady=2)
        self.status.pack(fill="x")

    # --- right panel -------------------------------------------------------
    def _build_operator_panel(self, parent):
        c = self.c
        card = Card(parent, self.app, "OPERATOR")
        card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        p = card.body

        laser = tk.Frame(p, bg=c["panel"])
        laser.pack(fill="x", pady=(2, 8))
        tk.Label(laser, text="Laser", font=self.app.f_body, bg=c["panel"],
                 fg=c["sub"], width=6, anchor="w").pack(side="left")
        self.btn_on = RoundButton(laser, "ON", lambda: self._set_laser(True),
                                  bg=c["panel2"], fg=c["text"],
                                  font=self.app.f_btn, height=38)
        self.btn_on.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.btn_off = RoundButton(laser, "OFF", lambda: self._set_laser(False),
                                   bg=c["panel2"], fg=c["text"],
                                   font=self.app.f_btn, height=38)
        self.btn_off.pack(side="left", expand=True, fill="x", padx=(4, 0))

        tk.Label(p, text="Motor position", font=self.app.f_body, bg=c["panel"],
                 fg=c["sub"], anchor="w").pack(fill="x", pady=(2, 2))
        motor = tk.Frame(p, bg=c["panel"])
        motor.pack(fill="x", pady=(0, 6))
        motor.grid_columnconfigure(0, weight=0)
        motor.grid_columnconfigure(1, weight=1, uniform="m")
        motor.grid_columnconfigure(2, weight=1, uniform="m")
        self._labeled_entry(motor, "A", self.app.a_var).grid(
            row=0, column=0, padx=(0, 8))
        RoundButton(motor, "Move",
                    lambda: self._log(f"Move: A={self.app.a_var.get()} 만큼 구동"),
                    bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                    height=38).grid(row=0, column=1, sticky="ew", padx=(0, 4))
        RoundButton(motor, "Scan", lambda: self._log("Scan: 설정값만큼 스캔 구동"),
                    bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                    height=38).grid(row=0, column=2, sticky="ew", padx=(4, 0))

        self._build_keypad(p)

    def _build_keypad(self, parent):
        c = self.c
        pad = tk.Frame(parent, bg=c["panel"])
        pad.pack(fill="both", expand=True, pady=(4, 0))
        for col in range(3):
            pad.grid_columnconfigure(col, weight=1, uniform="k")
        for r in range(4):
            pad.grid_rowconfigure(r, weight=1, uniform="kr")

        layout = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["C", "0", "⌫"],
        ]
        for r, row_keys in enumerate(layout):
            for col, k in enumerate(row_keys):
                if k == "C":
                    cmd, bg, fg = self._clear, c["line"], c["red"]
                elif k == "⌫":
                    cmd, bg, fg = self._backspace, c["line"], c["text"]
                else:
                    cmd, bg, fg = (lambda d=k: self._key(d)), c["panel2"], c["text"]
                RoundButton(pad, k, cmd, bg=bg, fg=fg, font=self.app.f_key,
                            radius=14, height=44).grid(
                    row=r, column=col, sticky="nsew", padx=4, pady=4)

    # --- inputs ------------------------------------------------------------
    def _labeled_entry(self, parent, label, var):
        c = self.c
        wrap = tk.Frame(parent, bg=c["panel"])
        tk.Label(wrap, text=label, font=self.app.f_body, bg=c["panel"],
                 fg=c["sub"]).pack(side="left", padx=(0, 6))
        re = RoundEntry(wrap, var, font=self.app.f_entry, bg=c["panel2"],
                        fg=c["text"], line=c["line"], accent=c["accent"],
                        width=74, height=42)
        re.pack(side="left")
        re.entry.bind("<FocusIn>", lambda ev: self._set_active(re.entry), add="+")
        return wrap

    def _set_active(self, entry):
        self.active_entry = entry

    def _key(self, digit):
        e = self.active_entry
        if e is None:
            return
        e.focus_set()
        e.insert("end", digit)

    def _backspace(self):
        e = self.active_entry
        if e is None or not e.get():
            return
        e.delete(len(e.get()) - 1, "end")

    def _clear(self):
        e = self.active_entry
        if e is None:
            return
        e.delete(0, "end")

    # --- laser -------------------------------------------------------------
    def _set_laser(self, on):
        self.app.laser_on = on
        self._reflect_laser()
        self._log("Laser ON: 레이저 활성화" if on else "Laser OFF: 레이저 비활성화")

    def _reflect_laser(self):
        c = self.c
        if self.app.laser_on:
            self.btn_on.set_colors(bg=c["accent"], fg=ON_DARK_TEXT)
            self.btn_off.set_colors(bg=c["panel2"], fg=c["text"])
        else:
            self.btn_off.set_colors(bg=c["sel_bg"], fg=c["sel_fg"])
            self.btn_on.set_colors(bg=c["panel2"], fg=c["text"])

    def _log(self, msg):
        self.status.config(text=f"● {msg}", fg=self.c["accent"])

    # --- graph -------------------------------------------------------------
    def _draw_graph(self):
        g = self.graph
        cl = self.c
        g.delete("all")
        w, h = g.winfo_width(), g.winfo_height()
        if w < 20 or h < 20:
            return

        round_rect(g, 1, 1, w - 1, h - 1, 12, fill=cl["graph_bg"],
                   outline=cl["line"], width=1)

        pad = 14
        for i in range(1, 8):
            x = pad + (w - 2 * pad) * i / 8
            g.create_line(x, pad, x, h - pad, fill=cl["graph_grid"])
        for i in range(1, 5):
            y = pad + (h - 2 * pad) * i / 5
            g.create_line(pad, y, w - pad, y, fill=cl["graph_grid"])
        g.create_line(pad, h - pad, w - pad, h - pad, fill=cl["line"])
        g.create_line(pad, pad, pad, h - pad, fill=cl["line"])
        g.create_text(pad + 6, pad + 4, text="Graph", anchor="nw",
                      fill=cl["sub"], font=self.app.f_body)

        pts = []
        n = 120
        for i in range(n + 1):
            t = i / n
            x = pad + (w - 2 * pad) * t
            val = math.sin(t * math.pi * 4) * math.exp(-t * 1.6)
            y = (h / 2) - val * (h * 0.30)
            pts.extend((x, y))
        g.create_line(*pts, fill=cl["accent"], width=2, smooth=True)
