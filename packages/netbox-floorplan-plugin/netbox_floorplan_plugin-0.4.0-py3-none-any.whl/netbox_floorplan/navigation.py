"""
Define the plugin menu buttons & the plugin navigation bar enteries.
"""

from netbox.plugins import PluginMenuItem


#
# Define plugin menu buttons
#
menu_buttons = (
    PluginMenuItem(
        link="plugins:netbox_floorplan:floorplan_list",
        link_text="Floorplans",
    ),
)


menu_items = menu_buttons
