# 라즈베리파이 7인치 디스플레이 해상도
SCREEN_W = 1024
SCREEN_H = 600

APP_TITLE = "STANDUP THERAPEUTICS"

DEFAULT_THEME = "dark"

# True면 제목표시줄(최소화/전체화면/닫기 버튼) 없이 전체화면으로 뜬다.
# 개발 PC에서 창 모드로 보려면: python main.py --windowed
FULLSCREEN = True

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

# FONT_STACK이 하나도 없을 때 이름으로 추측하기 위한 키워드.
# 주의: 그냥 "gothic"을 넣으면 한글이 없는 'URW Gothic', 'Century Gothic'이 잡힌다.
# 반드시 한글 폰트에서만 쓰이는 이름 조각만 넣을 것.
KOREAN_FONT_HINTS = ("cjk", "nanum", "gulim", "batang", "dotum", "myeongjo",
                     "malgun", "baekmuk", "hangul", "unbatang", "pretendard")

# 한글 폰트를 끝내 못 찾았을 때만 쓰는 최후 폴백. 한글은 □로 보이므로 경고를 띄운다.
FALLBACK_FONTS = ("DejaVu Sans", "Segoe UI", "Helvetica")
