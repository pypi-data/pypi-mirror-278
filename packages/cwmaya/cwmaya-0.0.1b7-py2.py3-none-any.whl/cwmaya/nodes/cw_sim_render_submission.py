# from __future__ import unicode_literals
import os
import json
import shlex

from cwmaya.nodes.cw_submission import cwSubmission


from cwstorm.dsl.upload import Upload
from cwstorm.serializers import default as serializer


# pylint: disable=import-error
import maya.api.OpenMaya as om

MAX_FILES_PER_UPLOAD = 4


def maya_useNewAPI():
    pass


class cwSimRenderSubmission(cwSubmission):
    # pass

    aSimTask = None
    aRenderTask = None
    aQuicktimeTask = None
    aFramesAttributes = None

    id = om.MTypeId(0x880504)

    def __init__(self):
        """Initialize the class."""
        super(cwSimRenderSubmission, self).__init__()

    @staticmethod
    def creator():
        return cwSimRenderSubmission()

    @classmethod
    def isAbstractClass(cls):
        return False

    @classmethod
    def initialize(cls):
        """Create the static attributes."""
        om.MPxNode.inheritAttributesFrom("cwSubmission")
        cls.aSimTask = cls.initializeTaskAttributes("sim", "sm")
        cls.aRenderTask = cls.initializeTaskAttributes("rnd", "rd")
        cls.aQuicktimeTask = cls.initializeTaskAttributes("qtm", "qt")
        cls.aFramesAttributes = cls.initializeFramesAttributes()

    def compute(self, plug, data):
        """Compute output json from input attributes."""
        if plug == self.aTokens:
            sequences = self.getSequences(data)
            chunk = sequences["main_sequence"].chunks()[0]
            static_context = self.getStaticContext(data)
            dynamic_context = self.getDynamicContext(static_context, chunk)
            result = json.dumps(dynamic_context)
            handle = data.outputValue(self.aTokens)
            handle.setString(result)
            data.setClean(plug)
            return self

        if not ((plug == self.aOutput)):
            return None

        job_values = self.getJobValues(data, self.aJob)
        sim_values = self.getTaskValues(data, self.aSimTask)
        render_values = self.getTaskValues(data, self.aRenderTask)
        quicktime_values = self.getTaskValues(data, self.aQuicktimeTask)
        sequences = self.getSequences(data)
        main_sequence = sequences["main_sequence"]
        scout_sequence = sequences["scout_sequence"] or []

        static_context = self.getStaticContext(data)

        job = self.computeJob(job_values, context=static_context)
        sim_task = self.computeTask(sim_values, context=static_context)
        quicktime_task = self.computeTask(quicktime_values, context=static_context)

        job.add(quicktime_task)

        for chunk in main_sequence.chunks():
            dynamic_context = self.getDynamicContext(static_context, chunk)
            render_task = self.computeTask(render_values, context=dynamic_context)
            if scout_sequence:
                if chunk.intersects(scout_sequence):
                    render_task.initial_state("START")
                else:
                    render_task.initial_state("HOLD")
            quicktime_task.add(render_task)
            render_task.add(sim_task)

        scenefile = static_context["scenepath"]
        up = Upload("Scene file")
        size = os.path.getsize(scenefile)
        up.push_files({"path": scenefile, "size": size})
        sim_task.add(up)

        result = json.dumps(serializer.serialize(job))

        handle = data.outputValue(self.aOutput)
        handle.setString(result)

        data.setClean(plug)

        return self
