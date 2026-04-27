import flet as ft
from src.ui.app import main_routing

def main():
    # flet 0.84.0+ 에서는 app 대신 run을 권환
    if hasattr(ft, "run"):
        ft.run(main=main_routing)
    else:
        ft.app(target=main_routing)

if __name__ == "__main__":
    main()