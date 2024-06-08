import pymel.core.uitypes as gui
import pymel.core as pm

import json
from cwmaya.lib import connections, templates_menu, connections_menu, submission_menu
from cwmaya.lib import const as k
from cwmaya.lib import window_utils


class StormWindow(gui.Window):
    def __init__(self):

        others = pm.lsUI(windows=True)
        for win in others:
            title = pm.window(win, q=True, title=True).split("|")[0].strip()
            if title == k.WINDOW_TITLE:
                pm.deleteUI(win)

        self.node = None
        self.setTitle(k.WINDOW_TITLE)
        self.setIconName(k.WINDOW_TITLE)
        self.setWidthHeight(k.WINDOW_DIMENSIONS)

        self.menuBarLayout = pm.menuBarLayout()
        self.connections_menu = connections_menu.create(self)
        self.templates_menu = templates_menu.create(self)
        self.submission_menu = submission_menu.create(self)

        self.form = pm.formLayout(nd=100)

        self.tabLayout = pm.tabLayout(changeCommand=pm.Callback(self.on_tab_changed))

        pm.setParent(self.form)
        self.submit_but = pm.button(label="Submit", command=pm.Callback(self.on_submit))

        self.composer_but = pm.button(
            label="Send to composer", command=pm.Callback(self.on_send_to_composer)
        )
        self.cancel_but = pm.button(label="Cancel", command=pm.Callback(self.on_cancel))
        self.layoutForm()

        pm.setParent(self.tabLayout)
        self.tabs = {}

        self.show()
        self.setResizeToFitChildren()

        self.load_with_first_preset()

        pm.evalDeferred(pm.Callback(connections.hydrate_coredata, self, force=False))

        

    def layoutForm(self):

        self.form.attachForm(self.tabLayout, "left", 2)
        self.form.attachForm(self.tabLayout, "right", 2)
        self.form.attachForm(self.tabLayout, "top", 2)
        self.form.attachControl(self.tabLayout, "bottom", 2, self.submit_but)

        self.form.attachNone(self.submit_but, "top")
        self.form.attachForm(self.submit_but, "right", 2)
        self.form.attachPosition(self.submit_but, "left", 2, 66)
        self.form.attachForm(self.submit_but, "bottom", 2)

        self.form.attachNone(self.composer_but, "top")
        self.form.attachControl(self.composer_but, "right", 2, self.submit_but)
        self.form.attachPosition(self.composer_but, "left", 2, 33)
        self.form.attachForm(self.composer_but, "bottom", 2)

        self.form.attachNone(self.cancel_but, "top")
        self.form.attachControl(self.cancel_but, "right", 2, self.composer_but)
        self.form.attachForm(self.cancel_but, "left", 2)
        self.form.attachForm(self.cancel_but, "bottom", 2)

    def clear_tabs(self):
        for tab in self.tabs.values():
            pm.deleteUI(tab)
        self.tabs = {}

    def on_cancel(self):
        print("on_cancel")

    def on_send_to_composer(self):
        connections.send_to_composer(self.node)

    def on_submit(self):
        connections.submit(self.node)
        # response_data = {"status_code": response.status_code, "message": json.loads(response.text)}
        # window_utils.show_data_in_window(response_data, title="Submission response")

    def on_tab_changed(self):
        print("on_tab_changed")

    def load_with_first_preset(self):
        """
        Ensure that at least one node of a registered type exists. If not, create a default node.

        Args:
            dialog: The PyMel UI dialog where the node information will be displayed.
        """
        nodes = pm.ls(type=k.NODE_TYPES)
        if not nodes:
            nodes = [pm.createNode("cwSimRenderSubmission")]
        self.load_template(nodes[0])

    def load_template(self, node):
        """
        Load a preset based on the node type and bind it to the dialog.

        Args:
            node: The node for which the preset is loaded.
            dialog: The PyMel UI dialog to update with the loaded preset.
        """
        self.node = node

        node_type = node.type()
        mod = k.NODE_TYPE_MODULES[node_type]
        mod.bind(node, self)
        pm.select(node)

    def create_template(self, node_type):
        """
        Create a new node of the specified type and load its preset into the dialog.

        Args:
            node_type: The type of node to be created.
            dialog: The PyMel UI dialog where the new node's preset will be applied.
        """
        mod = k.NODE_TYPE_MODULES[node_type]
        node = pm.createNode(node_type)
        for attr in mod.DEFAULTS:
            value = attr["value"]
            if type(value) == list:
                for i, v in enumerate(value):
                    node.attr(attr["attribute"])[i].set(v)
            else:
                node.attr(attr["attribute"]).set(value)
        self.load_template(node)
