# 01 - Data understanding

Review of the six sample input files: their structure, columns and data quality. The pipeline in `src/` was designed from these findings.

## Overview

| # | File | Cost type | Month | Sheet | Columns | Records | Data quality |
|---|---|---|---|---|---|---|---|
| 01 | `01_خدمات_فناوری_خرداد_1405.xlsx` | IT services | Khordad 1405 | `هزینه‌ها` | 7 | 8 | missing values; company-name problem |
| 02 | `02_پشتیبانی_خرداد_1405.xlsx` | Support | Khordad 1405 | `Data` | 6 | 7 | company names are not in one language |
| 03 | `03_تعداد_نفرات_خرداد_1405.xlsx` | Headcount | Khordad 1405 | `Headcount` | 4 | 5 | no problems |
| 04 | `04_خدمات_فناوری_تیر_1405.xlsx` | IT services | Tir 1405 | `گزارش تیر` | 8 | 10 | company-name problem; missing values |
| 05 | `05_پشتیبانی_تیر_1405.xlsx` | Support | Tir 1405 | `گزارش` | 7 | 9 | wrong (negative) value; company-name problem |
| 06 | `06_تعداد_نفرات_تیر_1405.xlsx` | Headcount | Tir 1405 | `HC` | 5 | 5 | missing value; company names not uniform |

(Khordad 1405 = period `1405/03`, Tir 1405 = period `1405/04`.)

## Columns of each file

| File | Columns |
|---|---|
| 01 IT, Khordad | row number, company name, service description, amount, month, allocation method, remarks |
| 02 Support, Khordad | Company, Cost Title, Amount (Rial), Period, Allocation Basis, Reference |
| 03 Headcount, Khordad | company code, company, headcount, period |
| 04 IT, Tir | number, company, service type, amount (rial), period, allocation method, cost centre, description |
| 05 Support, Tir | company name, cost title, amount, month, allocation basis, tracking code, status |
| 06 Headcount, Tir | Company ID, Company Name, Headcount, Month, Updated At |

## Findings

* **Different column names** for the same meaning (for example company: `نام شرکت`, `شرکت`, `Company`, `Company Name`; amount: `مبلغ`, `مبلغ (ریال)`, `Amount (Rial)`), and a different number and order of columns in every file.
* **The same company is written in several ways** (Persian, English, with or without "شرکت"/"Co"), and "all companies" appears as `همه`, `همه شرکت‌ها` and `ALL`.
* **Different values for the allocation method** (`مستقیم`/`Direct`, `مشترک`/`Headcount`/`تعداد نفرات`, `مساوی`/`Equal`).
* **Data-quality problems** noted in the original review: an empty amount, a negative amount (a correction), company names that are not uniform, and a missing headcount.
* **Found later, while building and testing the pipeline:** the same record entered twice in the IT file of month 2, and one record in the support file of month 2 that carries the month of the previous period; an unknown company (`Omega`) that is not in the headcount list.
* The headcount files are the only source for the shared-cost split; the headcount of one company is missing in month 2.

The data-quality counts per file are shown in `reports/figures/04_data_quality_issues.png`.
