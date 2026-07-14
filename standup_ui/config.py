SCREEN_W = 800
SCREEN_H = 480

APP_TITLE = "STANDUP THERAPEUTICS"

DEFAULT_THEME = "dark"

# 설치되어 있는 첫 번째 폰트를 사용한다. 여기 있는 폰트는 모두 한글 글리프를 가진다.
# 라즈베리파이(Debian)는 apt 패키지가 등록하는 실제 패밀리명이
# "Noto Sans CJK KR", "NanumGothic" 이므로 이름을 정확히 맞춰야 한다.
FONT_STACK = (
    "Pretendard",
    "Noto Sans KR",
    "Noto Sans CJK KR",
    "NanumGothic",
    "NanumBarunGothic",
    "UnDotum",
    "Malgun Gothic",
)

# FONT_STACK이 하나도 없을 때, 이 키워드가 든 패밀리를 한글 가능 폰트로 간주한다.
KOREAN_FONT_HINTS = ("cjk", "nanum", "gothic", "gulim", "batang", "dotum", "myeongjo")

# 한글 폰트를 끝내 못 찾았을 때만 쓰는 최후 폴백. 한글은 □로 보이므로 경고를 띄운다.
FALLBACK_FONTS = ("DejaVu Sans", "Segoe UI", "Helvetica")
