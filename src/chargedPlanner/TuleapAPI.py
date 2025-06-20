from typing import Any

import requests
from enum import Enum
import keyring

class TuleapBugsFieldsID(Enum) :
    EstimatedDays = 436
    RemainingDays = 437

class TuleapFeatsFieldsID(Enum) :
    EstimatedDays = 451
    RemainingDays = 452


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

            if tracker == "Versions" :
                return TuleapVersion(response)
            elif tracker == "Bugs" :
                return TuleapBug(response)
            elif tracker == "Features" :
                return TuleapFeature(response)
            else :
                print("skipping unrecognised item id : ", artifactId )
        else :
            print(f"Error: {response.status_code}")
            print(response.text)

    def __init__(self, artifactId : int ):

        raise TypeError("TuleapArtifactIO is an abstract class and cannot be instantiated directly.")

        # super().__init__()
        # self.__url__ = f"{TuleapIO.base_url}/artifacts/{artifactId}"
        # self.__Id__ = artifactId

    def __initialise__(self, response) -> Any :

        self.__jSonInfo__ = response.json()

        self.__tuleapId__ =  self.__jSonInfo__['id']
        self.__traker__ = self.__jSonInfo__['tracker']['label']

    def print(self):

        print("==================  Tuleap ARTIFACT info : ================")
        print(f"ID: {self.__jSonInfo__['id']}, \n"
              f"Project Label: {self.__jSonInfo__['project']['label']}\n",
              f"Tracker: {self.__jSonInfo__['tracker']['label']}")

        # print("================== ARTIFACT trackers for milestone : ================")
        for item in self.__jSonInfo__['values']:
            if item['type'] == "art_link":
                links = item['links']
                for artifact in links:
                    print("linked artifact id = " + str(artifact['id']))
        print("==========================================================")


class TuleapVersion(TuleapArtifactIO) :

    def __init__(self, response) :

        # cannot call the mother class constructor that raises an exception
        self.__initialise__(response)

        if not self.__traker__ == "Versions" :
            raise ValueError("This json is not describing a version !")

        self.__linkedArtifacts__ = []

        for item in self.__jSonInfo__['values']:
            if item['type'] == "art_link":
                links = item['links']
                for artifact in links:
                    id = int(artifact['id'])
                    print("linked artifact id = " + str(id))

                    self.__linkedArtifacts__.append( TuleapArtifactIO.factory(id) )

    def print(self) :

        print("==================  TuleapVersion print : ================")
        super().print()
        print("class type : ", type(self))
        for i in self.__linkedArtifacts__:
            i.print()
        print("==========================================================")


class TuleapBug(TuleapArtifactIO) :

    def __init__(self, response) :

        # cannot call the mother class constructor that raises an exception
        self.__initialise__(response)

        if not self.__traker__ == "Bugs" :
            raise ValueError("This json is not describing a Bug !")

    def print(self) :

        print("==================  TuleapBug print : ================")
        super().print()
        print("class type : ", type(self))
        print("==========================================================")

class TuleapFeature(TuleapArtifactIO) :

    def __init__(self, response) :

        # cannot call the mother class constructor that raises an exception
        self.__initialise__(response)

        if not self.__traker__ == "Features" :
            raise ValueError("This json is not describing a Feature !")

    def print(self):

        print("==================  TuleapFeature print : ================")
        super().print()
        print("class type : ", type(self))
        print("==========================================================")

### Access icoLab 1.4 milestone as an artifact  :
# artifact_1_4 = 1109
# url = f"{base_url}/artifacts/{artifact_1_4}"
# response = requests.get(url, headers=headers)
#
# if response.status_code == 200:
#     icolab14 = response.json()
#     print("================== ARTIFACT trackers for milestone Icolab 1.4: ================")
#     for item  in icolab14['values'] :
#         if item['type'] == "art_link" :
#             links= item['links']
#             for artifact in links :
#                 print("artifact id = " + str(artifact['id'])  )
# else:
#     print(f"Error: {response.status_code}")
#     print(response.text)


# Get a handle on IcoLab Version BETA 1.4.0 rCBV - artifact ID 1109
artifact_1_4 = TuleapArtifactIO.factory(1109)
artifact_1_4.print()


# ## Access one artifact
#
# artifactID = 1129
# url = f"{base_url}/artifacts/{artifactID}"
# response = requests.get(url, headers=headers)
#
# if response.status_code == 200:
#     artifact = response.json()
#     print("================== Artifact "+ str(artifactID) +" ================")
#     # improve diagnostics on scan reading missing fields
#     if artifact['tracker']['label'] == "Bug" :
#         print(f"artifact :"
#               f"\n\t\id= {artifact['id']},"
#               f"\n\ttitle : {artifact['title']}"
#               f"\n\ttype : {artifact['tracker']['label']}"
#               f"\n\tassignee : {artifact['assignees'][0]['username']}"
#               )
#
#         for iField in artifact['values'] :
#             if int(iField['field_id']) == TuleapBugsFieldsID.EstimatedDays.value :
#                 print(f"Estimated days = {iField['value']}")
#             if int(iField['field_id']) == TuleapBugsFieldsID.RemainingDays.value :
#                 print(f"Remaining days = {iField['value']}")
#
#     elif artifact['tracker']['label'] == "Features" :
#
#         print(f"artifact :"
#               f"\n\tid= {artifact['id']},"
#               f"\n\ttitle : {artifact['title']}"
#               f"\n\ttype : {artifact['tracker']['label']}"
#               )
#
#         for iField in artifact['values']:
#             if int(iField['field_id']) == TuleapFeatsFieldsID.EstimatedDays.value:
#                 print(f"Estimated days = {iField['value']}")
#             if int(iField['field_id']) == TuleapFeatsFieldsID.RemainingDays.value:
#                 print(f"Remaining days = {iField['value']}")
#     else :
#
#         print(f"artifact type non recognised :"
#               f"\n\ttype= {artifact['tracker']['label']}"
#               )
#
# else:
#     print(f"Error: {response.status_code}")
#     print(response.text)

