import math
import tkinter as tk

from ..widgets import styled_button, panel
from ..theme import ON_DARK_TEXT


class MainScreen(tk.Frame):
    def __init__(self, parent, app):
        self.c = app.colors
        super().__init__(parent, bg=self.c["bg"])
        self.app = app
        self.active_entry = None

        self._build_topbar()

        body = tk.Frame(self, bg=self.c["bg"])
        body.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        body.grid_columnconfigure(0, weight=3, uniform="col")
        body.grid_columnconfigure(1, weight=2, uniform="col")
        body.grid_rowconfigure(0, weight=1)

        self._build_user_panel(body)
        self._build_operator_panel(body)
        self._reflect_laser()

    def _build_topbar(self):
        c = self.c
        bar = tk.Frame(self, bg=c["panel"], height=46)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        tk.Label(bar, text="STANDUP THERAPEUTICS", font=self.app.f_title,
                 bg=c["panel"], fg=c["text"]).pack(side="left", padx=16)

        styled_button(bar, "Exit", self.app.quit, bg=c["red"], fg=c["text"],
                      font=self.app.f_btn, active=c["red"]).pack(
            side="right", padx=(4, 12), ipadx=10, ipady=4)
        styled_button(bar, "⚙  Setting", lambda: self.app.show("SettingsScreen"),
                      bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                      active=c["blue"]).pack(side="right", padx=4, ipadx=10, ipady=4)

    def _build_user_panel(self, parent):
        c = self.c
        p = panel(parent, self.app)
        p.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        ctrl = tk.Frame(p, bg=c["panel"])
        ctrl.pack(fill="x", padx=12, pady=(12, 6))
        for col in range(4):
            ctrl.grid_columnconfigure(col, weight=1, uniform="ctrl")

        styled_button(ctrl, "Home", lambda: self._log("Home: 모터/카트리지 원점 이동"),
                      bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                      active=c["blue"]).grid(row=0, column=0, sticky="ew",
                                             padx=(0, 4), ipady=8)
        self._labeled_entry(ctrl, "ST.P", self.app.stp_var).grid(row=0, column=1)
        self._labeled_entry(ctrl, "SC.D", self.app.scd_var).grid(row=0, column=2)
        styled_button(ctrl, "Start", lambda: self._log("Start: 전체 동작 시작"),
                      bg=c["green"], fg=ON_DARK_TEXT, font=self.app.f_btn,
                      active=c["green"]).grid(row=0, column=3, sticky="ew",
                                              padx=(4, 0), ipady=8)

        self.graph = tk.Canvas(p, bg=c["graph_bg"], highlightthickness=1,
                               highlightbackground=c["line"])
        self.graph.pack(fill="both", expand=True, padx=12, pady=6)
        self.graph.bind("<Configure>", lambda e: self._draw_graph())

        bottom = tk.Frame(p, bg=c["panel"])
        bottom.pack(fill="x", padx=12, pady=(2, 10))
        styled_button(bottom, "Save", lambda: self._log("Save: 설정 셋팅 저장"),
                      bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                      active=c["blue"]).pack(side="left", expand=True, fill="x",
                                             padx=(0, 4), ipady=8)
        styled_button(bottom, "Output", lambda: self._log("Output: 그래프 값 데이터 출력"),
                      bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                      active=c["blue"]).pack(side="left", expand=True, fill="x",
                                             padx=(4, 0), ipady=6)

        self.status = tk.Label(p, text="준비됨", font=self.app.f_body,
                               bg=c["panel"], fg=c["sub"], anchor="w")
        self.status.pack(fill="x", padx=12, pady=(0, 10))

    def _build_operator_panel(self, parent):
        c = self.c
        p = panel(parent, self.app, "OPERATOR")
        p.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        laser = tk.Frame(p, bg=c["panel"])
        laser.pack(fill="x", padx=12, pady=(2, 4))
        tk.Label(laser, text="Laser", font=self.app.f_body, bg=c["panel"],
                 fg=c["sub"], width=6, anchor="w").pack(side="left")
        self.btn_on = styled_button(laser, "ON", lambda: self._set_laser(True),
                                    bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                                    active=c["sel_bg"])
        self.btn_on.pack(side="left", expand=True, fill="x", padx=2, ipady=6)
        self.btn_off = styled_button(laser, "OFF", lambda: self._set_laser(False),
                                     bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                                     active=c["sel_bg"])
        self.btn_off.pack(side="left", expand=True, fill="x", padx=2, ipady=6)

        tk.Label(p, text="Motor position", font=self.app.f_body, bg=c["panel"],
                 fg=c["sub"], anchor="w").pack(fill="x", padx=12, pady=(6, 0))
        motor = tk.Frame(p, bg=c["panel"])
        motor.pack(fill="x", padx=12, pady=(2, 6))
        motor.grid_columnconfigure(0, weight=0)
        motor.grid_columnconfigure(1, weight=1, uniform="m")
        motor.grid_columnconfigure(2, weight=1, uniform="m")
        self._labeled_entry(motor, "A", self.app.a_var).grid(
            row=0, column=0, padx=(0, 8))
        styled_button(motor, "Move",
                      lambda: self._log(f"Move: A={self.app.a_var.get()} 만큼 구동"),
                      bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                      active=c["blue"]).grid(row=0, column=1, sticky="ew",
                                             padx=3, ipady=6)
        styled_button(motor, "Scan", lambda: self._log("Scan: 설정값만큼 스캔 구동"),
                      bg=c["panel2"], fg=c["text"], font=self.app.f_btn,
                      active=c["blue"]).grid(row=0, column=2, sticky="ew",
                                             padx=3, ipady=6)

        self._build_keypad(p)

    def _build_keypad(self, parent):
        c = self.c
        pad = tk.Frame(parent, bg=c["panel"])
        pad.pack(fill="both", expand=True, padx=12, pady=(6, 4))
        for col in range(3):
            pad.grid_columnconfigure(col, weight=1, uniform="k")
        for r in range(4):
            pad.grid_rowconfigure(r, weight=1, uniform="kr")

        layout = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["C", "0", "←"],
        ]
        for r, row_keys in enumerate(layout):
            for col, k in enumerate(row_keys):
                if k == "C":
                    cmd, bg, act = self._clear, c["line"], c["red"]
                elif k == "←":
                    cmd, bg, act = self._backspace, c["line"], c["red"]
                else:
                    cmd, bg, act = (lambda d=k: self._key(d)), c["panel2"], c["blue"]
                styled_button(pad, k, cmd, bg=bg, fg=c["text"],
                              font=self.app.f_key, active=act).grid(
                    row=r, column=col, sticky="nsew", padx=3, pady=3)

    def _labeled_entry(self, parent, label, var, width=4):
        c = self.c
        wrap = tk.Frame(parent, bg=c["panel"])
        tk.Label(wrap, text=label, font=self.app.f_body, bg=c["panel"],
                 fg=c["sub"]).pack(side="left", padx=(0, 6))
        e = tk.Entry(wrap, width=width, font=self.app.f_entry, justify="center",
                     textvariable=var, bg=c["panel2"], fg=c["text"],
                     insertbackground=c["text"], relief="flat", highlightthickness=1,
                     highlightbackground=c["line"], highlightcolor=c["accent"])
        e.pack(side="left", ipady=5, ipadx=4)
        e.bind("<FocusIn>", lambda ev: self._set_active(e))
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

    def _set_laser(self, on):
        self.app.laser_on = on
        self._reflect_laser()
        self._log("Laser ON: 레이저 활성화" if on else "Laser OFF: 레이저 비활성화")

    def _reflect_laser(self):
        c = self.c
        if self.app.laser_on:
            self.btn_on.config(bg=c["sel_bg"], fg=c["sel_fg"])
            self.btn_off.config(bg=c["panel2"], fg=c["text"])
        else:
            self.btn_off.config(bg=c["sel_bg"], fg=c["sel_fg"])
            self.btn_on.config(bg=c["panel2"], fg=c["text"])

    def _log(self, msg):
        self.status.config(text=msg, fg=self.c["accent"])

    def _draw_graph(self):
        c = self.graph
        cl = self.c
        c.delete("all")
        w, h = c.winfo_width(), c.winfo_height()
        if w < 10 or h < 10:
            return
        pad = 8
        for i in range(1, 8):
            x = pad + (w - 2 * pad) * i / 8
            c.create_line(x, pad, x, h - pad, fill=cl["graph_grid"])
        for i in range(1, 5):
            y = pad + (h - 2 * pad) * i / 5
            c.create_line(pad, y, w - pad, y, fill=cl["graph_grid"])
        c.create_line(pad, h - pad, w - pad, h - pad, fill=cl["line"])
        c.create_line(pad, pad, pad, h - pad, fill=cl["line"])
        c.create_text(pad + 6, pad + 4, text="Graph", anchor="nw",
                      fill=cl["sub"], font=self.app.f_body)
        pts = []
        n = 120
        for i in range(n + 1):
            t = i / n
            x = pad + (w - 2 * pad) * t
            val = math.sin(t * math.pi * 4) * math.exp(-t * 1.6)
            y = (h / 2) - val * (h * 0.32)
            pts.extend((x, y))
        c.create_line(*pts, fill=cl["accent"], width=2, smooth=True)
