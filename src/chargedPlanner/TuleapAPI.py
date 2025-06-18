import requests
from enum import Enum
import keyring

class TuleapBugsFieldsID(Enum) :
    EstimatedDays = 436
    RemainingDays = 437

class TuleapFeatsFieldsID(Enum) :
    EstimatedDays = 451
    RemainingDays = 452

base_url = "https://iconeus.tuleap.cloud/api"

headers = {
    "X-Auth-AccessKey": keyring.get_password("MyTuleapToken", "dummy")
}

### List the projects :

url = f"{base_url}/projects"
response = requests.get(url, headers=headers)

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
url = f"{base_url}/projects/{project_id}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    project_data = response.json()
    print("Project Details:")
    print(project_data)
else:
    print(f"Error: {response.status_code}")
    print(response.text)


### Access the icoLab milestones :

url = f"{base_url}/projects/{project_id}/milestones"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    milestones = response.json()
    print("==================  MILESTONES : ================")
    #print(milestones)
    for milestone in milestones :
        print(f"ID: {milestone['id']},"
              f" Name: {milestone['label']}, "
              f" Dates : {milestone['start_date']} -> {milestone['end_date']}")

else:
    print(f"Error: {response.status_code}")
    print(response.text)


### Access icoLab 1.4 milestone as an artifact  :
artifact_1_4 = 1109
url = f"{base_url}/artifacts/{artifact_1_4}"
response = requests.get(url, headers=headers)

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

artifactID = 1129
url = f"{base_url}/artifacts/{artifactID}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    artifact = response.json()
    print("================== Artifact "+ str(artifactID) +" ================")
    # improve diagnostics on scan reading missing fields
    if artifact['tracker']['label'] == "Bug" :
        print(f"artifact :"
              f"\n\t\id= {artifact['id']},"
              f"\n\ttitle : {artifact['title']}"
              f"\n\ttype : {artifact['tracker']['label']}"
              f"\n\tassignee : {artifact['assignees'][0]['username']}"
              )

        for iField in artifact['values'] :
            if int(iField['field_id']) == TuleapBugsFieldsID.EstimatedDays.value :
                print(f"Estimated days = {iField['value']}")
            if int(iField['field_id']) == TuleapBugsFieldsID.RemainingDays.value :
                print(f"Remaining days = {iField['value']}")

    elif artifact['tracker']['label'] == "Features" :

        print(f"artifact :"
              f"\n\tid= {artifact['id']},"
              f"\n\ttitle : {artifact['title']}"
              f"\n\ttype : {artifact['tracker']['label']}"
              )

        for iField in artifact['values']:
            if int(iField['field_id']) == TuleapFeatsFieldsID.EstimatedDays.value:
                print(f"Estimated days = {iField['value']}")
            if int(iField['field_id']) == TuleapFeatsFieldsID.RemainingDays.value:
                print(f"Remaining days = {iField['value']}")
    else :

        print(f"artifact type non recognised :"
              f"\n\ttype= {artifact['tracker']['label']}"
              )

else:
    print(f"Error: {response.status_code}")
    print(response.text)

