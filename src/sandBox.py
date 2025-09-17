from chargedPlanner.chargedPlanner import *

charles = DevGroup()["Charles"]
luc = DevGroup()["Luc"]
mohamed = DevGroup()["Mohamed"]
sara = DevGroup()["Sara"]
selene = DevGroup()["Selene"]

icoStudio240 = IcoStudioVersion("2.4.0")

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1215
# icoStudio240.addFeat(
# 	Feature(featName="ScanV2_readers",
# 			totalEffort=1,
# 			remainingEffort=1,
# 			assignee=adrien,
# 			percentageLoad=75,
# 			startDate=datetime(2024, 9, 20).date())
# )
# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1218
# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1219
# icoStudio240.addFeat(
# 	Feature(featName="ScanV2_fuslab",
# 			totalEffort=10,
# 			remainingEffort=10,
# 			assignee=luc,
# 			percentageLoad=75,
# 			startDate=datetime(2024, 9, 20).date())
# )

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1211
# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1216
icoStudio240.addFeat(
	Feature(featName="ScanV2_Matlab",
			totalEffort=3,
			remainingEffort=3,
			assignee=mohamed,
			percentageLoad=75,
			startDate=datetime(2024, 9, 20).date())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=3642
icoStudio240.addFeat(
	Feature(featName="rCBV_Metier",
			totalEffort=6,
			remainingEffort=6,
			assignee=luc,
			percentageLoad=80,
			startDate=datetime(2024, 9, 20).date())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1260
icoStudio240.addFeat(
	Feature(featName="ActMap_Soft",
			totalEffort=35,
			remainingEffort=18,
			assignee=charles,
			percentageLoad=80,
			startDate=datetime(2025, 9, 15).date())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1262
icoStudio240.addFeat(
	Feature(featName="ActMap_Metier",
			totalEffort=4,
			remainingEffort=3,
			assignee=luc,
			percentageLoad=80,
			startDate=datetime(2024, 9, 20).date())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=3986
# https://iconeus.tuleap.cloud/plugins/tracker/?aid=3987
icoStudio240.addFeat(
	Feature(featName="RemoveAcq",
			totalEffort=2,
			remainingEffort=2,
			assignee=charles,
			percentageLoad=80,
			startDate=charles.getEndDateForLatestAssignedFeat())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=3520
icoStudio240.addFeat(
	Feature(featName="depToLibIconeus",
			totalEffort=20,
			remainingEffort=2,
			assignee=charles,
			percentageLoad=80,
			startDate=charles.getEndDateForLatestAssignedFeat())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=1267
icoStudio240.addFeat(
	Feature(featName="rCBV_Soft",
			totalEffort=32,
			remainingEffort=5,
			assignee=selene,
			percentageLoad=80,
			startDate=selene.getEndDateForLatestAssignedFeat())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=3902
icoStudio240.addFeat(
	Feature(featName="getGlobalSignal",
			totalEffort=2,
			remainingEffort=1,
			assignee=selene,
			percentageLoad=80,
			startDate=selene.getEndDateForLatestAssignedFeat())
)

# https://iconeus.tuleap.cloud/plugins/tracker/?aid=4030
icoStudio240.addFeat(
	Feature(featName="installerChanges",
			totalEffort=1,
			remainingEffort=1,
			assignee=selene,
			percentageLoad=80,
			startDate=selene.getEndDateForLatestAssignedFeat())
)

icoStudio240.addFeat(
	DebugFeature(
		version=icoStudio240,
		assignee=charles,
		percentageLoad=5,
		timespan=timedelta(days=15))
)

icoStudio240.addFeat(
	DebugFeature(
		version=icoStudio240,
		assignee=selene,
		percentageLoad=5,
		timespan=timedelta(days=15))
)

icoStudio240.addFeat(
	DocumentationFeature(
		version=icoStudio240,
		assignee=sara,
		percentageLoad=10,
		timespan=timedelta(days=20)
	)
)

icoStudio240.gantt()
