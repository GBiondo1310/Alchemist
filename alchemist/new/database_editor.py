import json

import dearpygui.dearpygui as dpg
from .widgets.node import TableNode
from .widgets.field import TableField
from ..utils import center_to_viewport, center_to_widget
from ..core.codes import IMPORTS
from ..core.loader import Loader, Table


class DatabaseEditor:
    node_counter = 100
    code_shown = False
    nodes = []

    def __init__(self):

        with dpg.window(
            label="Database editor",
            tag="!database_editor",
            user_data=self,
        ):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="New database", callback=self.new_database)
                    dpg.add_menu_item(
                        label="Export to python file", callback=self.export
                    )
                    dpg.add_menu_item(
                        label="Import database", callback=self.import_database
                    )
                    dpg.add_spacer()
                    dpg.add_separator()
                    dpg.add_spacer()

                    dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)

                with dpg.menu(label="Insert"):
                    dpg.add_menu_item(label="New table", callback=self.new_table)

                dpg.add_menu_item(
                    label="Show code",
                    callback=self.toggle_code,
                    tag="!show_code_button",
                )

            with dpg.menu_bar():
                dpg.add_text("          ")
                dpg.add_text("Database:")
                dpg.add_input_text(
                    hint="Database name",
                    tag="!database_name",
                    callback=self.update_code,
                )

            with dpg.group(horizontal=True):

                with dpg.node_editor(
                    tag="!node_editor",
                    callback=self.add_link,
                    delink_callback=self.delete_link,
                ):
                    pass

                with dpg.window(
                    label="Generated code",
                    width=500,
                    tag="!generated_code",
                    no_background=True,
                    no_title_bar=True,
                ):
                    t = dpg.add_input_text(
                        multiline=True, width=-1, height=-1, tag="!generated_code!code"
                    )
                dpg.configure_item("!generated_code", show=False)

            self.update_code()

    def add_link(self, sender, items):

        parent_table_tag = dpg.get_item_alias(dpg.get_item_parent(items[0]))
        child_table_tag = dpg.get_item_alias(dpg.get_item_parent(items[1]))
        print(parent_table_tag)
        print(child_table_tag)

        parent_toplevel: TableNode = dpg.get_item_user_data(parent_table_tag)
        child_toplevel: TableNode = dpg.get_item_user_data(child_table_tag)

        parent_reopen = False
        child_reopen = False

        if parent_toplevel.code_open:
            parent_toplevel.toggle_code()
            parent_reopen = True
        if child_toplevel.code_open:
            child_toplevel.toggle_code()
            child_reopen = True

        c1 = TableField(
            child_toplevel.cur_id,
            child_toplevel,
            dpg.get_value(parent_toplevel.tag + "!__tablename__") + "_id",
            "Relationship FK",
            user_data=dpg.get_value(parent_toplevel.tag + "!__tablename__"),
            attr_type="input",
        ).tag

        child_toplevel.cur_id += 1

        c2 = TableField(
            child_toplevel.cur_id,
            child_toplevel,
            dpg.get_value(parent_toplevel.tag + "!__tablename__"),
            "Relationship Child",
            user_data=dpg.get_value(parent_toplevel.tag + "!class_name"),
            attr_type=None,
        ).tag

        child_toplevel.cur_id += 1

        p1 = TableField(
            parent_toplevel.cur_id,
            parent_toplevel,
            dpg.get_value(child_toplevel.tag + "!__tablename__") + "s",
            "Relationship Parent",
            user_data=dpg.get_value(child_toplevel.tag + "!class_name"),
            attr_type="output",
        ).tag

        parent_toplevel.cur_id += 1

        dpg.add_node_link(p1, c1, parent=sender, tag=f"{c1}+{c2}+{p1}")

        if parent_reopen:
            parent_toplevel.toggle_code()
        if child_reopen:
            child_toplevel.toggle_code()

        parent_toplevel.links.append(f"{c1}+{c2}+{p1}")
        child_toplevel.links.append(f"{c1}+{c2}+{p1}")
        self.update_code()

    def new_database(self):
        mw_width = dpg.get_viewport_width()
        mw_height = dpg.get_viewport_height()

        def delete_all(modal):
            dpg.delete_item(modal)
            dpg.set_value("!database_name", "")
            for x in range(100, self.node_counter):
                dpg.delete_item(f"!node_editor!table_{x}")

            self.nodes = []

            self.update_code()

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

    def delete_link(self, sender, app_data):
        link_tag = dpg.get_item_alias(app_data)
        for connected_item in link_tag.split("+"):
            parent = dpg.get_item_user_data(
                dpg.get_item_alias(dpg.get_item_parent(connected_item))
            )
            parent.attributes.remove(connected_item)
            if link_tag in parent.links:
                parent.links.remove(link_tag)
            dpg.delete_item(connected_item)
            parent.update_linked_tables()
        dpg.delete_item(link_tag)
        self.update_code()

    def export(self):
        def save_to_file(sender, app_data):
            filename = app_data.get("file_path_name")
            code = dpg.get_value("!generated_code!code")
            with open(filename, mode="w") as code_file:
                code_file.write(code)

        with dpg.file_dialog(
            directory_selector=False,
            modal=True,
            callback=save_to_file,
            width=700,
            height=350,
            default_filename="export",
        ):
            dpg.add_file_extension(".py")

    def generate_code(self):
        code = IMPORTS.replace("%database_name%", dpg.get_value("!database_name"))
        node: TableNode
        for node in self.nodes:
            user_data = dpg.get_item_user_data(node)
            new_code = user_data.update_linked_tables()
            code = code + new_code

        return code

    def update_code(self):
        dpg.set_value("!generated_code!code", self.generate_code())

    def toggle_code(self):
        self.code_shown = not self.code_shown
        dpg.configure_item("!generated_code", show=self.code_shown)
        label_text = "Show code" if not self.code_shown else "Hide code"
        dpg.set_item_label("!show_code_button", label_text)

    def new_table(self):
        TableNode(self.node_counter)
        self.node_counter += 1
        db_editor = dpg.get_item_user_data("!database_editor")
        db_editor.update_code()

    def set_code_pos(self):

        main_window_width = dpg.get_item_width("!database_editor")
        main_window_height = dpg.get_item_height("!database_editor")

        dpg.set_item_height("!generated_code", main_window_height - 20)
        dpg.set_item_pos("!generated_code", (main_window_width - 500, 20))

    def import_database(self):
        with open("temp.json", mode="r") as temp_json:
            temp = json.load(temp_json)

        databases = list(temp.keys())

        def load_database(database, modal_id):
            loader = Loader(temp, database)
            self.load_imported_database(loader)
            dpg.delete_item(modal_id)

        with dpg.window(
            label="Pick a database", modal=True, height=120, width=300
        ) as database_dialog:
            center_to_viewport(database_dialog)

            combo = dpg.add_combo(items=databases, default_value=databases[0])

            dpg.add_spacer(height=30)

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Load",
                    callback=lambda: load_database(
                        dpg.get_value(combo), database_dialog
                    ),
                )

                dpg.add_button(
                    label="Cancel", callback=lambda: dpg.delete_item(database_dialog)
                )

    def load_imported_database(self, loader: Loader):
        dpg.set_value("!database_name", "")
        for x in range(100, self.node_counter):
            dpg.delete_item(f"!node_editor!table_{x}")

        self.nodes = []

        self.update_code()

        tables = {}

        table: Table
        for table in loader.tables:
            t = TableNode(self.node_counter)
            self.node_counter += 1
            dpg.set_value(t.tag + "!class_name", table.table)
            dpg.set_item_label(t.tag, table.table)
            dpg.set_value(t.tag + "!__tablename__", table.tablename)

            for field_name, field_type in table.columns.items():
                TableField(
                    t.cur_id,
                    t,
                    field_name,
                    field_type,
                    add_to_parent_attributes=True,
                )
                t.cur_id += 1

            tables.update({table.table: t})

        for parent, child in loader.links.items():
            parent = tables.get(parent)
            child = tables.get(child)

            parent = dpg.get_item_children(parent.tag).get(1)[0]
            child = dpg.get_item_children(child.tag).get(1)[0]

            self.add_link(
                "!node_editor",
                [parent, child],
            )

        self.update_code()

    def save(self):
        database_name = dpg.get_value("!database_name")
        # TODO - Continue with save
