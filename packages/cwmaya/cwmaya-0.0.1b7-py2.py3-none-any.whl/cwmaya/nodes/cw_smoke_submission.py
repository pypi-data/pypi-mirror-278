# from __future__ import unicode_literals
import json

from cwmaya.nodes.cw_submission import cwSubmission
from cwstorm.dsl.task import Task
from cwstorm.serializers import default as serializer


# pylint: disable=import-error
import maya.api.OpenMaya as om

MAX_FILES_PER_UPLOAD = 4


def maya_useNewAPI():
    pass


class cwSmokeSubmission(cwSubmission):

    aWorkTask = None
    aNotifyTask = None

    id = om.MTypeId(0x880503)

    def __init__(self):
        """Initialize the class."""
        super(cwSmokeSubmission, self).__init__()

    @staticmethod
    def creator():
        return cwSmokeSubmission()

    @classmethod
    def isAbstractClass(cls):
        return False

    @classmethod
    def initialize(cls):
        """Create the static attributes."""
        om.MPxNode.inheritAttributesFrom("cwSubmission")

        cls.aWorkTask = cls.initializeTaskAttributes("wrk", "wk")
        cls.aNotifyTask = cls.initializeTaskAttributes("nfy", "nf")

    def compute(self, plug, data):
        """Compute output json from input attribs."""
        if not ((plug == self.aOutput)):
            return None

        job = self.computeJob(data)

        work_task = Task("Worker")
        work_task = self.computeOneTask(data, self.aWorkTask, work_task)

        notify_task = Task("Notify")
        notify_task = self.computeOneTask(data, self.aNotifyTask, notify_task)

        job.add(notify_task)
        notify_task.add(work_task)
        result = json.dumps(serializer.serialize(job))

        handle = data.outputValue(self.aOutput)
        handle.setString(result)

        data.setClean(plug)
        return self
