import flet as ft
from src.ui.app import main_routing

def main():
    if hasattr(ft, "run"):
        ft.run(main=main_routing)
    else:
        ft.app(target=main_routing)

if __name__ == "__main__":
    main()