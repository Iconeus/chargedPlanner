from chargedPlanner.chargedPlanner import *

charles = DevGroup()["Charles"]

connFeat = Feature(featName="Connectivity",
  					totalEffort=2, 
					remainingEffort=0,
					assignee=charles,
					percentageLoad=40,
					startDate=datetime(2024, 9, 24).date())

d = connFeat.getEndDate()

print("end day = ", d)