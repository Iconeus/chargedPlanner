from datetime import date
import os
import json

from decorators import singleton

@singleton
class LuccaAPI(object) :

    baseUrl = "https://iconeus-rh.ilucca.net/api/v3/leaves"

    def __init__(self):

        self.__headers__ = {}

        user_config_path = os.path.expanduser("~/.config/chargedPlanner/luccaToken.json")

        if os.path.exists(user_config_path):
            with open(user_config_path, "r") as f:
                self.__headers__["Authorization"] = "lucca application=" + json.load(f)["token"]

        else:

            from colorama import init, Fore

            init(autoreset=True)
            print(
                Fore.RED
                + "Please add your lucca token in : ~/.config/chargedPlanner/luccaToken.json"
                + "\nUntil then, Lucca bindings are disabled"
            )

    def __post__(self,url : str):

        # Lucca API Token not filled, cannot send the request
        if not len(self.__headers__) :
            return {}

        # Make the GET request
        import requests

        print("url= ", url)
        response = requests.get(LuccaAPI.baseUrl + url, headers=self.__headers__)

        # Check the response
        if response.status_code == 200:
            print("Success !")  # If the response is JSON, parse and print it
        else:
            print(f"Error {response.status_code}: {response.text}")

        return response.json()

    def getLeaves(self,lucca_ID : int, start_date : date, end_date = date) -> list :

        if not isinstance(lucca_ID, int):
            print("lucca ID type : ", type(lucca_ID))
            raise ValueError("incompatible lucca ID type")
        if not isinstance(start_date, date):
            print("start date type : ", type(start_date))
            raise ValueError("incompatible start_date type")
        if not isinstance(end_date, date):
            print("end_date type : ", type(end_date))
            raise ValueError("incompatible end_date type")

        data = []
        url = "?leavePeriod.ownerId=" + str(lucca_ID) + "&date=between," + str(start_date) + "," + str(end_date)
        ans = self.__post__(url)

        if not len(ans["data"]["items"]) :
            return []

        for i in ans["data"]["items"] :

            leave = self.__post__("/"+i['id'])

            # print("\t", "date : ", leave['data']['date'])
            # print("\t", "startDate : ", leave['data']['startDateTime'])
            # print("\t", "isRemoteWork : ", leave['data']['isRemoteWork'])
            # print("\t", "startsAt : ", leave['data']['startsAt'])
            # print("\t", "endsAt : ", leave['data']['endsAt'])
            # print("\t", "leaveAccountDuration : ", leave['data']['leaveAccountDuration'])

            from datetime import datetime
            data.append({"date": datetime.strptime(leave["data"]["date"], "%Y-%m-%dT%H:%M:%S"),
                         "time_period": "AM" if leave["data"]["isAM"] == True else "PM",
                         "duration": leave["data"]["leaveAccountDuration"]
                         })

        # Convert to DataFrame
        from pandas import DataFrame
        df = DataFrame(data)

        # Aggregate by date and duration
        aggregated = df.groupby("date")["duration"].sum().reset_index()

        # Convert back to a desired format
        return aggregated.to_dict(orient="records")


