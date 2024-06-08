import requests
import json
import os
import pymel.core as pm
from cwmaya.lib import const as k
from cwmaya.lib import window_utils
from ciocore import data as coredata
from contextlib import contextmanager


@contextmanager
def save_scene():
    """
    A context manager to save the current scene before executing the block of code.

    Yields:
        None: Yields control back to the context block after saving the scene.

    Usage Example:
    ```
    with save_scene():
        # Perform actions that require the scene to be saved
    ```
    """
    try:
        if pm.isModified():
            filters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
            entries = pm.fileDialog2(
                caption="Save File As",
                okCaption="Save As",
                fileFilter=filters,
                dialogStyle=2,
                fileMode=0,
                dir=os.path.dirname(pm.sceneName()),
            )
            if entries:
                filepath = entries[0]
                pm.saveAs(filepath)
        yield
    except Exception as err:
        pm.displayError(str(err))
    finally:
        pass

@contextmanager
def desktop_app(auth=False):
    """
    A context manager to check the health of the desktop application and optionally authenticate it.

    Yields:
        None: Yields control back to the context block if the health check succeeds (and authentication, if applicable).

    Parameters:
    - auth (bool): A flag to indicate whether authentication should be performed after the health check. Defaults to False.

    Usage Example:
    ```
    with desktop_app(auth=True):
        # Perform actions when the desktop app is healthy and authenticated
    ```

    If the health check or authentication fails, a window is displayed with the response or error message using `window_utils.show_data_in_window`.
    """
    errors = None
    try:
        response = desktop_app_health_check()
        if response.ok:
            if auth:
                auth_response = desktop_app_authenticate()
                if not auth_response.ok:
                    raise Exception(auth_response.text)
            yield
        else:
            errors = {"status_code": response.status_code, "text": response.text}
    except Exception as err:
        errors = {"error": str(err)}
    finally:
        if errors:
            window_utils.show_data_in_window(errors, title="Desktop app status")

def desktop_app_health_check():
    url = k.DESKTOP_URLS["HEALTHZ"]
    headers = {"Content-Type": "application/json"}
    return requests.get(url, headers=headers, timeout=5)

def desktop_app_authenticate():
    token = coredata.data()["account"]["token"]
    url = k.DESKTOP_URLS["AUTH"]
    headers = {"Content-Type": "application/json"}
    return requests.post(url, data=json.dumps({"token": token}), headers=headers, timeout=5)

def workflow_api_health_check():
    url = k.WORKFLOW_URLS["HEALTHZ"]
    headers = {"Content-Type": "application/json"}
    return requests.get(url, headers=headers, timeout=5)


def navigate_graph(route):
    if not route.startswith("/"):
        route = f"/{route}"

    url = k.DESKTOP_URLS["NAVIGATE"]
    data = json.dumps({"to": route})
    headers = {"Content-Type": "application/json"}
    return requests.post(url, data=data, headers=headers, timeout=5)


def send_to_composer(node):
    if not node:
        print("No node found")
        return

    with desktop_app(auth=True):
        _send_to_composer(node)
        
def _send_to_composer(node):
    url = k.DESKTOP_URLS["COMPOSER"]
    headers = {"Content-Type": "application/json"}
    out_attr = node.attr("output")
    pm.dgdirty(out_attr)
    payload = out_attr.get()
    response = requests.post(url, data=payload, headers=headers, timeout=5)
    if response.status_code == 200:
        print("Successfully sent payload to composer")
    else:
        pm.error("Error sending payload to composer:", response.text)


def submit(node):

    if not node:
        print("No node found")
        return

    with save_scene():
        _submit(node)

def _submit(node):
    headers = {"Content-Type": "application/json"}
    out_attr = node.attr("output")
    pm.dgdirty(out_attr)
    payload = out_attr.get()

    account_id = coredata.data()["account"]["account_id"]
    token = coredata.data()["account"]["token"]
    url = k.WORKFLOW_URLS["ACCOUNTS"]
    url = f"{url}/{account_id}/workflows"

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    return requests.post(url, data=payload, headers=headers, timeout=5)


def healthz(node):

    # Tauri app address
    url = "http://localhost:3031/healthz"

    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers, timeout=5)

    if response.status_code == 200:
        print(response.text)
        print("Healthz check successful")
    else:
        print("Error checking healthz:", response.text)


def hydrate_coredata(dialog, force=False):
    """
    Initializes core data with predefined services and attempts to populate the given dialog's tabs with instance types, package, and project models.

    This function initializes the core data for various services like 'maya-io', 'nuke', and 'arnold-standalone'. It then fetches the core data, forces a refresh if required, and handles any exceptions by displaying an error message.

    After successfully fetching the data, it processes the instance types, projects, and software packages to create models which are then used to update the UI elements of the provided dialog. The dialog is expected to have tabs that can be hydrated with this core data.

    Args:
        dialog: The dialog object containing tabs that need to be updated with the core data.
        force (bool): If True, forces a refresh of the core data.

    Returns:
        None: The function does not return a value but updates the dialog components in place.

    Raises:
        BaseException: Catches any exception that occurs during the core data initialization and data fetching process, displays an error message, and instructs the user on how to possibly resolve the issue.
    """
    coredata.init("maya-io", "nuke", "arnold-standalone")
    try:
        coredata.data(force=force)
    except BaseException as ex:
        pm.displayError(str(ex))
        pm.displayWarning(
            "Try again after deleting your credentials file (~/.config/conductor/credentials)"
        )
        return

    instance_types_model = coredata.data()["instance_types"].categories
    projects_model = [
        {"name": entry, "description": entry} for entry in coredata.data()["projects"]
    ]
    package_model = _get_package_model(coredata.data()["software"])

    kwargs = {
        "inst_types_model": instance_types_model,
        "package_model": package_model,
        "projects_model": projects_model,
    }
    for tab in dialog.tabs.values():
        tab.hydrate_coredata(**kwargs)


def _get_package_model(package_data):
    """
    Construct a package model from the given package data.

    This function takes package data, iterates over supported host names,
    and for each host, it creates an entry containing the host name, description,
    and a list of supported plugins with their respective versions and descriptions.

    Args:
        package_data (PackageTree): A tree-like object that is provided with ciocore::data.

    Returns:
        list: A list of dictionaries, where each dictionary represents a host and its
              associated plugins. Each host entry contains the keys 'name', 'description',
              and 'plugins', where 'plugins' is a list of plugin entries. Each plugin entry
              is a dictionary with keys 'name' and 'description'.
    """

    result = k.NONE_MODEL
    host_names = package_data.supported_host_names()
    for host_name in host_names:
        host_product, host_version, host_platform = host_name.split(" ")
        entry = {
            "name": host_name,
            "description": f"{host_product} {host_version}",
            "plugins": [],
        }
        plugin_packs = package_data.supported_plugins(host_name)
        for plugin_pack in plugin_packs:
            product = plugin_pack["plugin"]
            versions = plugin_pack["versions"]
            for version in versions:
                plugin_entry_name = f"{host_name}|{product} {version} {host_platform}"
                plugin_entry_description = (
                    f"{product} {version} for {host_product} {host_version}"
                )
                entry["plugins"].append(
                    {"name": plugin_entry_name, "description": plugin_entry_description}
                )
        result.append(entry)
    return result
