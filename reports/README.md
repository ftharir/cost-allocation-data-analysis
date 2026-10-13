# Reports

Data analysis results: charts and tables made from the final dataset (`data/processed/Final_Cost_Report.xlsx`) and the raw files. The written analysis is in [`key_findings.md`](key_findings.md) (English) and [`key_findings_fa.md`](key_findings_fa.md) (Persian).

Amounts are in rial; "million rial" is written M. Month 1 is Khordad 1405 (`1405/03`), month 2 is Tir 1405 (`1405/04`).

## Figures

| # | Figure | What it shows |
|---|---|---|
| 01 | [`01_cost_per_company_and_month.png`](figures/01_cost_per_company_and_month.png) | For each month, the cost of every company split into its direct part and its share of the shared costs |
| 02 | [`02_shared_cost_vs_headcount.png`](figures/02_shared_cost_vs_headcount.png) | Share of the headcount against share of the shared cost: the two are the same, because shared costs follow the headcount (Epsilon has no headcount in month 2) |
| 03 | [`03_cost_per_category.png`](figures/03_cost_per_category.png) | Total cost of each category over both months |
| 04 | [`04_data_quality_issues.png`](figures/04_data_quality_issues.png) | Rows with a data problem in each of the six raw files |
| 05 | [`05_total_cost_per_company.png`](figures/05_total_cost_per_company.png) | Total allocated cost per company and its share of everything |
| 06 | [`06_change_between_months.png`](figures/06_change_between_months.png) | Change of every company from month 1 to month 2, with the reason for the two big changes |
| 07 | [`07_ten_largest_items.png`](figures/07_ten_largest_items.png) | The ten largest items of the report (direct costs and shares of shared costs) |
| 08 | [`08_raw_to_final_reconciliation.png`](figures/08_raw_to_final_reconciliation.png) | How the sum of the raw amounts (7,272 M) becomes the final total (6,504 M) |

## Tables (`tables/`)

| File | Content |
|---|---|
| `cost_by_company_and_month.csv` | allocated cost of every company in each month, the total and the change between the months |
| `direct_vs_shared_by_month.csv` | direct and shared cost per month and the share of the shared cost |
| `cost_by_category.csv` | total cost per category |
| `shared_cost_vs_headcount.csv` | headcount, headcount share, shared cost and its share per company and month |
| `ten_largest_items.csv` | the ten largest rows of the final report |
| `reconciliation_raw_to_final.csv` | the steps from the raw total to the final total |

The numbers in every table can be reproduced from `data/processed/Final_Cost_Report.xlsx` (for the reconciliation, also from `data/raw`).
