import dearpygui.dearpygui as dpg
from .widgets.node import TableNode


class DatabaseEditor:
    node_counter = 100

    def __init__(self):
        with dpg.window(label="Database editor", tag="!database_editor"):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="New database", callback=self.new_database)
                    dpg.add_menu_item(
                        label="Export to python file", callback=self.export
                    )  # TODO - define export

                    dpg.add_spacer()
                    dpg.add_separator()
                    dpg.add_spacer()

                    dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)

                with dpg.menu(label="Insert"):
                    dpg.add_menu_item(label="New table", callback=self.new_table)

            with dpg.menu_bar():
                dpg.add_text("          ")
                dpg.add_text("Database:")
                dpg.add_input_text(hint="Database name", tag="!database_name")

            with dpg.node_editor(tag="!node_editor", callback=self.add_link):
                pass

    def add_link(self):
        pass

    def new_database(self):
        mw_width = dpg.get_viewport_width()
        mw_height = dpg.get_viewport_height()

        def delete_all(modal):
            dpg.delete_item(modal)
            dpg.set_value("!database_name", "")
            for x in range(100, self.node_counter):
                dpg.delete_item(f"!node_editor!table_{x}")

        with dpg.window(
            label="Delete table",
            modal=True,
            width=300,
            height=150,
            pos=((mw_width - 300) / 2, (mw_height - 150) / 2),
            no_resize=True,
            no_move=True,
            no_collapse=True,
            no_title_bar=True,
        ) as modal:
            dpg.add_text("Before creating a new database")
            dpg.add_text("make sure to have this one exported")
            dpg.add_text("Are you sure to start a new database?")
            dpg.add_spacer(height=13)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=75)
                dpg.add_button(label="Yes", callback=lambda: delete_all(modal))
                dpg.add_spacer(width=50)
                dpg.add_button(label="No", callback=lambda: dpg.delete_item(modal))
                dpg.add_spacer(width=75)

    def export(self):
        pass

    def new_table(self):
        TableNode(self.node_counter)
        self.node_counter += 1
