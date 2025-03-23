import dearpygui.dearpygui as dpg


class TableField:
    def __init__(
        self,
        id,
        parent_node,
        column_name="",
        column_type="",
        editable=False,
        deletable=False,
        linked_to=None,
        user_data=None,
        attr_type=None,  # attr_type can be "input", "output" or None
        add_to_parent_attributes=True,
    ):
        self.id = id
        self.parent_node = parent_node
        self.editable = editable
        self.deletable = deletable
        self.add_to_parent_attributes = add_to_parent_attributes

        self.tag = f"{self.parent_node.tag}!attr{self.id}"
        if self.add_to_parent_attributes:
            self.parent_node.attributes.append(self.tag)
        self.linked_to = linked_to

        attr_type = (
            dpg.mvNode_Attr_Input
            if attr_type == "input"
            else (
                dpg.mvNode_Attr_Output
                if attr_type == "output"
                else dpg.mvNode_Attr_Static
            )
        )
        with dpg.node_attribute(
            tag=self.tag,
            parent=self.parent_node.tag,
            attribute_type=attr_type,
            user_data=user_data,
        ):
            with dpg.group(horizontal=True):
                dpg.add_input_text(
                    width=100,
                    hint="Type column name...",
                    tag=f"{self.tag}!column_name",
                    callback=self.update_editor,
                    enabled=self.editable,
                    default_value=column_name,
                )

                dpg.add_combo(
                    width=100,
                    items=["Integer", "Float", "String", "DateTime", "Boolean"],
                    callback=self.update_editor,
                    tag=f"{self.tag}!column_type",
                    enabled=self.editable,
                    default_value=column_type,
                )

                if self.deletable:
                    dpg.add_button(label=" - ", callback=self.delete)

                dpg.add_button(label=" + ", callback=self.parent_node.add_field)

    def delete(self):
        if self.add_to_parent_attributes:
            self.parent_node.attributes.remove(self.tag)
            self.parent_node.update_linked_tables()
        dpg.delete_item(self.tag)

    def update_editor(self):
        db_editor = dpg.get_item_user_data("!database_editor")
        db_editor.update_code()
