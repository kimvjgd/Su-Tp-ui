"""라즈베리파이에서 한글 폰트가 왜 안 보이는지 진단한다.

사용법 (라즈베리파이 '데스크톱 화면'의 터미널에서):
    python3 check_font.py
"""
import subprocess
import tkinter as tk
from tkinter import font as tkfont

from standup_ui.application import App

TEST = "설정 준비됨 레이저"


def sh(*cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except (OSError, subprocess.SubprocessError) as e:
        return f"(실행 실패: {e})"


print("=" * 64)
print("1) 시스템에 한글 폰트가 설치되어 있는가?  (fc-list :lang=ko)")
ko = sh("fc-list", ":lang=ko", "family")
if ko:
    for line in sorted(set(ko.splitlines()))[:15]:
        print("   ", line)
    print(f"    -> 한글 폰트 {len(set(ko.splitlines()))}종 설치됨. OK")
else:
    print("    >>> 없음! 한글 폰트가 설치되어 있지 않습니다. 이것이 원인입니다.")
    print("    >>> sudo apt install fonts-noto-cjk  후  fc-cache -fv")

print("=" * 64)
print("2) fontconfig가 추천하는 한글 폰트  (fc-match :lang=ko)")
print("   ", sh("fc-match", "-f", "%{family}", ":lang=ko") or "(없음)")

root = tk.Tk()
root.withdraw()

print("=" * 64)
print("3) 앱이 최종적으로 고르는 폰트")
picked = App._pick_family()
print(f"    >>> _pick_family() = {picked!r}")

print("=" * 64)
print("4) 그 폰트가 한글을 실제로 그리는가?  (글리프 유무 판정)")


def renders_hangul(family):
    """한글 글리프가 없으면 Tk는 모든 문자를 같은 폭의 □로 그린다.
    서로 폭이 크게 다른 한글 두 글자의 폭이 같으면 글리프가 없다는 뜻."""
    f = tkfont.Font(family=family, size=20)
    w_ko = f.measure("한")
    w_box = f.measure("鿿")  # 폰트에 거의 없는 CJK 문자 = 확실한 두부(□) 폭
    return w_ko > 0 and w_ko != w_box


for family in (picked, "Noto Sans CJK KR", "NanumGothic"):
    ok = renders_hangul(family)
    print(f"    {family:22s} : {'한글 렌더 가능 OK' if ok else '>>> 한글 글리프 없음 (□)'}")

print("=" * 64)
print("5) 창을 띄웁니다. 한글이 보이는 줄이 있으면 그 폰트 이름을 알려주세요.")
root.deiconify()
root.title("font check")
root.geometry("680x300")
root.configure(bg="#0d141c")
for family in (picked, "Noto Sans CJK KR", "NanumGothic", "DejaVu Sans"):
    tk.Label(root, text=f"[{family}]  {TEST}",
             font=tkfont.Font(family=family, size=18),
             bg="#0d141c", fg="#e8eef4").pack(anchor="w", padx=16, pady=8)
root.mainloop()
