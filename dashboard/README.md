# Power BI dashboard

`Cost_Allocation_Dashboard.pbix` reads the final dataset (`data/processed/Final_Cost_Report.xlsx`) and shows it on one page (1280 x 720).

| Visual | Type | Fields |
|---|---|---|
| Total cost | card | `Total Cost` (sum of `allocated_amount`) |
| Number of companies | card | `Company Count` |
| Number of cost types | card | `Cost Type Count` |
| Total cost per company | clustered bar chart | `company`, `Total Cost` |
| **Direct vs Shared Cost** | donut chart | `allocation_type`, `Total Cost` |
| **Monthly Cost Trend** | line chart | `period`, `Total Cost` |
| **Monthly Cost by Company** | clustered column chart | `company`, `Total Cost`, series `period` |
| notes | text box | |

To refresh it after a new run: open the file in Power BI Desktop, point the data source at the new `Final_Cost_Report.xlsx` and choose *Refresh*.
