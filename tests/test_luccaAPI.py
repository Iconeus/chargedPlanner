import pytest
from datetime import datetime, timedelta

def test_lucca_api():

    from src.chargedPlanner.LuccaAPI import LuccaAPI

    l = LuccaAPI()

    lucca_ID = 16

    data = []
    url = ("?leavePeriod.ownerId=" + str(lucca_ID) + "&date=between," +
           str(datetime(2024, 12, 20).date()) + "," +
           str(datetime(2025, 1, 1).date()))

    ans = l.__post__(url)

    print(ans)

    ans = l.getLeaves(
        lucca_ID,
        start_date= datetime(2024, 12, 20).date(),
        end_date= datetime(2025, 1, 1).date()
    )