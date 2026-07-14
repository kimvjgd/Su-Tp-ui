import tkinter as tk
from tkinter import font as tkfont

from .config import SCREEN_W, SCREEN_H, APP_TITLE, DEFAULT_THEME
from .theme import THEMES
from .screens.main_screen import MainScreen
from .screens.settings_screen import SettingsScreen


class App(tk.Tk):
    SCREENS = (MainScreen, SettingsScreen)

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{SCREEN_W}x{SCREEN_H}")
        self.resizable(False, False)

        self.attributes("-fullscreen", False)
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
        self.f_title = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.f_h2 = tkfont.Font(family="Helvetica", size=13, weight="bold")
        self.f_btn = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.f_body = tkfont.Font(family="Helvetica", size=11)
        self.f_key = tkfont.Font(family="Helvetica", size=14, weight="bold")
        self.f_entry = tkfont.Font(family="Helvetica", size=13, weight="bold")

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
