import pandas as pd

from validator import check_period_consistency


def test_row_with_another_month_is_reported(capsys):
    df = pd.DataFrame({"company": list("ABC"), "period": ["1405/04", "1405/04", "1405/03"]})
    different = check_period_consistency(df)
    assert list(different["company"]) == ["C"]
    assert "different from the rest of the file (1405/04)" in capsys.readouterr().out


def test_consistent_file_gives_no_warning(capsys):
    df = pd.DataFrame({"company": list("AB"), "period": ["1405/03", "1405/03"]})
    assert check_period_consistency(df).empty
    assert capsys.readouterr().out == ""


def test_table_without_period_column_is_ignored():
    assert check_period_consistency(pd.DataFrame({"company": ["A"]})).empty
