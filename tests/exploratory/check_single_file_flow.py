import os, sys
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(TEST_DIR, "..", "..", "src"))
RAW = os.path.join(TEST_DIR, "..", "..", "data", "raw")

from loader import load_excel
from validator import(validate_columns, check_missing_values, check_negative_amount)
from cleaner import clean_data
from aggregator import aggregate_cost_data


# text loader
file_path = os.path.join(RAW, "01_خدمات_فناوری_خرداد_1405.xlsx")
df = load_excel(file_path=file_path)

it_file = os.path.join(RAW, "01_خدمات_فناوری_خرداد_1405.xlsx")
df_it = load_excel(it_file)

support_file = os.path.join(RAW, "02_پشتیبانی_خرداد_1405.xlsx")
df_support = load_excel(support_file)


print(df.head())
print("-------------")
print(df.info())


# test validator
print("-------------")
required_columns = ["ردیف","نام شرکت", "شرح خدمت", "مبلغ", "ماه", "روش تخصیص", "توضیحات" ]
Missing_columns = validate_columns(df, required_columns=required_columns)
print(f"Missing Columns: {Missing_columns}")

Missing_Values = check_missing_values(df=df)
print(f"\nMissing Values: {Missing_Values}")

Negative_amount = check_negative_amount(df=df, amount_column="مبلغ")
print(f"\nNegative amount: {Negative_amount}")


# test cleaner
print("-------------")
clean_df = clean_data(df)
print("clean data")
print(clean_df.columns)
print(clean_df.head())

df_it = clean_data(df=df_it)
df_support = clean_data(df=df_support)

#test aggregator 
# قبل از این مرحله باید استاندارد سازی کامل انجام شده باشه برای ستون ها
cost_dataset = aggregate_cost_data([
    df_it,
    df_support
])

print("-------------")
print("finall df:")
print(cost_dataset.head(100))
print(cost_dataset.shape)













