import os, sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TEST_DIR, "..", "..", "src"))
RAW = os.path.join(TEST_DIR, "..", "..", "data", "raw")


from loader import load_excel
from validator import(validate_columns, check_missing_values, check_negative_amount)
from cleaner import clean_data
from aggregator import aggregate_cost_data




print("-------------test--------------")

files = [
    os.path.join(RAW, "01_خدمات_فناوری_خرداد_1405.xlsx"),
    os.path.join(RAW, "02_پشتیبانی_خرداد_1405.xlsx"),
    os.path.join(RAW, "04_خدمات_فناوری_تیر_1405.xlsx"),
    os.path.join(RAW, "05_پشتیبانی_تیر_1405.xlsx"),
]


cleaned_dataframes = []


for file in files:

    print("\nProcessing:")
    print(file)

    df = load_excel(file)

    print("Before cleaning:")
    print(df.columns.tolist())


    clean_df = clean_data(df)

    print("After cleaning:")
    print(clean_df.columns.tolist())

    print("Duplicate columns:")
    print(clean_df.columns[clean_df.columns.duplicated()].tolist())
    cleaned_dataframes.append(clean_df)



final_cost_df = aggregate_cost_data(
    cleaned_dataframes
)


print("\n========== FINAL DATASET ==========")

print(final_cost_df.head(20))

print("\nShape:")
print(final_cost_df.shape)

print("\nColumns:")
print(final_cost_df.columns.tolist())

print("\nAllocation Types:")
print(final_cost_df["allocation_type"].unique())

print("\nCompanies:")
print(final_cost_df["company"].unique())