import dearpygui.dearpygui as dpg
from .database_editor import DatabaseEditor

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("assets/Maple_Mono_NF_Italic.ttf", 15)
    second_font = dpg.add_font("assets/Maple_Mono_NF_Regular.ttf", 15)


DatabaseEditor()

dpg.bind_font(default_font)
dpg.create_viewport(title="Alchemist v0.0.1.dev1")
dpg.set_primary_window("!database_editor", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
