# STAND UP THERAPEUTICS — 7inch LCD GUI

라즈베리파이 4 Model B + 공식 7인치 터치 디스플레이(800×480, 가로)용 tkinter GUI.
현재는 PC에서 개발하고, 이후 라즈베리파이로 그대로 이식할 수 있습니다.

## 실행

```bash
python main.py
```

> tkinter는 파이썬 표준 라이브러리에 기본 포함되어 별도 설치가 필요 없습니다.
> (라즈베리파이는 `sudo apt install python3-tk` 가 필요할 수 있습니다.)

조작:
- `F11` 전체화면 토글
- `Esc` 전체화면 해제

## 폴더 구조

```
software/
├── main.py                       # 실행 진입점(thin)
├── README.md
└── standup_ui/                   # 애플리케이션 패키지
    ├── __init__.py               # App 노출
    ├── config.py                 # 화면 크기/타이틀 등 전역 상수
    ├── theme.py                  # Dark/Light 테마 팔레트
    ├── widgets.py                # 공통 위젯 헬퍼(styled_button, panel)
    ├── application.py            # App: 메인 윈도우 · 화면전환 · 테마관리
    └── screens/                  # 화면(Frame)들
        ├── __init__.py
        ├── main_screen.py        # 메인 화면(User/Operator)
        └── settings_screen.py    # 설정 화면(테마 선택)
```

## 구성 개요

- **config.py** — 화면 해상도(`SCREEN_W/H`), 타이틀, 기본 테마.
- **theme.py** — `THEMES["dark"|"light"]` 색 팔레트. 위젯은 색을 하드코딩하지 않고
  `app.colors[...]` 에서 읽으므로, 테마를 바꾸면 화면을 다시 그려 일괄 적용됩니다.
- **widgets.py** — 화면들이 공통으로 쓰는 버튼/패널 헬퍼.
- **application.py** — `App(tk.Tk)`. 화면을 같은 자리에 겹쳐두고 전환하며,
  입력값(ST.P/SC.D/A)·레이저 상태를 보관해 테마 전환 후에도 유지합니다.
- **screens/** — 화면 단위로 한 파일씩. 새 화면을 추가하려면
  `screens/` 에 파일을 만들고 `App.SCREENS` 에 클래스를 등록하면 됩니다.

## 화면 기능

- **메인 — User(왼쪽)**: Home / ST.P / SC.D / Start / Graph / Save / Output / 상태표시
- **메인 — Operator(오른쪽)**: Laser ON·OFF / Motor position(A, Move, Scan) / 숫자 키패드
- **설정**: 테마(Dark / Light) 선택
