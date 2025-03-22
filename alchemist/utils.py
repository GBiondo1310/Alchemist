import dearpygui.dearpygui as dpg


def center_to_viewport(widget):
    mw_width = dpg.get_viewport_width()
    mw_height = dpg.get_viewport_height()

    widget_width = dpg.get_item_width(widget)
    widget_height = dpg.get_item_height(widget)
    pos = ((mw_width - widget_width) / 2, (mw_height - widget_height) / 2)
    dpg.set_item_pos(widget, pos)

    return pos


def center_to_widget(widget, parent):
    parent_width = dpg.get_item_width(parent)
    parent_height = dpg.get_item_height(parent)

    widget_width = dpg.get_item_width(widget)
    widget_height = dpg.get_item_height(widget)

    pos = ((parent_width - widget_width) / 2, (parent_height - widget_height) / 2)
    dpg.set_item_pos(widget, pos)
    return pos
