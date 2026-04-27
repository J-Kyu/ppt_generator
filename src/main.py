import flet as ft
from ui.app import main_routing

<<<<<<< HEAD
def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        input.value = str(int(input.value) - 1)

    def plus_click(e):
        input.value = str(int(input.value) + 1)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                input,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
        )
    )

ft.run(main)
=======
def main():
    # flet 0.84.0+ 에서는 app 대신 run을 권환
    if hasattr(ft, "run"):
        ft.run(main=main_routing)
    else:
        ft.app(target=main_routing)

if __name__ == "__main__":
    main()
>>>>>>> 23ad0dfc8c586fe2d46acf3bad4b656ff7f3478c
