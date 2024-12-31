# DevTeam Gantt Planner

DevTeam Gantt Planner is a Python-based tool designed to assist development teams in creating and visualizing Gantt charts for project planning and task management.

## Features

Project Scheduling: Define features, define the required effort, assign them to developers within the DevTeam. Outline project timelines.

Team Assignment: Allocate tasks to specific developers or teams.

Gantt Chart Generation: Visualize project schedules through interactive Gantt charts.

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

See the auto tests for code usage 

## Dependencies

Python 3.6+
plotly

Copy code
pip install pandas matplotlib plotly

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Special thanks to the contributors of the following resources:
Gantt Charts in Python - Plotly
