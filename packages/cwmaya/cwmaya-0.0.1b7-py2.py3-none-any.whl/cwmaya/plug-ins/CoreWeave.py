import sys
import os

import maya.api.OpenMaya as om

CIODIR = os.environ.get("CWMAYA_CIODIR")
sys.path.append(CIODIR)

from cwmaya.nodes.cw_submission import cwSubmission
from cwmaya.nodes.cw_smoke_submission import cwSmokeSubmission
from cwmaya.nodes.cw_sim_render_submission import cwSimRenderSubmission
from cwmaya.lib import coreweave_menu


def maya_useNewAPI():
    pass


def initializePlugin(obj):

    plugin = om.MFnPlugin(obj, "CoreWeave", "0.0.1-beta.7", "Any")

    try:
        plugin.registerNode(
            "cwSubmission",
            cwSubmission.id,
            cwSubmission.creator,
            cwSubmission.initialize,
            om.MPxNode.kDependNode,
        )


        plugin.registerNode(
            "cwSmokeSubmission",
            cwSmokeSubmission.id,
            cwSmokeSubmission.creator,
            cwSmokeSubmission.initialize,
            om.MPxNode.kDependNode,
        )
        
        plugin.registerNode(
            "cwSimRenderSubmission",
            cwSimRenderSubmission.id,
            cwSimRenderSubmission.creator,
            cwSimRenderSubmission.initialize,
            om.MPxNode.kDependNode,
        )

    except:
        sys.stderr.write("Failed to register submission nodes\n")
        raise

    coreweave_menu.load()


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        plugin.deregisterNode(cwSimRenderSubmission.id)
        plugin.deregisterNode(cwSmokeSubmission.id)
        plugin.deregisterNode(cwSubmission.id)
    except:
        sys.stderr.write("Failed to deregister submission nodes\n")
        raise

    coreweave_menu.unload()
