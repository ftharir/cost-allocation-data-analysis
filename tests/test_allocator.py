import pandas as pd
import pytest

from allocator import allocate_by_headcount, allocate_costs, allocate_direct_costs


def _costs():
    return pd.DataFrame({
        "company": ["Alpha company", "ALL", "ALL"],
        "cost_title": ["Software License", "Shared Office Space", "Shared Office Space"],
        "amount": [100.0, 900.0, 300.0],
        "period": ["1405/03", "1405/03", "1405/04"],
        "allocation_type": ["Direct", "Shared_Headcount", "Shared_Headcount"],
    })


def _headcount():
    return pd.DataFrame({
        "company": ["Alpha company", "Beta company", "Alpha company", "Beta company"],
        "headcount": [30, 60, 10, 0],
        "period": ["1405/03", "1405/03", "1405/04", "1405/04"],
    })


def test_direct_cost_stays_with_its_company():
    out = allocate_direct_costs(_costs())
    assert list(out["company"]) == ["Alpha company"]
    assert list(out["allocated_amount"]) == [100.0]


def test_shared_cost_follows_headcount_of_the_same_month():
    costs = _costs()
    out = allocate_by_headcount(costs[costs.allocation_type == "Shared_Headcount"], _headcount())
    march = out[out.period == "1405/03"].set_index("company")["allocated_amount"]
    assert march["Alpha company"] == pytest.approx(300.0)  # 900 * 30 / 90
    assert march["Beta company"] == pytest.approx(600.0)  # 900 * 60 / 90


def test_company_without_headcount_gets_nothing():
    costs = _costs()
    out = allocate_by_headcount(costs[costs.allocation_type == "Shared_Headcount"], _headcount())
    april = out[out.period == "1405/04"].set_index("company")["allocated_amount"]
    assert april["Beta company"] == 0
    assert april["Alpha company"] == pytest.approx(300.0)


def test_nothing_is_lost_or_created():
    final = allocate_costs(_costs(), _headcount())
    assert final["allocated_amount"].sum() == pytest.approx(_costs()["amount"].sum())
    assert final["allocated_amount"].notna().all()
