import flet as ft

def main(page: ft.Page):
    page.title = "PPT Generator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Text("Hello, PPT Generator!", size=30, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton("Upload PPTX")
    )

if __name__ == "__main__":
    ft.app(target=main)