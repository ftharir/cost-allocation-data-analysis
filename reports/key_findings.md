# Key findings

All numbers come from the final report of the sample data (57 rows, 6 companies, two months). Amounts in million rial (M).

## 1. The total

* **6,504 M** were allocated: **2,933 M** in month 1 and **3,571 M** in month 2 (+22 %).
* The sum of the raw amounts is 7,272 M. Two corrections explain the difference to the final total: the repeated 780 M row is removed (-780 M) and a negative correction of 12 M is set to 0 (+12 M). Every other rial of the raw files is in the report (figure 08).

## 2. Who carries the cost

| Company | Total (M) | Share |
|---|---|---|
| Gamma | 2,236 | 34 % |
| Alpha | 1,621 | 25 % |
| Beta | 1,284 | 20 % |
| Delta | 890 | 14 % |
| Epsilon | 439 | 7 % |
| Omega | 33 | 1 % |

Gamma is the largest because of its direct costs: the three largest items of the report all belong to Gamma (a 780 M data-analysis project and the cloud infrastructure, 365 M and 372 M).

## 3. Direct and shared costs

* Month 1: direct 1,653 M, shared 1,280 M (**44 % shared**). Month 2: direct 2,206 M, shared 1,365 M (**38 % shared**).
* The shared share fell in month 2 only because the direct part grew (the 780 M project); the shared costs themselves grew by 7 %.
* The three biggest categories are shared office space (1,255 M), software licences (899 M) and the collaboration tool subscription (870 M).

## 4. The two big movements between the months

* **Gamma +106 %** (732 M to 1,505 M): the special 780 M data-analysis project of month 2. Without it Gamma would be roughly in line with the others.
* **Epsilon -87 %** (390 M to 49 M): this is **not a real fall**. In month 2 the security-licence amount of Epsilon is empty and its headcount is empty too, so it receives no share of the shared costs. The cost of Epsilon in month 2 is understated.
* Alpha +13 %, Delta +11 %, Beta +5 %: small growth that follows the headcount and the licence prices.

## 5. Shared costs follow the headcount

In both months the share of the shared cost of each company equals its share of the headcount (Alpha 29 % then 34 %, Gamma 22 % then 26 %, ...). This confirms the allocation rule works as designed, and shows its weak point: a company whose headcount is missing receives nothing.

## 6. Data quality of the inputs

* Problems in the raw files (figure 04): one missing amount and one repeated row in the IT file of month 2; one negative amount and one row with the wrong month in the support file of month 2; one missing headcount in month 2.
* Every company is written in 3 to 4 different ways across the files, and the column names differ in every file; the pipeline maps all of them to one standard.
* Month 2 has all the problems; month 1 has none. Controls on the input files would pay off most for the files that arrive late in the process.

## 7. What the numbers depend on

The decisions on negative corrections, missing headcounts and the "equal" allocation method change the report (see `docs/en/05_open_decisions.md`). With the decided rules, month 2 would show a lower cost for Gamma (the 12 M correction), a share of the shared costs for Epsilon and a different split of two shared costs worth 670 M.
