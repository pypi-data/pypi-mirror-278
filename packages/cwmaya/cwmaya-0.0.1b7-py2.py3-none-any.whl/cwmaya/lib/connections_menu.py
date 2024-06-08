import pymel.core as pm
from cwmaya.lib import connections
from cwmaya.lib import const as k
from cwmaya.lib import window_utils


class ConnectionsMenuGroup(object):

    def __init__(self, dialog):
        """
        Initialize the TemplatesMenuGroup with a dialog and set up the initial
        menu structure.

        Args:
            dialog: The PyMel UI dialog to which this menu will be attached.
        """
        self.dialog = dialog
        pm.setParent(dialog.menuBarLayout)
        self.menu = pm.menu(label="Connections", tearOff=True)

        pm.menuItem(label="Connect to Conductor", command=pm.Callback(self.on_connect))

        self.create_desktop_app_menu()
        self.create_workflow_api_menu()

    def on_connect(self):
        print("Connecting")
        connections.hydrate_coredata(self.dialog, force=True)

    def create_desktop_app_menu(self):
        pm.setParent(self.menu, menu=True)
        self.desktop_app_menu = pm.menuItem(label="Desktop app", subMenu=True)
        pm.menuItem(
            label="Health check", command=pm.Callback(on_desktop_app_health_check)
        )
        pm.menuItem(label="Navigate", subMenu=True)
        for route in k.DESKTOP_APP_ROUTES:
            pm.menuItem(
                label=route, command=pm.Callback(on_desktop_app_navigate, route)
            )

    def create_workflow_api_menu(self):
        pm.setParent(self.menu, menu=True)
        self.workflow_api_menu = pm.menuItem(label="Workflow API", subMenu=True)
        pm.menuItem(
            label="Health check", command=pm.Callback(on_workflow_api_health_check)
        )


def create(dialog):
    return ConnectionsMenuGroup(dialog)


def on_desktop_app_health_check():
    try:
        response = connections.desktop_app_health_check()
        data = {"status_code": response.status_code, "text": response.text}
    except Exception as err:
        data = {"error": str(err)}
    window_utils.show_data_in_window(data, title="Desktop app health check")

def on_workflow_api_health_check():
    try:
        response = connections.workflow_api_health_check()
        data = {"status_code": response.status_code, "text": response.text}
    except Exception as err:
        data = {"error": str(err)}
    window_utils.show_data_in_window(data, title="Workflow API health check")


def on_desktop_app_navigate(route):
    response = connections.navigate_graph(route)
    if response.status_code == 200:
        print(f"Successfully navigated to {route}")
    else:
        pm.error(f"Error navigating to {route}: {response.text}")
