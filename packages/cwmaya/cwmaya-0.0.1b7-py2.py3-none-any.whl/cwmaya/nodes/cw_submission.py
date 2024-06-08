import os
import shlex
import re
import socket
from cwstorm.dsl.upload import Upload

import maya.api.OpenMaya as om

from cwstorm.dsl.job import Job
from cwstorm.dsl.task import Task
from cwstorm.dsl.cmd import Cmd

from ciocore import data as coredata
from cioseq.sequence import Sequence
import maya.cmds as cmds


def maya_useNewAPI():
    pass


class cwSubmission(om.MPxNode):

    aJob = None

    aOutput = None
    aTokens = None

    MAX_FILES_PER_UPLOAD = 4

    id = om.MTypeId(0x880501)

    @staticmethod
    def creator():
        return cwSubmission()

    @classmethod
    def isAbstractClass(cls):
        return True

    @classmethod
    def initialize(cls):

        cls.aOutput = cls.makeStringAttribute(
            "output",
            "out",
            hidden=True,
            writable=False,
            keyable=False,
            storable=False,
            readable=True,
        )
        om.MPxNode.addAttribute(cls.aOutput)

        cls.aTokens = cls.makeStringAttribute(
            "tokens",
            "tok",
            hidden=True,
            writable=False,
            keyable=False,
            storable=False,
            readable=True,
        )
        om.MPxNode.addAttribute(cls.aTokens)

        cls.aJob = cls.initializeJobAttributes()

    @classmethod
    def initializeJobAttributes(cls):
        result = {}

        result["label"] = cls.makeStringAttribute("label", "lbl")
        result["description"] = cls.makeStringAttribute("description", "desc")
        result["projectName"] = cls.makeStringAttribute("projectName", "prn")
        result["currentTime"] = cls.makeTimeAttribute("currentTime", "ct")
        result["locationTag"] = cls.makeStringAttribute("location", "loc")
        result["author"] = cls.makeStringAttribute("author", "ath")

        metadata = cls.makeKvPairsAttribute("metadata", "mtd")
        result["metadata"] = metadata["compound"]
        result["metadataKey"] = metadata["key"]
        result["metadataValue"] = metadata["value"]

        om.MPxNode.addAttribute(result["label"])
        om.MPxNode.addAttribute(result["description"])
        om.MPxNode.addAttribute(result["projectName"])
        om.MPxNode.addAttribute(result["currentTime"])
        om.MPxNode.addAttribute(result["locationTag"])
        om.MPxNode.addAttribute(result["author"])
        om.MPxNode.addAttribute(result["metadata"])

        om.MPxNode.attributeAffects(result["label"], cls.aOutput)
        om.MPxNode.attributeAffects(result["description"], cls.aOutput)
        om.MPxNode.attributeAffects(result["projectName"], cls.aOutput)
        om.MPxNode.attributeAffects(result["metadata"], cls.aOutput)
        om.MPxNode.attributeAffects(result["currentTime"], cls.aOutput)
        om.MPxNode.attributeAffects(result["locationTag"], cls.aOutput)
        om.MPxNode.attributeAffects(result["author"], cls.aOutput)

        return result

    @classmethod
    def initializeTaskAttributes(cls, longPrefix, shortPrefix):
        """Create the static attributes for the export column."""
        result = {}

        result["label"] = cls.makeStringAttribute(
            f"{longPrefix}Label", f"{shortPrefix}lb"
        )

        result["instanceType"] = cls.makeStringAttribute(
            f"{longPrefix}InstanceType", f"{shortPrefix}it"
        )

        result["preemptible"] = cls.makeBoolAttribute(
            f"{longPrefix}Preemptible", f"{shortPrefix}pt"
        )

        result["software"] = cls.makeStringAttribute(
            f"{longPrefix}Software", f"{shortPrefix}sw", array=True
        )

        result["commands"] = cls.makeStringAttribute(
            f"{longPrefix}Commands", f"{shortPrefix}cm", array=True
        )

        environment = cls.makeKvPairsAttribute(
            f"{longPrefix}Environment", f"{shortPrefix}nv"
        )

        result["environment"] = environment["compound"]
        result["environmentKey"] = environment["key"]
        result["environmentValue"] = environment["value"]
        result["extraAssets"] = cls.makeStringAttribute(
            f"{longPrefix}ExtraAssets", f"{shortPrefix}ea", array=True
        )

        result["output_path"] = cls.makeStringAttribute(
            f"{longPrefix}OutputPath", f"{shortPrefix}op"
        )

        om.MPxNode.addAttribute(result["label"])
        om.MPxNode.addAttribute(result["instanceType"])
        om.MPxNode.addAttribute(result["preemptible"])
        om.MPxNode.addAttribute(result["software"])
        om.MPxNode.addAttribute(result["commands"])
        om.MPxNode.addAttribute(result["environment"])
        om.MPxNode.addAttribute(result["extraAssets"])
        om.MPxNode.addAttribute(result["output_path"])

        om.MPxNode.attributeAffects(result["label"], cls.aOutput)
        om.MPxNode.attributeAffects(result["instanceType"], cls.aOutput)
        om.MPxNode.attributeAffects(result["preemptible"], cls.aOutput)
        om.MPxNode.attributeAffects(result["software"], cls.aOutput)
        om.MPxNode.attributeAffects(result["commands"], cls.aOutput)
        om.MPxNode.attributeAffects(result["environment"], cls.aOutput)
        om.MPxNode.attributeAffects(result["extraAssets"], cls.aOutput)
        om.MPxNode.attributeAffects(result["output_path"], cls.aOutput)
        return result

    @classmethod
    def initializeFramesAttributes(cls):

        result = {}

        result["chunkSize"] = cls.makeIntAttribute("chunkSize", "csz", default=1, min=0)
        result["useCustomRange"] = cls.makeBoolAttribute("useCustomRange", "ucr")
        result["customRange"] = cls.makeStringAttribute("customRange", "crn")
        result["useScoutFrames"] = cls.makeBoolAttribute("useScoutFrames", "usf")
        result["scoutFrames"] = cls.makeStringAttribute("scoutFrames", "scf")
        result["startFrame"] = cls.makeTimeAttribute("startFrame", "stf")
        result["endFrame"] = cls.makeTimeAttribute("endFrame", "enf")
        result["byFrame"] = cls.makeIntAttribute("byFrame", "byf", default=1, min=1)

        om.MPxNode.addAttribute(result["chunkSize"])
        om.MPxNode.addAttribute(result["useCustomRange"])
        om.MPxNode.addAttribute(result["customRange"])
        om.MPxNode.addAttribute(result["useScoutFrames"])
        om.MPxNode.addAttribute(result["scoutFrames"])
        om.MPxNode.addAttribute(result["startFrame"])
        om.MPxNode.addAttribute(result["endFrame"])
        om.MPxNode.addAttribute(result["byFrame"])

        om.MPxNode.attributeAffects(result["chunkSize"], cls.aOutput)
        om.MPxNode.attributeAffects(result["useCustomRange"], cls.aOutput)
        om.MPxNode.attributeAffects(result["customRange"], cls.aOutput)
        om.MPxNode.attributeAffects(result["useScoutFrames"], cls.aOutput)
        om.MPxNode.attributeAffects(result["scoutFrames"], cls.aOutput)
        om.MPxNode.attributeAffects(result["startFrame"], cls.aOutput)
        om.MPxNode.attributeAffects(result["endFrame"], cls.aOutput)
        om.MPxNode.attributeAffects(result["byFrame"], cls.aOutput)

        om.MPxNode.attributeAffects(result["chunkSize"], cls.aTokens)
        om.MPxNode.attributeAffects(result["useCustomRange"], cls.aTokens)
        om.MPxNode.attributeAffects(result["customRange"], cls.aTokens)
        om.MPxNode.attributeAffects(result["useScoutFrames"], cls.aTokens)
        om.MPxNode.attributeAffects(result["scoutFrames"], cls.aTokens)
        om.MPxNode.attributeAffects(result["startFrame"], cls.aTokens)
        om.MPxNode.attributeAffects(result["endFrame"], cls.aTokens)
        om.MPxNode.attributeAffects(result["byFrame"], cls.aTokens)

        return result

    @classmethod
    def makeIntAttribute(cls, attr_name, short_name, **kwargs):
        """
        Create an int attribute.
        """
        default = kwargs.get("default", 0)
        attr = om.MFnNumericAttribute()
        result = attr.create(attr_name, short_name, om.MFnNumericData.kInt, default)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        if "min" in kwargs:
            attr.setMin(kwargs["min"])
        if "max" in kwargs:
            attr.setMax(kwargs["max"])
        return result

    @classmethod
    def makeBoolAttribute(cls, attr_name, short_name, **kwargs):
        """
        Create a bool attribute.
        """
        default = kwargs.get("default", True)
        attr = om.MFnNumericAttribute()
        result = attr.create(attr_name, short_name, om.MFnNumericData.kBoolean, default)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        return result

    @classmethod
    def makeStringAttribute(cls, attr_name, short_name, **kwargs):
        attr = om.MFnTypedAttribute()
        result = attr.create(attr_name, short_name, om.MFnData.kString)
        attr.hidden = kwargs.get("hidden", False)
        attr.writable = kwargs.get("writable", True)
        attr.readable = kwargs.get("readable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        attr.array = kwargs.get("array", False)
        return result

    @classmethod
    def makeKvPairsAttribute(cls, attr_name, short_name, **kwargs):
        cAttr = om.MFnCompoundAttribute()
        tAttr = om.MFnTypedAttribute()

        result_key = tAttr.create(
            f"{attr_name}Key", f"{short_name}k", om.MFnData.kString
        )
        result_value = tAttr.create(
            f"{attr_name}Value", f"{short_name}v", om.MFnData.kString
        )
        result_compound = cAttr.create(attr_name, short_name)
        cAttr.hidden = kwargs.get("hidden", False)
        cAttr.writable = kwargs.get("writable", True)
        cAttr.array = True
        cAttr.addChild(result_key)
        cAttr.addChild(result_value)
        return {"compound": result_compound, "key": result_key, "value": result_value}

    @classmethod
    def makeTimeAttribute(cls, attr_name, short_name, **kwargs):
        attr = om.MFnUnitAttribute()
        result = attr.create(attr_name, short_name, om.MFnUnitAttribute.kTime)
        attr.writable = kwargs.get("writable", True)
        attr.keyable = kwargs.get("keyable", True)
        attr.storable = kwargs.get("storable", True)
        return result

    def compute(self, plug, data):
        pass
        """Compute output json from input attribs."""
        if not ((plug == self.aOutput)):
            return None

    # TASK ACCESSOR METHOD
    @classmethod
    def getTaskValues(cls, data, aTask):
        result = {}
        # result["perTask"] = data.inputValue(aTask["perTask"]).asInt()

        result["label"] = data.inputValue(aTask["label"]).asString()
        result["instance_type"] = data.inputValue(aTask["instanceType"]).asString()
        result["preemptible"] = data.inputValue(aTask["preemptible"]).asBool()

        result["output_path"] = data.inputValue(aTask["output_path"]).asString()

        result["software"] = []
        array_handle = data.inputArrayValue(aTask["software"])
        while not array_handle.isDone():
            software = array_handle.inputValue().asString().strip()
            if software:
                result["software"].append(software)
            array_handle.next()

        result["commands"] = []
        array_handle = data.inputArrayValue(aTask["commands"])
        while not array_handle.isDone():
            cmd = array_handle.inputValue().asString().strip()
            if cmd:
                result["commands"].append(cmd)
            array_handle.next()

        result["environment"] = []
        array_handle = data.inputArrayValue(aTask["environment"])
        while not array_handle.isDone():
            key = (
                array_handle.inputValue()
                .child(aTask["environmentKey"])
                .asString()
                .strip()
            )
            value = (
                array_handle.inputValue()
                .child(aTask["environmentValue"])
                .asString()
                .strip()
            )
            if key and value:
                result["environment"].append({"key": key, "value": value})
            array_handle.next()

        result["extra_assets"] = []
        array_handle = data.inputArrayValue(aTask["extraAssets"])
        while not array_handle.isDone():
            path = array_handle.inputValue().asString().strip()
            if path:
                result["extra_assets"].append(path)
            array_handle.next()

        return result

    @classmethod
    def getJobValues(cls, data, attr):
        result = {}
        result["label"] = data.inputValue(attr["label"]).asString()
        result["description"] = data.inputValue(attr["description"]).asString()
        result["project_name"] = data.inputValue(attr["projectName"]).asString()

        metadata = {}
        array_handle = data.inputArrayValue(attr["metadata"])
        while not array_handle.isDone():
            key = (
                array_handle.inputValue().child(attr["metadataKey"]).asString().strip()
            )
            value = (
                array_handle.inputValue()
                .child(attr["metadataValue"])
                .asString()
                .strip()
            )
            metadata[key] = value
            array_handle.next()
        result["metadata"] = metadata
        result["current_time"] = (
            data.inputValue(attr["currentTime"]).asTime().asUnits(om.MTime.uiUnit())
        )
        result["location"] = data.inputValue(attr["locationTag"]).asString()
        result["author"] = data.inputValue(attr["author"]).asString()

        print("RESULT IN GET JOB VALUES", result)
        return result

    @classmethod
    def getSequences(cls, data):
        result = {"main_sequence": None, "scout_sequence": None}

        chunk_size = data.inputValue(cls.aFramesAttributes["chunkSize"]).asInt()
        use_custom_range = data.inputValue(
            cls.aFramesAttributes["useCustomRange"]
        ).asBool()

        if use_custom_range:
            custom_range = data.inputValue(
                cls.aFramesAttributes["customRange"]
            ).asString()
            result["main_sequence"] = Sequence.create(
                custom_range, chunk_size=chunk_size, chunk_strategy="progressions"
            )
        else:
            start_frame = (
                data.inputValue(cls.aFramesAttributes["startFrame"])
                .asTime()
                .asUnits(om.MTime.uiUnit())
            )
            end_frame = (
                data.inputValue(cls.aFramesAttributes["endFrame"])
                .asTime()
                .asUnits(om.MTime.uiUnit())
            )
            by_frame = data.inputValue(cls.aFramesAttributes["byFrame"]).asInt()
            result["main_sequence"] = Sequence.create(
                int(start_frame),
                int(end_frame),
                by_frame,
                chunk_size=chunk_size,
                chunk_strategy="progressions",
            )

        use_scout_frames = data.inputValue(
            cls.aFramesAttributes["useScoutFrames"]
        ).asBool()

        if use_scout_frames:
            scout_frames = data.inputValue(
                cls.aFramesAttributes["scoutFrames"]
            ).asString()

            match = re.compile(r"^(auto|fml)[, :]+(\d+)$").match(scout_frames)

            if match:
                keyword = match.group(1)
                # This will hold the captured digits
                samples = int(match.group(2))
                if keyword == "auto":
                    result["scout_sequence"] = result["main_sequence"].subsample(
                        samples
                    )
                elif keyword == "fml":
                    result["scout_sequence"] = result["main_sequence"].calc_fml(samples)
            else:
                try:
                    result["scout_sequence"] = Sequence.create(scout_frames)
                except (ValueError, TypeError):
                    pass
        return result

    @staticmethod
    def composeEnvVars(env_vars):
        """
        Processes a list of environment variables and composes a dictionary of key-value pairs.

        The function handles keys both with and without square brackets:
        - If a key is enclosed in square brackets and already exists in the result dictionary,
        the new value is concatenated to the existing value using a colon as a separator.
        - If a key is enclosed in square brackets and does not exist in the result dictionary,
        it is added without the brackets.
        - If a key is not enclosed in brackets, it is added to the dictionary directly, and any
        existing value under the same key is overwritten.

        Args:
            env_vars (list of dict): A list of dictionaries where each dictionary has a 'key' and 'value'
                                    indicating the environment variable's name and value respectively.

        Returns:
            dict: A dictionary with environment variable keys as dictionary keys and the corresponding values.
                If keys are enclosed in brackets and repeated, their values are concatenated.

        Example:
            >>> composeEnvVars([{"key": "[PATH]", "value": "/usr/bin"}, {"key": "[PATH]", "value": "/bin"}])
            {'PATH': '/usr/bin:/bin'}
            >>> composeEnvVars([{"key": "USER", "value": "root"}, {"key": "SHELL", "value": "/bin/bash"}])
            {'USER': 'root', 'SHELL': '/bin/bash'}
        """
        result = {}
        for env_var in env_vars:
            key = env_var["key"]
            value = env_var["value"]

            if key.startswith("[") and key.endswith("]"):
                stripped_key = key[1:-1]
                if stripped_key in result:
                    result[stripped_key] = f"{result[stripped_key]}:{value}"
                else:
                    result[stripped_key] = value
            else:
                result[key] = value

        return result

    @classmethod
    def generateUploadTasks(cls, files, prefix, max_files_per_upload=10):
        """Generate the upload tasks."""
        for i in range(0, len(files), max_files_per_upload):
            name = f"{prefix}{i}"
            u = Upload(name)
            for f in files[i : i + max_files_per_upload]:
                path = f.strip()
                size = os.path.getsize(path)
                u.push_files({"path": path, "size": size})
            yield u

    @classmethod
    def get_packages_data(cls, software_list):
        """Get package IDs and env based on selected software.

        When making queries to the package tree, we must qualify host and plugin paths with the
        platform. The platform was previously stripped away because it was not needed in a single
        platform environment. We don't want to have the word linux next to every entry in the
        dropdown.

        * "maya 1.0.0" must be "maya 1.0.0 linux"
        * "maya 1.0.0 linux/arnold 5.0.0" must be "maya 1.0.0 linux/arnold 5.0.0 linux"
        """
        tree_data = coredata.data().get("software")

        package_ids = []
        environment = []
        print("software_list", software_list)
        for package in filter(
            None, [tree_data.find_by_path(path) for path in software_list if path]
        ):
            if package:
                package_ids.append(package["package_id"])
                for entry in package["environment"]:
                    if entry["merge_policy"].endswith("pend"):

                        environment.append(
                            {
                                "key": f"[{entry['name']}]",
                                "value": entry["value"],
                            }
                        )
                    else:
                        environment.append(
                            {
                                "key": entry["name"],
                                "value": entry["value"],
                            }
                        )
        package_ids = list(set(package_ids))
        print("package_ids", package_ids)
        return package_ids, environment

    # Helper functions to compute the job and tasks
    @classmethod
    def computeJob(cls, job_values, context=None):
        """Compute the job."""

        if not context:
            context = {}
        name = job_values["label"].format(**context)
        job = Job(name)
        metadata = job_values["metadata"]
        # loop through metadata and resolve values with context
        for key, value in metadata.items():
            metadata[key] = value.format(**context)
        job.metadata(metadata)

        job.project(job_values["project_name"])

        comment = job_values["description"].format(**context)
        job.comment(comment)

        author = job_values["author"].format(**context)
        job.author(author)

        location = job_values["location"].format(**context)
        job.location(location)
        return job

    @classmethod
    def computeTask(cls, task_values, context=None):
        """Compute the common task."""
        name = task_values["label"].format(**context)
        task = Task(name)

        task.hardware(task_values["instance_type"])
        task.preemptible(task_values["preemptible"])

        for command in task_values["commands"]:
            command = command.format(**context)
            task.push_commands(Cmd(*shlex.split(command)))

        software_list = task_values["software"]
        package_ids, environment = cls.get_packages_data(software_list)
        environment += task_values["environment"]
        env_dict = cls.composeEnvVars(environment)
        task.env(env_dict)
        task.packages(*package_ids)

        task.lifecycle({"minsec": 30, "maxsec": 1500})
        task.initial_state("START")

        output_path = task_values["output_path"].format(**context)
        task.output_path(output_path)

        upload_prefix = f"{task.name}_xtr_"
        for uploadTask in cls.generateUploadTasks(
            task_values["extra_assets"],
            prefix=upload_prefix,
            max_files_per_upload=cls.MAX_FILES_PER_UPLOAD,
        ):
            task.add(uploadTask)
        return task

    def getStaticContext(self, data):

        this_node = self.thisMObject()
        dep_fn = om.MFnDependencyNode(this_node)

        sequences = self.getSequences(data)

        scenepath = cmds.file(q=True, sn=True)
        scenename = os.path.splitext(cmds.file(q=True, sn=True, shn=True))[0]
        scenedir = os.path.dirname(scenepath)
        mayaprojdir = cmds.workspace(q=True, rd=True)
        imagesdir = cmds.workspace(fileRuleEntry="images")

        nodename = dep_fn.name()
        sequence = str(sequences["main_sequence"])
        seqstart = str(sequences["main_sequence"].start)
        seqend = str(sequences["main_sequence"].end)
        seqlen = str(len(sequences["main_sequence"]))
        hostname = socket.getfqdn()

        username = os.getlogin()

        return {
            "nodename": nodename,
            "scenepath": scenepath,
            "scenename": scenename,
            "scenedir": scenedir,
            "mayaprojdir": mayaprojdir,
            "imagesdir": imagesdir,
            "sequence": sequence,
            "seqstart": seqstart,
            "seqend": seqend,
            "seqlen": seqlen,
            "hostname": hostname,
            "username": username,
        }

    @classmethod
    def getDynamicContext(cls, static_context, chunk):
        context = static_context.copy()
        context["chunk"] = str(chunk)
        context["start"] = str(chunk.start)
        context["end"] = str(chunk.end)
        context["step"] = str(chunk.step)
        context["chunklen"] = str(len(chunk))
        return context
