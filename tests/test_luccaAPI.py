import pytest

def test_lucca_api():

    from src.chargedPlanner.LuccaAPI import LuccaAPI
    from datetime import datetime

    l = LuccaAPI()

    lucca_ID = 16
    data = []
    url = ("?leavePeriod.ownerId=" + str(lucca_ID) + "&date=between," +
           str(datetime(2024, 12, 20).date()) + "," +
           str(datetime(2025, 12, 1).date()))

    ans = l.__post__(url)
