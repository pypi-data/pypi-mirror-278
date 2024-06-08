import pymel.core as pm
from cwmaya.lib import const as k


class TemplatesMenuGroup(object):
    """
    Build and manage the menu for creating submission template nodes.

    Attributes:
        dialog: The PyMel UI dialog that this menu group is associated with.
        menu: The main menu item under which other submenu items will be created.
        templates_menu: Submenu for selection-related actions.
        create_menu: Submenu for creation-related actions.
    """

    def __init__(self, dialog):
        """
        Initialize the TemplatesMenuGroup with a dialog and set up the initial
        menu structure.

        Args:
            dialog: The PyMel UI dialog to which this menu will be attached.
        """
        self.dialog = dialog
        pm.setParent(dialog.menuBarLayout)
        self.menu = pm.menu(
            label="Templates", tearOff=True, pmc=pm.Callback(self.post_menu_command)
        )
        pm.setParent(self.menu, menu=True)
        self.templates_menu = pm.menuItem(label="Load", subMenu=True)
        pm.setParent(self.menu, menu=True)

        self.create_menu = pm.menuItem(label="Create", subMenu=True)
        pm.setParent(self.menu, menu=True)

        pm.menuItem(divider=True)
        self.select_menu = pm.menuItem(
            label="Select current", command=pm.Callback(select_current, self.dialog)
        )
        pm.menuItem(divider=True)

    def post_menu_command(self):
        """
        Dynamically build the Select and Create submenus just before the menu is opened,
        populating them based on existing nodes of registered types.
        """
        pm.setParent(self.templates_menu, menu=True)
        pm.menu(self.templates_menu, edit=True, deleteAllItems=True)
        for j in pm.ls(type=k.NODE_TYPES):
            pm.menuItem(
                label=f"Load {str(j)}",
                command=pm.Callback(self.dialog.load_template, j),
            )

        pm.setParent(self.create_menu, menu=True)
        pm.menu(self.create_menu, edit=True, deleteAllItems=True)

        for j in k.NODE_TYPES:
            pm.menuItem(
                label=f"Create {str(j)}",
                command=pm.Callback(self.dialog.create_template, j),
            )
        pm.setParent(self.menu, menu=True)


def create(dialog):
    """
    Factory function to create a new instance of TemplatesMenuGroup attached to the given dialog.

    Args:
        dialog: The PyMel UI dialog to which the menu group will be attached.
    """
    return TemplatesMenuGroup(dialog)


def select_current(dialog):
    pm.select(dialog.node)
