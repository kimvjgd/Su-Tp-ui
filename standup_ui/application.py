import subprocess
import sys
import tkinter as tk
from tkinter import font as tkfont

from .config import (SCREEN_W, SCREEN_H, APP_TITLE, DEFAULT_THEME, FONT_STACK,
                     KOREAN_FONT_HINTS, FALLBACK_FONTS, FULLSCREEN)
from .theme import THEMES
from .screens.main_screen import MainScreen
from .screens.settings_screen import SettingsScreen


class App(tk.Tk):
    SCREENS = (MainScreen, SettingsScreen)

    def __init__(self, fullscreen=FULLSCREEN):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{SCREEN_W}x{SCREEN_H}")
        self.resizable(False, False)

        # 전체화면이면 창 테두리와 제목표시줄(최소화/전체화면/닫기)이 함께 사라진다.
        # 종료는 화면 우상단 Exit 버튼, 임시 해제는 F11 / Escape.
        self.attributes("-fullscreen", fullscreen)
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self._init_fonts()

        self.theme_name = DEFAULT_THEME
        self.colors = THEMES[self.theme_name]
        self.current = "MainScreen"
        self.stp_var = tk.StringVar(value="0")
        self.scd_var = tk.StringVar(value="100")
        self.a_var = tk.StringVar(value="0")
        self.laser_on = False

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self._build_frames()
        self.show(self.current)

    def _init_fonts(self):
        fam = self._pick_family()
        self.f_title = tkfont.Font(family=fam, size=16, weight="bold")
        self.f_h2 = tkfont.Font(family=fam, size=11, weight="bold")
        self.f_btn = tkfont.Font(family=fam, size=12, weight="bold")
        self.f_body = tkfont.Font(family=fam, size=11)
        self.f_key = tkfont.Font(family=fam, size=16, weight="bold")
        self.f_entry = tkfont.Font(family=fam, size=13, weight="bold")

    @staticmethod
    def _pick_family():
        available = {f.lower(): f for f in tkfont.families()}

        for name in FONT_STACK:
            if name.lower() in available:
                return available[name.lower()]

        # 이름만 보고 고르면 한글이 없는 'URW Gothic' 같은 폰트가 잡힌다.
        # 리눅스에서는 fontconfig에게 한글 가능 폰트를 직접 물어보는 게 정확하다.
        family = App._ask_fontconfig_for_korean()
        if family:
            return family

        for low, family in sorted(available.items()):
            if any(hint in low for hint in KOREAN_FONT_HINTS):
                return family

        print("[warn] 한글 폰트가 없습니다. 한글이 네모(□)로 보입니다.\n"
              "       설치: sudo apt install fonts-noto-cjk  (또는 fonts-nanum)\n"
              "       설치 후: fc-cache -fv", file=sys.stderr)
        for name in FALLBACK_FONTS:
            if name.lower() in available:
                return available[name.lower()]
        return "TkDefaultFont"

    @staticmethod
    def _ask_fontconfig_for_korean():
        """fc-match로 한글을 실제로 렌더할 수 있는 폰트 패밀리명을 얻는다."""
        try:
            # 한글 폰트가 하나도 없으면 fc-match는 엉뚱한 라틴 폰트를 돌려주므로
            # fc-list로 한글 지원 폰트의 존재부터 확인한다.
            listed = subprocess.run(["fc-list", ":lang=ko", "family"],
                                    capture_output=True, text=True, timeout=5)
            if listed.returncode != 0 or not listed.stdout.strip():
                return None

            matched = subprocess.run(["fc-match", "-f", "%{family}", ":lang=ko"],
                                     capture_output=True, text=True, timeout=5)
            if matched.returncode != 0:
                return None
        except (OSError, subprocess.SubprocessError):
            return None  # fc-match 없는 환경(윈도우 등)

        # fc-match는 "Noto Sans CJK KR,Noto Sans CJK KR Regular" 처럼 별칭을 붙여준다.
        for family in matched.stdout.split(","):
            family = family.strip()
            if family:
                return family
        return None

    def _build_frames(self):
        self.configure(bg=self.colors["bg"])
        self.container.configure(bg=self.colors["bg"])
        self.frames = {}
        for ScreenClass in self.SCREENS:
            screen = ScreenClass(self.container, self)
            self.frames[ScreenClass.__name__] = screen
            screen.grid(row=0, column=0, sticky="nsew")

    def set_theme(self, name):
        if name == self.theme_name or name not in THEMES:
            return
        self.theme_name = name
        self.colors = THEMES[name]
        for frame in self.frames.values():
            frame.destroy()
        self._build_frames()
        self.show(self.current)

    def show(self, name):
        self.current = name
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def _toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))
