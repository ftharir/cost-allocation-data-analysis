import os
from loader import load_excel
from cleaner import (
    clean_data,
    clean_headcount_data,
    handling_negative_amount,
    handling_nan_data
)
from aggregator import aggregate_cost_data
from allocator import allocate_costs
import pandas as pd
from exporter import export_to_excel

# Folder of the data, found relative to this file
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

# Cost Files

cost_files = [
    os.path.join(DATA_DIR, "raw", "01_خدمات_فناوری_خرداد_1405.xlsx"),
    os.path.join(DATA_DIR, "raw", "02_پشتیبانی_خرداد_1405.xlsx"),
    os.path.join(DATA_DIR, "raw", "04_خدمات_فناوری_تیر_1405.xlsx"),
    os.path.join(DATA_DIR, "raw", "05_پشتیبانی_تیر_1405.xlsx"),
]


cost_dfs = []


for file in cost_files:

    df = load_excel(file)

    clean_df = clean_data(df)
    cost_dfs.append(clean_df)


# Aggregate Cost Data

cost_dataset = aggregate_cost_data(
    cost_dfs
)




# Headcount Files

headcount_files = [
    os.path.join(DATA_DIR, "raw", "03_تعداد_نفرات_خرداد_1405.xlsx"),
    os.path.join(DATA_DIR, "raw", "06_تعداد_نفرات_تیر_1405.xlsx"),
]


headcount_dfs = []


for file in headcount_files:

    df = load_excel(file)

    clean_df = clean_headcount_data(df)

    headcount_dfs.append(clean_df)



headcount_dataset = aggregate_cost_data(
    headcount_dfs
)



 
# Allocation

final_dataset = allocate_costs(
    cost_dataset,
    headcount_dataset
)


pd.set_option(
    'display.float_format',
    '{:,.0f}'.format
)

print("Final Dataset:")
print(final_dataset)


print("\nShape:")
print(final_dataset.shape)

output_file = os.path.join(DATA_DIR, "processed", "Final_Cost_Report.xlsx")

export_to_excel(
    final_dataset,
    output_file
)