# اصلاح و cleaning  داده
#  data cleaning & Transformation

# توجه: ستون ها مپینگشون رو کامل کنم تمامی اسامی رو وارد کنم 

from validator import validate_numeric_values, check_period_consistency

def standardize_columns(df):
    # rename column names to standardard name

    column_mapping = {

    # Company
    "نام شرکت": "company",
    "شرکت": "company",
    "Company": "company",
    "Company Name": "company",

    # Amount
    "مبلغ": "amount",
    "مبلغ (ریال)": "amount",
    "Amount (Rial)": "amount",

    # Cost Description
    "شرح خدمت": "cost_title",
    "نوع خدمت": "cost_title",
    "عنوان هزینه": "cost_title",
    "Cost Title": "cost_title",
    "شرح": "description",

    # Period
    "ماه": "period",
    "دوره": "period",
    "Period": "period",
    "Month" : "period",

    # Allocation
    "روش تخصیص": "allocation_type",
    "نحوه تخصیص": "allocation_type",
    "مبنای تسهیم": "allocation_type",
    "Allocation Basis": "allocation_type",

    #Reference
    "Reference": "reference",
    "Reference": "reference",
    "کد پیگیری": "reference",
    "توضیحات": "description",
    "مرکز هزینه" : "reference",

    "Company Name": "company",
    "تعداد نفرات": "headcount",
    "Headcount": "headcount",
    "Reference": "reference",
    "reference": "reference",


    }

    df = df.rename(columns = column_mapping)
    return df 


def standardize_company_names(df):
    # Standardize company value's column using mapping

    company_mapping = {
        "Alpha": "Alpha company",
        "آلفا": "Alpha company",
        "شرکت آلفا": "Alpha company",
        "Alpha Co": "Alpha company",
        "Gamma Co": "Gamma company",
        "گاما": "Gamma company",
        "گاما": "Gamma company",
        "شرکت گاما" : "Gamma company",
        "شرکت امگا": "Omega company",
        "دلتا": "Delta company",
        "شرکت دلتا": "Delta company",
        "Delta Co": "Delta company",
        "Epsilon": "Epsilon company",
        "اپسیلون": "Epsilon company",
        "شرکت اپسیلون" : "Epsilon company",
        "بتا": "Beta company", 
        "شرکت بتا":"Beta company", 
        "Beta Co": "Beta company", 
        "همه": "ALL",
        "همه شرکت‌ها": "ALL"
    }

    if "company" in df.columns:
        df["company"] = df["company"].replace(company_mapping)


    return df 

def standardize_allocation_type(df):

    # Standardize allocation_type value's column using mapping

    allocation_mapping = {

    # Direct
    "مستقیم": "Direct",
    "Direct": "Direct",

    # Shared by Headcount
    "مشترک": "Shared_Headcount",
    "Headcount": "Shared_Headcount",
    "تعداد نفرات": "Shared_Headcount",

    # Shared equally - ایا نوع محاسبه دیگری دارد؟
    "مساوی": "Shared_Headcount",
    "Equal": "Shared_Headcount"
}

    if "allocation_type" in df.columns:
        df["allocation_type"]= (
            df["allocation_type"].replace(allocation_mapping)
        )
    return df


def standardize_period(df):

    if "period" in df.columns:
        df["period"] = (
            df["period"].astype(str).str.replace("-", "/")
        )

    return df


def standardize_cost_title(df):

    cost_title_mapping = {

    "لایسنس نرم‌افزار": "Software License",

    "زیرساخت ابری": "Cloud Infrastructure",

    "پشتیبانی سامانه": "System Support",

    "لایسنس امنیتی": "Security License",

    "فضای ذخیره‌سازی": "Storage",

    "خدمات مانیتورینگ": "Monitoring Service",

    "اشتراک ابزار همکاری": "Collaboration Tool Subscription",

    "خدمات تحلیل داده": "Data Analysis Service",

    "فضای اداری مشترک": "Shared Office Space",

    "پشتیبانی عمومی": "General Support",

    "پیک و ارسال": "Courier",

    "خدمات چاپ": "Printing Service",

    "خدمات پذیرایی": "Catering Service",

    "لوازم اداری": "Office Supplies",

    "تعمیرات": "Repair Service",

    "Shared Office": "Shared Office Space",

    "Facility Repair": "Repair Service"

}

    if "cost_title" in df.columns:
        df["cost_title"] = (
            df["cost_title"]
            .replace(cost_title_mapping)
        )

    return df


def remove_unnecessary_columns(df):

    columns_to_remove = [
        "ردیف",
        "شماره",
        "وضعیت"
    ]

    df = df.drop(columns=columns_to_remove,errors="ignore")

    return df



def remove_duplicate_rows(df):

    # rows that are identical in every column (after the row-number columns were removed)
    # are the same record entered twice; keep only the first one
    before = len(df)
    df = df.drop_duplicates()

    if len(df) < before:
        print(f"Warning: {before - len(df)} duplicate row(s) removed.")

    return df


def standardize_headcount_columns(df):

    column_mapping = {

        "شرکت": "company",
        "Company Name": "company",

        "تعداد نفرات": "headcount",
        "Headcount": "headcount",

        "دوره": "period",
        "Month": "period"
    }


    df = df.rename(columns=column_mapping)

    return df

def handling_nan_data(df):
    #Replace all missing values (NaN) with 0

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    df[numeric_columns] = (
        df[numeric_columns]
        .fillna(0)
    )

    return df


def handling_negative_amount(df):

    if "amount" not in df.columns:
        return df


    negative_values = df[
        df["amount"] < 0
    ]

    if not negative_values.empty:
        print("Warning: Negative amount:")
        print(negative_values)
        print("for now we changed negative amount to 0, please reassign the value.")


    df.loc[
        df["amount"] < 0,
        "amount"
    ] = 0


    return df

# clean cost data
def clean_data(df):
    df = standardize_columns(df)
    df = standardize_company_names(df)
    df = standardize_allocation_type(df)
    df = standardize_period(df)
    check_period_consistency(df)
    df = remove_unnecessary_columns(df)
    df = remove_duplicate_rows(df)
    df = standardize_cost_title(df)
    validate_numeric_values(df)
    df = handling_negative_amount(df)
    df = handling_nan_data(df)

    return df 





# clean headcount data
def clean_headcount_data(df):

    df = standardize_headcount_columns(df)
    df = standardize_columns(df)
    df = standardize_company_names(df)
    validate_numeric_values(df)
    df = handling_negative_amount(df)
    df = handling_nan_data(df)

    return df[
        [
            "company",
            "headcount",
            "period"
        ]
    ]