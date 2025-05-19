import requests
from enum import Enum
import keyring

class TuleapFieldsID(Enum) :
    EstimatedDays = 436
    RemainingDays = 437

base_url = "https://iconeus.tuleap.cloud/api"

headers = {
    "X-Auth-AccessKey": keyring.get_password("MyTuleapToken", "dummy")
}

### List the projects :

endpoint = f"{base_url}/projects"
response = requests.get(endpoint, headers=headers)

if response.status_code == 200:
    projects = response.json()
    print("Available Projects:")
    for project in projects:
        print(f"ID: {project['id']}, Name: {project['label']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)


### Access project 102 -> icoLab (todo get the id from the projList) :

project_id = "102"
endpoint = f"{base_url}/projects/{project_id}"
response = requests.get(endpoint, headers=headers)

if response.status_code == 200:
    project_data = response.json()
    print("Project Details:")
    print(project_data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)


### Access the icoLab milestones :

endpoint = f"{base_url}/projects/{project_id}/milestones"
response = requests.get(endpoint, headers=headers)

if response.status_code == 200:
    milestones = response.json()
    print("==================  MILESTONES : ================")
    #print(milestones)
    for milestone in milestones :
        print(f"ID: {milestone['id']},"
              f" Name: {milestone['label']}, "
              f" Dates : {milestone['start_date']} -> {milestone['end_date']}"
              f" Artifact : {milestone['artifact']['id']}")

else:
    print(f"Error: {response.status_code}")
    print(response.text)


### Access icoLab 1.4 milestone as an artifact  :
artifact_1_4 = 1109
endpoint = f"{base_url}/artifacts/{artifact_1_4}"
response = requests.get(endpoint, headers=headers)

if response.status_code == 200:
    icolab14 = response.json()
    print("================== ARTIFACT trackers for milestone Icolab 1.4: ================")
    for item  in icolab14['values'] :
        if item['type'] == "art_link" :
            links= item['links']
            for artifact in links :
                print("artifact id = " + str(artifact['id'])  )
else:
    print(f"Error: {response.status_code}")
    print(response.text)


## Access one artifact

artifactID = "1445"
endpoint = f"{base_url}/artifacts/{artifactID}"
response = requests.get(endpoint, headers=headers)

if response.status_code == 200:
    artifact = response.json()
    print("================== Artifact 1445 ================")
    # improve diagnostics on scan reading missing fields
    print(f"artifact :"
          f"\n\t\id= {artifact['id']},"
          f"\n\ttitle : {artifact['title']}"
          f"\n\ttype : {artifact['tracker']['label']}"
          f"\n\tassignee : {artifact['assignees'][0]['username']}"
          )

    for iField in artifact['values'] :
        if int(iField['field_id']) == TuleapFieldsID.EstimatedDays.value :
            print(f"Estimated days = {iField['value']}")
        if int(iField['field_id']) == TuleapFieldsID.RemainingDays.value :
            print(f"Remaining days = {iField['value']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

