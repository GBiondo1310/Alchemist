from __future__ import annotations

import dearpygui.dearpygui as dpg

from .field import TableField
from ...core.db_class import DBClass
from ...utils import center_to_viewport


class TableNode:
    def __init__(self, id):
        self.attributes = []
        self.cur_id = 0
        self.code_open = False
        self.tag = f"!node_editor!table_{id}"

        with dpg.node(
            label="New table", parent="!node_editor", tag=self.tag, user_data=self
        ):
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Show code", callback=self.toggle_code)
                    dpg.add_spacer(width=50)
                    dpg.add_button(label="Delete table", callback=self.delete)

            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output):
                with dpg.group(horizontal=True):
                    dpg.add_text("Class name: ")
                    dpg.add_input_text(
                        width=100,
                        hint="Type class name...",
                        tag=f"{self.tag}!class_name",
                        callback=self.set_class_name,
                    )

            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input):
                with dpg.group(horizontal=True):
                    dpg.add_text("Table name: ")
                    dpg.add_input_text(
                        width=100,
                        hint="Type table name...",
                        tag=f"{self.tag}!__tablename__",
                        callback=self.set_tablename,
                        user_data=self,
                    )

            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                with dpg.group(horizontal=True):
                    dpg.add_text("Column")
                    dpg.add_spacer(width=50)
                    dpg.add_text("Type")

            TableField(
                self.cur_id,
                self,
                "id",
                "Integer",
                add_to_parent_attributes=False,
            )

            self.cur_id += 1

    def set_class_name(self, sender, app_data, user_data):
        dpg.set_item_label(f"{self.tag}", app_data)
        self.update()

    def set_tablename(self, sender, app_data, user_data):
        self.update()

    def add_field(self):
        if self.code_open:
            self.toggle_code()
        TableField(self.cur_id, self, editable=True, deletable=True)
        self.cur_id += 1
        if not self.code_open:
            self.toggle_code()

    def toggle_code(self):
        dpg.delete_item(self.tag + "!code_attr")
        dpg.delete_item(self.tag + "!code")
        if not self.code_open:
            with dpg.node_attribute(
                parent=self.tag,
                tag=self.tag + "!code_attr",
                attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_text("", tag=self.tag + "!code")

        self.code_open = not self.code_open
        self.update()

    def update(self):
        if self.code_open:
            db_class = DBClass()

            db_class.classname = dpg.get_value(f"{self.tag}!class_name")
            db_class.tablename = dpg.get_value(f"{self.tag}!__tablename__")

            for attribute in self.attributes:

                field_name = dpg.get_value(f"{attribute}!column_name")
                field_type = dpg.get_value(f"{attribute}!column_type")
                field_pk = dpg.get_value(f"{attribute}!column_pk")
                if field_type == "Relationship FK":
                    db_class.add_relationship_field_child_fk(
                        attribute, field_name, dpg.get_item_user_data(attribute)
                    )
                elif field_type == "Relationship Child":
                    db_class.add_relationship_field_child(
                        attribute,
                        field_name,
                        dpg.get_item_user_data(attribute),
                        dpg.get_value(f"{self.tag}!__tablename__"),
                    )
                elif field_type == "Relationship Parent":
                    db_class.add_relationship_field_parent(
                        attribute,
                        field_name,
                        dpg.get_item_user_data(attribute),
                        dpg.get_value(f"{self.tag}!__tablename__"),
                    )
                else:
                    db_class.add_field(attribute, field_name, field_type, field_pk)

            code = db_class.generate_code()

            dpg.set_value(self.tag + "!code", db_class.generate_code())
            return code

    def delete(self):

        def delete_node(self, modal_window):
            dpg.delete_item(modal_window)
            dpg.delete_item(self.tag)
            del self

        with dpg.window(
            label="Delete table",
            modal=True,
            width=300,
            height=50,
            no_resize=True,
            no_move=True,
            no_collapse=True,
            no_title_bar=True,
        ) as modal:
            dpg.add_text("Do you really want to delete this table?")
            dpg.add_spacer(height=13)
            with dpg.group(horizontal=True):
                dpg.add_spacer(width=75)
                dpg.add_button(label="Yes", callback=lambda: delete_node(self, modal))
                dpg.add_spacer(width=50)
                dpg.add_button(label="No", callback=lambda: dpg.delete_item(modal))
                dpg.add_spacer(width=75)
