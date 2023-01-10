from mvc.controller import Controller
from mvc.view import MainView
from mvc.model import Model

import flet as ft

def main(page):
    # MVC set-up
    model = Model()
    controller = Controller(page, model)
    view = MainView(controller, model)
    
    # model operations
    model.controller = controller
    model.create_checkboxes()
    
    
    # Settings
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.on_keyboard_event = controller.on_keyboard
    page.theme_mode = "light"
    page.padding = 20
    page.window_width = 580
    page.window_always_on_top = True
    page.window_resizable = False
    page.window_height = 500
    
    # Run
    page.add(
        *view.content
    )

ft.app(target=main)
    