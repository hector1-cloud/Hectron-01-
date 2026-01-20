import flet as ft

def main_ui(page: ft.Page):
    
    # Campo de salida de texto (Log o Chat)
    output_text = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # Función para manejar el envío de comandos
    def btn_click(e):
        if input_field.value:
            output_text.controls.append(ft.Text(f"> {input_field.value}"))
            input_field.value = ""
            # Aquí conectarías con logic.py más adelante
            output_text.controls.append(ft.Text("Hectron: Procesando comando...", color=ft.colors.CYAN))
            page.update()

    # Campo de entrada
    input_field = ft.TextField(
        hint_text="Escribe un comando...",
        expand=True,
        on_submit=btn_click
    )

    # Botón de envío
    send_btn = ft.IconButton(icon=ft.icons.SEND, on_click=btn_click)

    # Layout principal
    page.add(
        ft.Container(
            content=output_text,
            expand=True,
            padding=10,
            border=ft.border.all(1, ft.colors.BLUE_GREY_100),
            border_radius=10,
        ),
        ft.Row(
            controls=[input_field, send_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )
