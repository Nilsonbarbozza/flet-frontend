import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Exemplo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add()

if __name__ == "__main__":
    ft.app(target=main)
