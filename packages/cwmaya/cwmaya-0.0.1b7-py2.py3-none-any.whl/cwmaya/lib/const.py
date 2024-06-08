import os

LABEL_WIDTH = 145
TRASH_COLUMN_WIDTH = 36
FORM_SPACING_X = 4
FORM_SPACING_Y = 2
WINDOW_DIMENSIONS = [600, 800]
WINDOW_TITLE = "Storm Tools"


CURRENT_LAYER = 0
LAYERS_ONE_JOB = 1
JOB_PER_LAYER = 2


DEFAULT_TEMPLATE = 'Render -r <Renderer> -s <start> -e <end> -b <step> -rl "<RenderLayer>" -rd "<OutputPath>"  -proj "<WorkspacePath>" "<SceneFile>"'
DEFAULT_DESTINATION_DIR_TEMPLATE = "<ImagesPath>"
OTHER_TEMPLATES = [
    'Render -r <Renderer>  -ai:lve 3 -s <start> -e <end> -b <step> -rl "<RenderLayer>" -rd "<OutputPath>"  -proj "<WorkspacePath>" "<SceneFile>"'
]


DEFAULT_TITLE = "Maya:<Renderer> - <Scene> <RenderLayer>"
DEFAULT_AUTOSAVE_TEMPLATE = "cio_<Scene>"

DEFAULT_INSTANCE_TYPE = "n1-standard-4"
MAX_TASKS = int(os.environ.get("CONDUCTOR_MAX_TASKS", 1000))
LIST_HEADER_BG = (0.35, 0.35, 0.35)

UNCONNECTED_MODEL = [{"name": "none", "description": "Not connected"}]

UNCONNECTED_DUAL_MODEL = [
    {"label": "None", "content": [{"name": "none", "description": "Not connected"}]}
]

NONE_MODEL = [{"name": "none", "description": "None"}]

DESKTOP_API = "http://localhost:3031"
DESKTOP_URLS = {
    "HEALTHZ": f"{DESKTOP_API}/healthz",
    "COMPOSER": f"{DESKTOP_API}/graph",
    "NAVIGATE": f"{DESKTOP_API}/navigate",
    "AUTH": f"{DESKTOP_API}/jwt",
}

WORKFLOW_API = "http://localhost:8000/workflow"
WORKFLOW_URLS = {
    "HEALTHZ": f"{WORKFLOW_API}/healthz",
    "ACCOUNTS": f"{WORKFLOW_API}/v1/accounts",
}


from cwmaya.lib.template import (
    cw_ass_template,
    cw_smoke_template,
    cw_sim_render_template,
)

NODE_TYPE_MODULES = {
    "cwSmokeSubmission": cw_smoke_template,
    "cwSimRenderSubmission": cw_sim_render_template,
}

NODE_TYPES = NODE_TYPE_MODULES.keys()

DESKTOP_APP_ROUTES = [
    "/",
    "/user_management",
    "/storage_center",
    "/graph_composer",
    "/storm_monitor",
    "/job_center",
    "/projects",
    "/plugins",
    "/my_account",
    "/billing_center",
]


#################### EXAMPLE STRUCTURES #####################
#
# INSTANCE_TYPES =[
#    {
#       "label": "CPU",
#       "content": [
#          {
#             "description": "2 core 13GB Mem",
#             "name": "n1-highmem-2",
#          },
#          {
#             "description": "2 core 7.5GB Mem",
#             "name": "n1-standard-2",
#          }
#       ],
#       "order": 1
#    },
#    {
#       "label": "GPU",
#       "content": [
#          {
#             "description": "2 core 7.5GB Mem (1 V100 GPUs 16GB Mem)",
#             "name": "n1-standard-2-v1-1",
#          },
#          {
#             "description": "2 core 7.5GB Mem (2 V100 GPUs 16GB Mem)",
#             "name": "n1-standard-2-v1-2",
#          }
#       ],
#       "order": 2
#    }
# ]
#
# SOFTWARE = [
#     {"name": "maya-2019", "description": "Maya 2019 X", "plugins": [
#         {"name": "vray 1.2.3", "description": "Vray 1.2.3 X"},
#         {"name": "vray 1.2.4", "description": "Vray 1.2.4 X"},
#         {"name": "redshift 1.3.4", "description": "Redshift 1.3.4 X"},
#         {"name": "arnold-maya 1.3.5", "description": "Arnold-Maya 1.3.5 X"},
#         {"name": "arnold-maya 1.3.6", "description": "Arnold-Maya 1.3.6 X"}]},
#     {"name": "maya-2020", "description": "Maya 2020 X", "plugins": [
#         {"name": "vray 1.2.3", "description": "Vray 1.2.3 X"}]},
#     {"name": "maya-2021", "description": "Maya 2021 X", "plugins": [
#         {"name": "vray 2.2.3", "description": "Vray 2.2.3 X"},
#         {"name": "vray 2.2.4", "description": "Vray 2.2.4 X"},
#         {"name": "redshift 2.3.4", "description": "Redshift 2.3.4 X"},
#         {"name": "arnold-maya 2.3.5", "description": "Arnold-Maya 2.3.5 X"},
#         {"name": "arnold-maya 2.3.6", "description": "Arnold-Maya 2.3.6 X"}]},
#     {"name": "kick-6.4.4.2", "description": "Kick 6.4.4.2 X", "plugins": []},
#     {"name": "kick-kick-6.5.0.0", "description": "Kick 6.5.0.0 X", "plugins": []},
# ]
#
# PROJECTS = [
#     {"name": "corelli", "description": "Captain Corelli's Mandolin"},
#     {"name": "troy", "description": "Troy"},
#     {"name": "borrowers", "description": "The Borrowers"},
#     {"name": "montecristo", "description": "The Count of Monte Cristo"},
#     {"name": "hours", "description": "The Hours"},
#     {"name": "potter2", "description": "Harry Potter and the Chamber of Secrets"},
#     {"name": "fishtank", "description": "Fish Tank"},
#     {"name": "pitchblack", "description": "Pitch Black"},
# ]
