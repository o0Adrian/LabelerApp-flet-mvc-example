from flet_mvc import FletView
import flet as ft

# view
class MainView(FletView):
    def __init__(self, controller, model):
        view = [
            ft.Row(
                controls=[
                    ft.Text(
                        "Supermarket",
                        size=36,
                        weight="w700",
                    ),
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        icon_color=ft.colors.BLACK26,
                        icon_size=28,
                        tooltip="Reload",
                        on_click=controller.reload_app
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                controls=[
                    ft.Text(ref=model.info, value=model.found_invoices(), size=18),
                ]
            ),
            ft.ListView(
                ref=model.checkboxes,
                expand=True
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        alignment=ft.alignment.bottom_center,
                        margin=ft.margin.only(bottom=-10, top=10),
                        content=(
                            ft.Text(
                                "Utility",
                                size=14,
                                color=ft.colors.BLACK26,
                            )
                        )
                    ),
                ]                        
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        hint_text="0.0",
                        suffix_text="%",
                        border=ft.InputBorder.NONE,
                        filled=True,
                        expand=True,
                        keyboard_type="number",
                        on_change=controller.check_digits_only,
                        on_submit=controller.create_labels
                    ),
                    ft.Container(
                        alignment=ft.alignment.bottom_center,
                        content=(
                            ft.ElevatedButton(
                                content=ft.Text("Create Labels", size=18, weight="w700"),
                                on_click=controller.create_labels,
                                bgcolor="#f7ce7c",
                                color="black",
                                width=220,
                                height=50,
                            )
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
        ]
        super().__init__(model, view, controller)
