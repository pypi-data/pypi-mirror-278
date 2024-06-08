# -*- coding: utf-8 -*-

import pymel.core as pm

from cwmaya.lib.tabs import general_tab, simple_tab, job_tab
from cwmaya.lib.template import template_utils

DEFAULTS = [
    {"attribute": "label", "value": "Job_{sequence}"},
    {"attribute": "description", "value": "Creates a fluid sim, renders it with Arnold through Maya, and finally makes a movie."},
    {"attribute": "location", "value": "Panama"},
    {"attribute": "author", "value": "jmann"},
    {"attribute": "simLabel", "value": "Sim_{sequence}"},
    {"attribute": "simPreemptible", "value": True},
    {"attribute": "simCommands", "value": ['maya - batch -export-a-simulation {seqstart} {seqend}']},
    {"attribute": "simOutputPath", "value": "/myproject/caches"},
    {"attribute": "rndLabel", "value": "Ren_{start:>04}"},
    {"attribute": "rndPreemptible", "value": True},
    {"attribute": "rndCommands", "value": ['Render -s {start} -e {end} -r \"arnold\" -proj \"/myproject\" -rd \"/myproject/renders\"']},
    {"attribute": "rndOutputPath", "value": "/myproject/renders"},
    {"attribute": "qtmLabel", "value": "Qt_{sequence}"},
    {"attribute": "qtmPreemptible", "value": True},
    {"attribute": "qtmCommands", "value": ['ffmpeg -framerate 24 -i input_%04d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p output.mp4\n']},
    {"attribute": "qtmOutputPath", "value": "/myproject/movies"},
    {"attribute": "chunkSize", "value": 1},
    {"attribute": "useCustomRange", "value": True},
    {"attribute": "customRange", "value": "1-7"},
    {"attribute": "useScoutFrames", "value": True},
    {"attribute": "scoutFrames", "value": "fml:5"}
]

def bind(node, dialog):

    dialog.clear_tabs()

    pm.setParent(dialog.tabLayout)
    dialog.tabs["general_tab"] = general_tab.GeneralTab()
    pm.setParent(dialog.tabLayout)
    dialog.tabs["sim_tab"] = simple_tab.SimpleTab()
    pm.setParent(dialog.tabLayout)
    dialog.tabs["render_tab"] = simple_tab.SimpleTab()
    pm.setParent(dialog.tabLayout)
    dialog.tabs["quicktime_tab"] = simple_tab.SimpleTab()
    pm.setParent(dialog.tabLayout)
    dialog.tabs["job_tab"] = job_tab.JobTab()
    pm.setParent(dialog.tabLayout)

    dialog.tabLayout.setTabLabel((dialog.tabs["general_tab"], "General"))
    dialog.tabLayout.setTabLabel((dialog.tabs["sim_tab"], "Sim task"))
    dialog.tabLayout.setTabLabel((dialog.tabs["render_tab"], "Render task"))
    dialog.tabLayout.setTabLabel((dialog.tabs["quicktime_tab"], "Quicktime task"))
    
    dialog.tabLayout.setTabLabel((dialog.tabs["job_tab"], "Job"))

    dialog.tabs["general_tab"].bind(node)
    dialog.tabs["sim_tab"].bind(node, "sim")
    dialog.tabs["render_tab"].bind(node, "rnd")
    dialog.tabs["quicktime_tab"].bind(node, "qtm")
    dialog.tabs["job_tab"].bind(node)
    dialog.tabLayout.setSelectTabIndex(1)

    template_utils.setDialogTitle(dialog, node)

