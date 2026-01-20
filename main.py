import flet as ft
from src.ui import main_ui

def main(page: ft.Page):
    # Configuración de la ventana principal
    page.title = "Hectron-01: Interface"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = True
    
    # Cargar la interfaz de usuario desde src/ui.py
    main_ui(page)

if __name__ == "__main__":
    ft.app(target=main)
