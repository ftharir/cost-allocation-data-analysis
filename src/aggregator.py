# اینجا همه فایل ها غیر فایل هدکنت رو ادد میکنیم که همه جمع بشن اتومات کردن کاری که کراشناس انجام میداد همه فایل ها رو در فایل نهایی ذخیره میکرد
import pandas as pd 

def aggregate_cost_data(dfs):
    #  Combine multiple cost DataFrames into one dataset
    cost_dataset = pd.concat(dfs, ignore_index=True)

    return cost_dataset