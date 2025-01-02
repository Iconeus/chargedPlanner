# DevTeam Gantt Planner

DevTeam Gantt Planner is a Python-based tool designed to assist development teams in creating and visualizing Gantt charts for project planning and task management.

## Features

Project Scheduling: Define features, define the required effort, assign them to developers within the DevTeam. Outline project timelines.

Team Assignment: Allocate tasks to specific developers or teams.

Gantt Chart Generation: Visualize project schedules through interactive Gantt charts.

Once a project is defined, it is possible to visualise it as Gantt chart with different levels of granularity (Project, Version). See below the Gantt chart for a specific version of the project : 

![image](docs/images/VersionGantt.PNG)

At the developer level, the associated workload can be visualised under the form of a Gannt diagram, or a loadchart. Peaks overcoming 100% effort are highlighted in red :

![image](docs/images/DevGantt.PNG)

![image](docs/images/DevCharge.PNG)



## Installation

Ensure you have Python 3.6 or higher installed. Then, install the required dependencies:
```
  pip install -r requirements.txt
```

## Usage
Clone the Repository:

```
https://github.com/Iconeus/chargedPlanner
```

## Prepare Your Data:

Create a json file named tasks.csv with the following structure:

```
{
    "devs": [
        {
            "name": "TheDevName"
        },
}
```

Fill all the devs of your group and place the file in the project resource folder : 
```
C:\Users\<currentUser>\.config\chargedPlanner\devs.json
```

## Getting started :

```
from chargedPlanner import * 

charles = DevGroup()["Charles"]
selene = DevGroup()["Selene"]

connFeat = Feature(featName="Connectivity",
                   remainingEffort=5,
                   assignee=charles,
                   percentageLoad = 20,
                   startDate=datetime(2024, 12, 26).date())

seedMapFeat = Feature(featName="SeedMap",
                      remainingEffort=15,                      assignee=selene,
                      percentageLoad=20,                      startDate=datetime(2024, 11, 15).date())

scanV2Feat = Feature(featName="ScanV2",
                    remainingEffort=15,
                     assignee=charles,
                     percentageLoad=40,
                     startDate=datetime(2025, 1, 8).date())

version1 = IcoStudioVersion("1.0.0")
version1.addFeat(connFeat)
version1.addFeat(seedMapFeat)

with pytest.raises(ValueError):
    charles.addWorkLoad(seedMapFeat,50)

version2 = IcoStudioVersion("1.1.0")
version2.addFeat(scanV2Feat)

icoStudioProject = Project(IconeusProduct.IcoStudio)
icoStudioProject.addVersion(version1)
icoStudioProject.addVersion(version2)

print(icoStudioProject)
icoStudioProject.gantt()

version1.gantt()

charles.gantt()
charles.loadChart()

selene.gantt()
selene.loadChart()

icoStudioProject.serialise()
```

See the auto tests for code usage 


## Dependencies

See file : requirements.txt

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Special thanks to the contributors of the following resources:
Gantt Charts in Python - Plotly
