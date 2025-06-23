from typing import Any
import requests
from enum import Enum
import keyring

class TuleapVersionsFieldsID(Enum) :
    Title = -100
    EstimatedDays = 436
    RemainingDays = 437

class TuleapBugsFieldsID(Enum) :
    Title = 417
    EstimatedDays = 436
    RemainingDays = 437

class TuleapFeatsFieldsID(Enum) :
    Title = 445
    # Feats are not assigned to an assignee !
    # AssignedTo = -100
    EstimatedDays = 451
    RemainingDays = 452

class TuleapTasksFieldsID(Enum) :
    Title = 514
    AssignedTo = 518
    EstimatedDays = 520
    RemainingDays = 521

class TuleapItemType(Enum):
    Versions = "Versions"
    Features = "Features"
    Requirements = "Requirements"
    Bugs = "Bugs"
    Tasks = "Tasks"

# //////////////////////////////////////////////////////////////////////////////

class TuleapIO(object) :

    base_url = "https://iconeus.tuleap.cloud/api"

    headers = {
        "X-Auth-AccessKey": keyring.get_password("MyTuleapToken", "dummy")
    }

    def __init__(self):

        self.__url__ = ""

    def print(self, response ):
        raise ValueError("this base class method should never be called ! ")

    def get(self, print_response: bool = False ):

        response = requests.get(self.__url__, headers=TuleapIO.headers)

        if response.status_code == 200 and print_response:
            self.print(response)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

        return response

# ===========================================================

### List the projects :
class TuleapProjectListIO(TuleapIO) :

    def __init__(self):

        super().__init__()

        self.__url__ = f"{TuleapIO.base_url}/projects"

    def print(self, response):

        projects = response.json()
        print("======== Available Projects: =============")
        for project in projects:
            print(f"ID: {project['id']}, Name: {project['label']}")

projList = TuleapProjectListIO()
projList.get(print_response=True)

# ===========================================================

class TuleapProjectIO(TuleapIO) :

    def __init__(self, projId : int):

        super().__init__()
        self.__id__ = projId
        self.__url__ = f"{TuleapIO.base_url}/projects/{projId}"
        self.__milestonesUrl__ = self.__url__ + "/milestones"

    def print(self, response):

        project_data = response.json()
        print("======== Project "+ str(self.__id__) +" details:")
        print(project_data)

### Access project 102 -> icoLab (todo get the id from the projList) :
proj102 = TuleapProjectIO(projId=102)
proj102.get(print_response=True)

# ===========================================================

class TuleapProectMilestoneListIO(TuleapIO) :

    def __init__(self, projId : int ):

        super().__init__()
        self.__projId__ = projId
        self.__url__ = f"{TuleapIO.base_url}/projects/{projId}/milestones"

    def print(self, response):

        milestones = response.json()
        print("==================  MILESTONES : ================")
        # print(milestones)
        for milestone in milestones:
            print(f"ID: {milestone['id']},"
                  f" Name: {milestone['label']}, "
                  f" Dates : {milestone['start_date']} -> {milestone['end_date']}")

milestoneList = TuleapProectMilestoneListIO(proj102.__id__)
milestoneList.get(print_response=True)

# ===========================================================

class TuleapArtifactIO(TuleapIO) :

    url = f"{TuleapIO.base_url}/artifacts/"

    @staticmethod
    def factory(artifactId : int):

        query = TuleapArtifactIO.url + f"{artifactId}"
        response = requests.get(query, headers=TuleapIO.headers)

        if response.status_code == 200 :

            # Search for the type of this item
            artifact = response.json()
            tracker = artifact['tracker']['label']

            if tracker == TuleapItemType.Versions.value :
                return TuleapVersion(response)
            elif tracker == TuleapItemType.Bugs.value :
                return TuleapBug(response)
            elif tracker == TuleapItemType.Features.value :
                return TuleapFeature(response)
            elif tracker == TuleapItemType.Tasks.value:
                return TuleapTask(response)
            else :
                print("skipping unrecognised item id : ", artifactId )
        else :
            print(f"Error: {response.status_code}")
            print(response.text)

    def __init__(self, artifactId : int ):

        self.__title__ = None
        self.__estimatedDays__ = None
        self.__remainingdDays__ = None

        raise TypeError("TuleapArtifactIO is an abstract class and cannot be instantiated directly.")


    def __initialise__(self, response) -> Any :

        self.__jSonInfo__ = response.json()

        self.__title__ = None
        self.__estimatedDays__ = None
        self.__remainingDays__ = None

        self.__tuleapId__ =  self.__jSonInfo__['id']
        self.__traker__ = self.__jSonInfo__['tracker']['label']

        self.__linkedArtifacts__ = []

        for item in self.__jSonInfo__['values']:
            if item['type'] == "art_link":
                links = item['links']
                for artifact in links:
                    id = int(artifact['id'])
                    print("linked artifact id = " + str(id))

                    self.__linkedArtifacts__.append( TuleapArtifactIO.factory(id) )

    def getEstimatedDays(self) -> int :
        if self.__estimatedDays__ is None:
            print("Warning : Effort for " + self.__class__.__name__ + " = " +  str(self.__tuleapId__) + " not estimated")

        return self.__estimatedDays__

    def getRemainingDays(self) -> int:

        if self.__remainingDays__ is None:
            print("Warning : Remaining effort for " + self.__class__.__name__ + " = " +  str(self.__tuleapId__) + " not estimated")

        return self.__remainingDays__

    #         childrenReminingDaysSum += artifact.getRemainingDays()
    def print(self, separator: str ="" ):

        print(f"{separator}ID: {self.__jSonInfo__['id']},\n"
              f"{separator}Title: {self.__jSonInfo__['title']},\n",
              f"{separator}Project: {self.__jSonInfo__['project']['label']},\n",
              f"{separator}Tracker: {self.__jSonInfo__['tracker']['label']},\n",
              f"{separator}Estimated days: {self.getEstimatedDays()},\n",
              f"{separator}Remaining days: {self.getRemainingDays()}")

        for artifact in self.__linkedArtifacts__ :
            artifact.print(separator+"\t")

class TuleapVersion(TuleapArtifactIO) :

    def __init__(self, response) :

        # cannot call the mother class constructor that raises an exception
        self.__initialise__(response)

        if not self.__traker__ == TuleapItemType.Versions.value :
            raise ValueError("This json is not describing a version !")

        for iValue in self.__jSonInfo__['values']:
            if iValue["field_id"] == TuleapVersionsFieldsID.Title.value :
                self.__title__ = iValue["value"]
            if iValue["field_id"] == TuleapVersionsFieldsID.EstimatedDays.value :
                self.__estimatedDays__ = iValue["value"]
            if iValue["field_id"] ==  TuleapVersionsFieldsID.RemainingDays.value :
                self.__remainingDays__ = iValue["value"]

    def print(self, separator:str ="") :

        print("==================  TuleapVersion : ================")
        super().print(separator+"\t")
        print("class type : ", type(self))
        print("==========================================================")

class TuleapBug(TuleapArtifactIO) :

    def __init__(self, response) :

        # cannot call the mother class constructor that raises an exception
        # as TuleapArtifactIO is abstract
        self.__initialise__(response)

        if not self.__traker__ == TuleapItemType.Bugs.value :
            raise ValueError("This json is not describing a Bug !")

        for iValue in self.__jSonInfo__['values']:
            if iValue["field_id"] == TuleapBugsFieldsID.Title.value :
                self.__title__ = iValue["value"]
            if iValue["field_id"] == TuleapBugsFieldsID.EstimatedDays.value :
                self.__estimatedDays__ = iValue["value"]
            if iValue["field_id"] ==  TuleapBugsFieldsID.RemainingDays.value :
                self.__remainingDays__ = iValue["value"]

    def print(self,separator:str ="") :

        print(separator+"==================  Tuleap Bug : ================")
        super().print(separator)
        print(separator+"class type : ", type(self))
        print(separator+"==========================================================")

class TuleapFeature(TuleapArtifactIO) :

    def __init__(self, response) :

        # cannot call the mother class constructor that raises an exception
        self.__initialise__(response)

        if not self.__traker__ == TuleapItemType.Features.value :
            raise ValueError("This json is not describing a Feature !")

        for iValue in self.__jSonInfo__['values']:
            if iValue["field_id"] == TuleapFeatsFieldsID.Title.value :
                self.__title__ = iValue["value"]
            if iValue["field_id"] == TuleapFeatsFieldsID.EstimatedDays.value :
                self.__estimatedDays__ = iValue["value"]
            if iValue["field_id"] ==  TuleapFeatsFieldsID.RemainingDays.value :
                self.__remainingDays__ = iValue["value"]

        def checkEstimatedDays() -> None:

            childrenEstimatedDaysSum = 0
            childrenReminingDaysSum = 0
            for artifact in self.__linkedArtifacts__:
                childrenEstimatedDaysSum += artifact.getEstimatedDays()
                childrenReminingDaysSum += artifact.getRemainingDays()

            if  childrenEstimatedDaysSum != self.__estimatedDays__ :
                raise ValueError("The estimated days for this feature does not correspond to the sum of its children")
            if  childrenReminingDaysSum != self.__remainingDays__ :
                raise ValueError("The remaining days for this feature does not correspond to the sum of its children")

        checkEstimatedDays()

    def print(self, separator:str =""):

        print(separator+"==================  Tuleap Feature : ================")
        super().print(separator)
        print(separator+"class type : ", type(self))
        print(separator+"==========================================================")

class TuleapTask(TuleapArtifactIO) :

    def __init__(self, response) :

        # cannot call the mother class constructor that raises an exception
        self.__initialise__(response)

        if not self.__traker__ == TuleapItemType.Tasks.value :
            raise ValueError("This json is not describing a Task !")

        for iValue in self.__jSonInfo__['values']:
            if iValue["field_id"] == TuleapTasksFieldsID.Title.value :
                self.__title__ = iValue["value"]
            if iValue["field_id"] == TuleapTasksFieldsID.EstimatedDays.value :
                self.__estimatedDays__ = iValue["value"]
            if iValue["field_id"] ==  TuleapTasksFieldsID.RemainingDays.value :
                self.__remainingDays__ = iValue["value"]
            if iValue["field_id"] ==  TuleapTasksFieldsID.AssignedTo.value :
                if not len(iValue["values"]) == 1 :
                    raise ValueError("Only one assignee allowed !")
                self.__assigneeID__ = iValue["values"][0]['id']
                self.__assigneeName__ = iValue["values"][0]['username']

    def print(self, separator:str =""):

        print(separator+"==================  Tuleap Task : ================")
        super().print(separator)
        print(separator+"class type : ", type(self))
        print(separator+"Title : ", self.__title__)
        print(separator+"Estimated Days : ", self.__estimatedDays__)
        print(separator+"Remaining Days : ", self.__remainingDays__)
        print(separator+"Assigned to : ", self.__assigneeName__)
        print(separator+"==========================================================")

# Get a handle on an artifact ID 1109
# Artifact 1109 corresponds to IcoLab Version : BETA 1.4.0 rCBV
artifact_1_4 = TuleapArtifactIO.factory(1109)
artifact_1_4.print()
