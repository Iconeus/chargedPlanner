import pytest
from datetime import datetime, timedelta

def test_lucca_api():

    from src.chargedPlanner.LuccaAPI import LuccaAPI

    l = LuccaAPI()

    lucca_ID = 33

    data = []
    url = ("?leavePeriod.ownerId=" + str(lucca_ID) + "&date=between," +
           str(datetime(2025, 4, 20).date()) + "," +
           str(datetime(2025, 4, 30).date()))

    ans = l.__post__(url)

    print(ans)

    ans = l.getLeaves(
        lucca_ID,
        start_date= datetime(2024, 12, 1).date(),
        end_date= datetime(2025, 2, 20).date()
    )
