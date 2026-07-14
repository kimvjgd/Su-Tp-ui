"""라즈베리파이에서 한글 폰트가 왜 안 보이는지 진단한다.

사용법 (라즈베리파이 데스크톱 터미널에서):
    python3 check_font.py
"""
import subprocess
import sys
import tkinter as tk
from tkinter import font as tkfont

from standup_ui.config import FONT_STACK, KOREAN_FONT_HINTS, FALLBACK_FONTS
from standup_ui.application import App

TEST = "설정 준비됨 레이저 한글"


def sh(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
    except Exception as e:  # noqa: BLE001
        return f"(실행 실패: {e})"


print("=" * 60)
print("1) 시스템에 설치된 한글 폰트 (fc-list :lang=ko)")
ko = sh("fc-list :lang=ko family")
print(ko if ko else "  >>> 없음! 한글 폰트가 설치되어 있지 않습니다.")

print("=" * 60)
print("2) Tk가 인식하는 폰트 패밀리 중 한글로 보이는 것")
root = tk.Tk()
root.withdraw()
fams = sorted(tkfont.families())
hits = [f for f in fams if any(h in f.lower() for h in KOREAN_FONT_HINTS)]
print("  " + (", ".join(hits) if hits else ">>> 없음"))
print(f"  (Tk가 보는 전체 패밀리 개수: {len(fams)})")

print("=" * 60)
print("3) 앱이 실제로 고르는 폰트")
picked = App._pick_family(None)
print(f"  >>> _pick_family() = {picked!r}")
print(f"  FONT_STACK     = {FONT_STACK}")
print(f"  FALLBACK_FONTS = {FALLBACK_FONTS}")

print("=" * 60)
print("4) 그 폰트로 한글을 실제로 그릴 수 있는지 (폭 측정)")
f = tkfont.Font(family=picked, size=16)
w_ko = f.measure(TEST)
w_en = f.measure("ABCD" * 3)
print(f"  '{TEST}' 폭 = {w_ko}px")
print(f"  영문 12자     폭 = {w_en}px")
if w_ko == 0:
    print("  >>> 폭이 0. 글리프가 없어 아무것도 안 그려집니다.")

print("=" * 60)
print("5) 창을 띄웁니다. 아래 3줄이 보이는지 눈으로 확인하세요. (닫으려면 창 X)")
root.deiconify()
root.title("font check")
root.geometry("640x260")
root.configure(bg="#0d141c")
for label, family in ((f"picked: {picked}", picked),
                      ("Noto Sans CJK KR", "Noto Sans CJK KR"),
                      ("NanumGothic", "NanumGothic")):
    tk.Label(root, text=f"[{label}]  {TEST}",
             font=tkfont.Font(family=family, size=18),
             bg="#0d141c", fg="#e8eef4").pack(anchor="w", padx=16, pady=10)
tk.Label(root, text="한글이 보이는 줄이 있으면 그 폰트 이름을 알려주세요.",
         font=tkfont.Font(family=picked, size=11),
         bg="#0d141c", fg="#8ea0b2").pack(anchor="w", padx=16, pady=10)
root.mainloop()
