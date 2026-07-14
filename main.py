import argparse

from standup_ui import App


def main():
    parser = argparse.ArgumentParser(description="STANDUP THERAPEUTICS UI")
    parser.add_argument("--windowed", action="store_true",
                        help="제목표시줄이 있는 창 모드로 실행 (개발용)")
    args = parser.parse_args()

    app = App(fullscreen=not args.windowed)
    app.mainloop()


if __name__ == "__main__":
    main()
