import pymel.core as pm
import json
from cwmaya.lib import const as k
from cwmaya.lib import window_utils
from ciocore import data as coredata


class SubmissionMenuGroup(object):

    def __init__(self, dialog):
        """
        Initialize the TemplatesMenuGroup with a dialog and set up the initial
        menu structure.

        Args:
            dialog: The PyMel UI dialog to which this menu will be attached.
        """
        self.dialog = dialog
        pm.setParent(dialog.menuBarLayout)
        self.menu = pm.menu(label="Submissions", tearOff=True)

        pm.menuItem(
            label="Show submission", command=pm.Callback(self.on_show_submission)
        )
        pm.menuItem(
            label="Export submission", command=pm.Callback(self.on_export_submission)
        )
        pm.menuItem(label="Show tokens", command=pm.Callback(self.on_show_tokens))

    def on_show_submission(self):

        node = self.dialog.node
        if not node:
            print("No node found")
            return

        out_attr = node.attr("output")
        pm.dgdirty(out_attr)
        payload = out_attr.get()

        payload = json.loads(payload)

        account_id = coredata.data()["account"]["account_id"]
        token = coredata.data()["account"]["token"]

        url = k.WORKFLOW_URLS["ACCOUNTS"]
        url = f"{url}/{account_id}/workflows"
        headers = {"Content-Type": "application/json"}

        data = {
            "request_data": {
                "headers": headers,
                "url": url,
                "token": token,
                "node": node.name(),
            },
            "payload": payload,
        }
        window_utils.show_data_in_window(data, title="Submission preview")


    def on_export_submission(self):

        node = self.dialog.node
        if not node:
            print("No node found")
            return

        out_attr = node.attr("output")
        pm.dgdirty(out_attr)
        payload = out_attr.get()
        
        
        filters = "JSON Files (*.json)"
        ws = pm.Workspace()
        datadir = ws.expandName(ws.fileRules.get('diskCache'))
        entries = pm.fileDialog2(
            caption="Save File As",
            okCaption="Export",
            fileFilter=filters,
            dialogStyle=2,
            fileMode=0,
            dir=datadir,
        )

        if not entries:
            print("No file selected")
            return
        
        with open(entries[0], "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Exported submission to {entries[0]}")




    def on_show_tokens(self):
        node = self.dialog.node
        if not node:
            print("No node found")
            return

        out_attr = node.attr("tokens")
        pm.dgdirty(out_attr)
        payload = out_attr.get()
        data = json.loads(payload)
        window_utils.show_data_in_window(data, title="Tokens")


def create(dialog):
    return SubmissionMenuGroup(dialog)
