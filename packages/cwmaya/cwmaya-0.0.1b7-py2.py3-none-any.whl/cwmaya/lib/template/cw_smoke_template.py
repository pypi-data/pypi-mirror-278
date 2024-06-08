# -*- coding: utf-8 -*-

import pymel.core as pm

from cwmaya.lib.tabs import simple_tab, job_tab


from cwmaya.lib.template import template_utils


def bind(node, dialog):

    dialog.clear_tabs()

    pm.setParent(dialog.tabLayout)
    dialog.tabs["work_tab"] = simple_tab.SimpleTab()
    pm.setParent(dialog.tabLayout)
    dialog.tabs["notify_tab"] = simple_tab.SimpleTab()
    pm.setParent(dialog.tabLayout)
    dialog.tabs["job_tab"] = job_tab.JobTab()
    pm.setParent(dialog.tabLayout)

    dialog.tabLayout.setTabLabel((dialog.tabs["work_tab"], "Work task"))
    dialog.tabLayout.setTabLabel((dialog.tabs["notify_tab"], "Notify task"))
    dialog.tabLayout.setTabLabel((dialog.tabs["job_tab"], "Job"))

    dialog.tabs["work_tab"].bind(node, "wrk")
    dialog.tabs["notify_tab"].bind(node, "nfy")
    dialog.tabs["job_tab"].bind(node)
    dialog.tabLayout.setSelectTabIndex(1)

    template_utils.setDialogTitle(dialog, node)
