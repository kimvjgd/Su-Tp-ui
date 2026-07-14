import tkinter as tk

from .theme import RADIUS_BTN, RADIUS_CARD, RADIUS_INPUT


def _rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    ra, ga, ba = _rgb(a)
    rb, gb, bb = _rgb(b)
    return "#%02x%02x%02x" % (
        round(ra + (rb - ra) * t),
        round(ga + (gb - ga) * t),
        round(ba + (bb - ba) * t),
    )


def is_dark(color):
    r, g, b = _rgb(color)
    return (0.299 * r + 0.587 * g + 0.114 * b) < 140


def hover_of(color):
    return mix(color, "#ffffff", 0.12) if is_dark(color) else mix(color, "#000000", 0.07)


def press_of(color):
    return mix(color, "#000000", 0.14) if is_dark(color) else mix(color, "#000000", 0.16)


def round_rect(canvas, x1, y1, x2, y2, r, **kw):
    """Draw a rounded rectangle as a smoothed polygon."""
    r = max(0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    pts = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, splinesteps=24, **kw)


class RoundButton(tk.Canvas):
    """Canvas-backed button with rounded corners and hover/press feedback."""

    def __init__(self, parent, text, command=None, *, fg, bg, font,
                 radius=RADIUS_BTN, height=40, width=96, pad_bg=None):
        super().__init__(parent, width=width, height=height, bd=0,
                         highlightthickness=0, takefocus=0, cursor="hand2",
                         bg=pad_bg or parent.cget("bg"))
        self._text = text
        self._cmd = command
        self._font = font
        self._fg = fg
        self._bg = bg
        self._radius = radius
        self._hover = False
        self._press = False

        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _fill(self):
        if self._press:
            return press_of(self._bg)
        if self._hover:
            return hover_of(self._bg)
        return self._bg

    def _draw(self):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2 or h < 2:
            return
        round_rect(self, 1, 1, w - 1, h - 1, self._radius,
                   fill=self._fill(), outline="")
        self.create_text(w / 2, h / 2 + 1, text=self._text,
                         fill=self._fg, font=self._font)

    def _on_enter(self, _e):
        self._hover = True
        self._draw()

    def _on_leave(self, _e):
        self._hover = False
        self._press = False
        self._draw()

    def _on_press(self, _e):
        self._press = True
        self._draw()

    def _on_release(self, e):
        fired = self._press
        self._press = False
        self._draw()
        inside = 0 <= e.x <= self.winfo_width() and 0 <= e.y <= self.winfo_height()
        if fired and inside and self._cmd:
            self._cmd()

    def set_colors(self, bg=None, fg=None, text=None):
        if bg:
            self._bg = bg
        if fg:
            self._fg = fg
        if text:
            self._text = text
        self._draw()

    def configure(self, **kw):
        bg = kw.pop("bg", None) or kw.pop("background", None)
        fg = kw.pop("fg", None) or kw.pop("foreground", None)
        text = kw.pop("text", None)
        if bg or fg or text:
            self.set_colors(bg, fg, text)
        if kw:
            super().configure(**kw)

    config = configure


class RoundEntry(tk.Canvas):
    """Canvas-backed entry with a rounded, focus-aware frame."""

    def __init__(self, parent, textvariable, *, font, bg, fg, line, accent,
                 width=78, height=40, radius=RADIUS_INPUT, pad_bg=None):
        super().__init__(parent, width=width, height=height, bd=0,
                         highlightthickness=0, takefocus=0,
                         bg=pad_bg or parent.cget("bg"))
        self._bg = bg
        self._line = line
        self._accent = accent
        self._radius = radius
        self._focused = False

        self.entry = tk.Entry(self, textvariable=textvariable, font=font,
                              justify="center", bg=bg, fg=fg, insertbackground=accent,
                              relief="flat", bd=0, highlightthickness=0)
        self._win = self.create_window(0, 0, anchor="nw", window=self.entry)

        self.entry.bind("<FocusIn>", self._on_focus, add="+")
        self.entry.bind("<FocusOut>", self._on_blur, add="+")
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Button-1>", lambda e: self.entry.focus_set())

    def _draw(self):
        self.delete("frame")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2 or h < 2:
            return
        round_rect(self, 1, 1, w - 1, h - 1, self._radius, fill=self._bg,
                   outline=self._accent if self._focused else self._line,
                   width=2 if self._focused else 1, tags="frame")
        self.tag_lower("frame")
        self.coords(self._win, 8, 6)
        self.itemconfigure(self._win, width=w - 16, height=h - 12)

    def _on_focus(self, _e=None):
        self._focused = True
        self._draw()

    def _on_blur(self, _e=None):
        self._focused = False
        self._draw()


class RoundFrame(tk.Canvas):
    """Small rounded container (e.g. segmented control). Add children to `.body`."""

    def __init__(self, parent, *, bg, width, height, radius=12, pad=3, pad_bg=None):
        super().__init__(parent, width=width, height=height, bd=0,
                         highlightthickness=0, bg=pad_bg or parent.cget("bg"))
        self._bg = bg
        self._radius = radius
        self._pad = pad
        self.body = tk.Frame(self, bg=bg)
        self._win = self.create_window(pad, pad, anchor="nw", window=self.body)
        self.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.delete("frame")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2 or h < 2:
            return
        round_rect(self, 1, 1, w - 1, h - 1, self._radius, fill=self._bg,
                   outline="", tags="frame")
        self.tag_lower("frame")
        p = self._pad
        self.itemconfigure(self._win, width=w - 2 * p, height=h - 2 * p)


class Card(tk.Canvas):
    """Rounded panel. Add children to `.body`."""

    def __init__(self, parent, app, title=None, radius=RADIUS_CARD, pad=12):
        c = app.colors
        super().__init__(parent, width=10, height=10, bd=0, highlightthickness=0,
                         bg=parent.cget("bg"))
        self._c = c
        self._radius = radius
        self._pad = pad

        self.body = tk.Frame(self, bg=c["panel"])
        self._win = self.create_window(pad, pad, anchor="nw", window=self.body)

        if title:
            tk.Label(self.body, text=title, font=app.f_h2, bg=c["panel"],
                     fg=c["accent"], anchor="w").pack(fill="x", pady=(0, 6))

        self.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.delete("card")
        w, h = self.winfo_width(), self.winfo_height()
        if w < 2 or h < 2:
            return
        round_rect(self, 1, 1, w - 1, h - 1, self._radius,
                   fill=self._c["panel"], outline=self._c["line"], width=1,
                   tags="card")
        self.tag_lower("card")
        p = self._pad
        self.itemconfigure(self._win, width=w - 2 * p, height=h - 2 * p)
