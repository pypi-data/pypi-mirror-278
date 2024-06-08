# -*- coding: utf-8 -*-

from cwmaya.lib import (
    connections_menu,
    submission_menu,
    const,
    templates_menu,
    window_utils,
    node_utils,
    layer_utils,
    about_window,
    connections,
)

from cwmaya.lib.tabs import base_tab
from cwmaya.lib.tabs import task_tab
from cwmaya.lib.tabs import job_tab
from cwmaya.lib.tabs import general_tab
from cwmaya.lib.tabs import export_tab
from cwmaya.lib.tabs import render_tab
from cwmaya.lib.tabs import quicktime_tab
from cwmaya.lib.tabs import slack_tab
from cwmaya.lib.tabs import comp_tab
from cwmaya.lib.tabs import simple_tab


from cwmaya.lib.template import (
    cw_sim_render_template,
    cw_smoke_template,
    cw_ass_template,
    template_utils,
)

from cwmaya.lib.widgets import (
    integer_field,
    checkbox,
    kv_pairs,
    commands,
    text_area,
    hidable_text_field,
    dual_option_menu,
    single_option_menu,
    software_stack_control,
    text_field,
    asset_list,
)

from cwstorm.dsl import cmd, dag_node, job, node_metaclass, node, task, upload


import importlib


importlib.reload(node_metaclass)
importlib.reload(node)
importlib.reload(dag_node)
importlib.reload(cmd)
importlib.reload(job)
importlib.reload(task)
importlib.reload(upload)

importlib.reload(const)

importlib.reload(hidable_text_field)
importlib.reload(text_field)
importlib.reload(integer_field)
importlib.reload(checkbox)

importlib.reload(text_area)
importlib.reload(kv_pairs)
importlib.reload(commands)
importlib.reload(dual_option_menu)
importlib.reload(single_option_menu)
importlib.reload(software_stack_control)
importlib.reload(asset_list)

# Tabs
importlib.reload(base_tab)
importlib.reload(task_tab)
importlib.reload(simple_tab)
importlib.reload(job_tab)
importlib.reload(general_tab)
importlib.reload(export_tab)
importlib.reload(render_tab)
importlib.reload(quicktime_tab)
importlib.reload(comp_tab)
importlib.reload(slack_tab)

# Presets
importlib.reload(template_utils)
importlib.reload(cw_ass_template)
importlib.reload(cw_smoke_template)
importlib.reload(cw_sim_render_template)


# Utils
importlib.reload(node_utils)
importlib.reload(layer_utils)
importlib.reload(window_utils)
importlib.reload(about_window)
importlib.reload(connections)


importlib.reload(connections_menu)
importlib.reload(submission_menu)
importlib.reload(templates_menu)
