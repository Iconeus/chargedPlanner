from datetime import date
from chargedPlanner.decorators import singleton
from chargedPlanner.chargedPlanner import get_config_filePath

@singleton
class LuccaAPI(object) :

    import json
    with open(get_config_filePath(), "r") as f:
        baseUrl = json.load(f)["luccaURL"]
        f.close()

    # On windows, set your token on credential manager with :
    # cmdkey /generic:MyLuccaToken /user:dummy /pass:<TOKEN>

    def __init__(self):

        self.__headers__ = {}

        try :
            import keyring  
            self.__headers__["Authorization"] = "lucca application=" + keyring.get_password("MyLuccaToken", "dummy")

        except Exception as e:

            from colorama import init, Fore

            init(autoreset=True)
            print(
                Fore.RED
                + "Error retrieving token: {e}"
            )
            import sys
            sys.exit(1)

    # =====================================================

    def __post__(self,url : str):

        # Lucca API Token not filled, cannot send the request
        if not len(self.__headers__) :
            return {}

        # Make the GET request
        print("url= ", url)
        import requests
        response = requests.get(LuccaAPI.baseUrl + url, headers=self.__headers__)

        # Check the response
        if response.status_code == 200:
            print("Success !")  # If the response is JSON, parse and print it
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

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

        if ans == None :
            return []

        if not len(ans["data"]):
            return []

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


