import os, sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TEST_DIR, "..", "..", "src"))
RAW = os.path.join(TEST_DIR, "..", "..", "data", "raw")

from loader import load_excel
from cleaner import clean_headcount_data, handling_nan_data, handling_negative_amount
from validator import(validate_columns, check_missing_values, check_negative_amount)


files = [
    os.path.join(RAW, "03_تعداد_نفرات_خرداد_1405.xlsx"),
    os.path.join(RAW, "06_تعداد_نفرات_تیر_1405.xlsx")
]


for file in files:
    print("\nFILE:")
    print(file)

    df = load_excel(file)
    clean_df = clean_headcount_data(df)

    clean_df = handling_nan_data(clean_df)
    clean_df = handling_negative_amount(clean_df)

    

    print(clean_df)

