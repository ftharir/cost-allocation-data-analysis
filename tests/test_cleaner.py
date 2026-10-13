import pandas as pd

from cleaner import (
    clean_data,
    clean_headcount_data,
    handling_negative_amount,
    handling_nan_data,
    remove_duplicate_rows,
    standardize_company_names,
    standardize_cost_title,
    standardize_columns,
    standardize_period,
)


def test_column_names_in_persian_and_english_become_standard():
    df = pd.DataFrame(columns=["نام شرکت", "مبلغ (ریال)", "نوع خدمت", "دوره", "نحوه تخصیص"])
    out = standardize_columns(df)
    assert list(out.columns) == ["company", "amount", "cost_title", "period", "allocation_type"]


def test_company_name_variants_map_to_one_name():
    names = ["آلفا", "شرکت آلفا", "Alpha", "Alpha Co"]
    out = standardize_company_names(pd.DataFrame({"company": names}))
    assert set(out["company"]) == {"Alpha company"}


def test_omega_is_not_merged_into_gamma():
    out = standardize_company_names(pd.DataFrame({"company": ["شرکت امگا", "شرکت گاما"]}))
    assert list(out["company"]) == ["Omega company", "Gamma company"]


def test_all_companies_keyword():
    out = standardize_company_names(pd.DataFrame({"company": ["همه", "همه شرکت‌ها", "ALL"]}))
    assert set(out["company"]) == {"ALL"}


def test_cost_title_variants_are_unified():
    titles = ["Shared Office", "فضای اداری مشترک", "Facility Repair", "تعمیرات"]
    out = standardize_cost_title(pd.DataFrame({"cost_title": titles}))
    assert list(out["cost_title"]) == ["Shared Office Space", "Shared Office Space", "Repair Service", "Repair Service"]


def test_period_uses_slash():
    out = standardize_period(pd.DataFrame({"period": ["1405-03", "1405/04"]}))
    assert list(out["period"]) == ["1405/03", "1405/04"]


def test_negative_amount_becomes_zero(capsys):
    out = handling_negative_amount(pd.DataFrame({"amount": [100.0, -12.0]}))
    assert list(out["amount"]) == [100.0, 0.0]
    assert "Negative amount" in capsys.readouterr().out


def test_missing_numbers_become_zero():
    out = handling_nan_data(pd.DataFrame({"amount": [1.0, None], "headcount": [None, 5.0]}))
    assert out.isna().sum().sum() == 0


def test_identical_rows_are_removed_once(capsys):
    df = pd.DataFrame({"company": ["A", "A", "B"], "amount": [1, 1, 1]})
    out = remove_duplicate_rows(df)
    assert len(out) == 2
    assert "1 duplicate" in capsys.readouterr().out


def test_clean_data_on_a_small_raw_like_table():
    raw = pd.DataFrame({
        "ردیف": [1, 2, 3],
        "نام شرکت": ["شرکت آلفا", "همه شرکت‌ها", "شرکت آلفا"],
        "شرح خدمت": ["لایسنس نرم‌افزار", "اشتراک ابزار همکاری", "لایسنس نرم‌افزار"],
        "مبلغ": [100, 400, 100],
        "ماه": ["1405-03"] * 3,
        "روش تخصیص": ["مستقیم", "مساوی", "مستقیم"],
    })
    out = clean_data(raw)
    assert "ردیف" not in out.columns
    assert len(out) == 2  # the repeated row is gone
    assert set(out["allocation_type"]) == {"Direct", "Shared_Headcount"}
    assert set(out["period"]) == {"1405/03"}


def test_headcount_table_keeps_three_columns():
    raw = pd.DataFrame({"کد شرکت": [1], "شرکت": ["شرکت آلفا"], "تعداد نفرات": [10], "دوره": ["1405/03"]})
    out = clean_headcount_data(raw)
    assert list(out.columns) == ["company", "headcount", "period"]
    assert out.loc[0, "company"] == "Alpha company"
