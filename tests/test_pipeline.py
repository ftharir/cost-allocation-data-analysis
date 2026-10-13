"""End-to-end checks on the real sample files in data/raw."""
import os

import pandas as pd
import pytest

from aggregator import aggregate_cost_data
from allocator import allocate_costs
from cleaner import clean_data, clean_headcount_data
from conftest import COST_FILES, HEADCOUNT_FILES, RAW
from exporter import export_to_excel
from loader import load_excel


@pytest.fixture(scope="module")
def datasets():
    cost = aggregate_cost_data([clean_data(load_excel(os.path.join(RAW, f))) for f in COST_FILES])
    head = aggregate_cost_data([clean_headcount_data(load_excel(os.path.join(RAW, f))) for f in HEADCOUNT_FILES])
    return cost, head


@pytest.fixture(scope="module")
def final(datasets):
    return allocate_costs(*datasets)


def test_all_six_raw_files_exist():
    for f in COST_FILES + HEADCOUNT_FILES:
        assert os.path.exists(os.path.join(RAW, f)), f


def test_cleaned_cost_data_has_standard_columns(datasets):
    cost, _ = datasets
    assert {"company", "cost_title", "amount", "period", "allocation_type"} <= set(cost.columns)
    assert not cost.columns.duplicated().any()


def test_only_the_expected_allocation_types_remain(datasets):
    cost, _ = datasets
    assert set(cost["allocation_type"]) == {"Direct", "Shared_Headcount"}


def test_no_negative_or_missing_amounts_after_cleaning(datasets):
    cost, _ = datasets
    assert (cost["amount"] >= 0).all()
    assert cost["amount"].notna().all()


def test_cost_titles_are_unified(datasets):
    cost, _ = datasets
    assert {"Shared Office", "Facility Repair"}.isdisjoint(set(cost["cost_title"]))


def test_the_duplicated_analysis_project_is_counted_once(datasets):
    cost, _ = datasets
    big = cost[(cost["company"] == "Gamma company") & (cost["cost_title"] == "Data Analysis Service")]
    assert len(big) == 1


def test_every_rial_is_allocated(datasets, final):
    cost, _ = datasets
    assert final["allocated_amount"].sum() == pytest.approx(cost["amount"].sum())


def test_expected_totals(final):
    assert len(final) == 57
    assert final["allocated_amount"].sum() == pytest.approx(6_504_000_000)
    by_period = final.groupby("period")["allocated_amount"].sum()
    assert by_period["1405/03"] == pytest.approx(2_933_000_000)
    assert by_period["1405/04"] == pytest.approx(3_571_000_000)


def test_companies_in_the_report(final):
    assert set(final["company"]) == {
        "Alpha company", "Beta company", "Gamma company", "Delta company", "Epsilon company", "Omega company",
    }
    assert "ALL" not in set(final["company"])


def test_company_with_missing_headcount_gets_no_shared_cost(final):
    shared = final[(final["company"] == "Epsilon company") & (final["period"] == "1405/04")
                   & (final["allocation_type"] == "Shared_Headcount")]
    assert (shared["allocated_amount"] == 0).all() and len(shared) > 0


def test_export_writes_a_readable_excel_file(final, tmp_path):
    target = tmp_path / "out.xlsx"
    export_to_excel(final, str(target))
    back = pd.read_excel(target)
    assert len(back) == len(final)
    assert back["allocated_amount"].sum() == pytest.approx(final["allocated_amount"].sum())


def test_committed_report_matches_a_fresh_run(final):
    saved = pd.read_excel(os.path.join(os.path.dirname(RAW), "processed", "Final_Cost_Report.xlsx"))
    assert len(saved) == len(final)
    assert saved["allocated_amount"].sum() == pytest.approx(final["allocated_amount"].sum())
