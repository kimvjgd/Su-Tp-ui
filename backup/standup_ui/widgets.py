import tkinter as tk


def styled_button(parent, text, command, *, fg, bg, font, active):
    return tk.Button(
        parent, text=text, command=command,
        font=font, fg=fg, bg=bg,
        activebackground=active, activeforeground=fg,
        relief="flat", bd=0, highlightthickness=0, cursor="hand2",
    )


def panel(parent, app, title=None):
    c = app.colors
    outer = tk.Frame(parent, bg=c["panel"], highlightthickness=1,
                     highlightbackground=c["line"])
    if title:
        tk.Label(outer, text=title, font=app.f_h2, bg=c["panel"],
                 fg=c["accent"], anchor="w").pack(fill="x", padx=12, pady=(8, 2))
    return outer
