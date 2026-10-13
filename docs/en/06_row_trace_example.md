# 06 - Following one row from the raw file to the final report

Two real rows of the sample data, step by step. They show what every module of the pipeline does.

![Architecture](../assets/architecture.png)

## Example 1 - a shared cost (`05_پشتیبانی_تیر_1405.xlsx`)

**Raw row**

| نام شرکت | عنوان هزینه | مبلغ | ماه | مبنای تسهیم | کد پیگیری | وضعیت |
|---|---|---|---|---|---|---|
| همه شرکت‌ها | فضای اداری مشترک | 645,000,000 | 1405/04 | تعداد نفرات | SUP-0406 | ثبت‌شده |

| Step | Module | What happens to the row |
|---|---|---|
| 1 | `loader.py` | the sheet is read into a table |
| 2 | `cleaner.py` | the columns get standard names (`company`, `cost_title`, `amount`, `period`, `allocation_type`, `reference`); the status column is dropped |
| 3 | `cleaner.py` | `همه شرکت‌ها` becomes `ALL`; `فضای اداری مشترک` becomes `Shared Office Space`; `تعداد نفرات` becomes `Shared_Headcount` |
| 4 | `validator.py` | nothing to report (no zero, negative or other-month value) |
| 5 | `aggregator.py` | the row joins the cost rows of the other files |
| 6 | `allocator.py` | the cost is split with the headcount of month `1405/04` (file `06_تعداد_نفرات_تیر_1405.xlsx`) |
| 7 | `exporter.py` | five rows, one per company, are written to `Final_Cost_Report.xlsx` |

**The split.** Headcount of `1405/04`: Alpha 131, Beta 87, Gamma 101, Delta 72, Epsilon missing (counted as 0), total 391.
Allocated amount = `645,000,000 × company headcount ÷ 391`:

| Company | Headcount | Allocated amount (rial) |
|---|---|---|
| Alpha | 131 | 216,099,744 |
| Beta | 87 | 143,516,624 |
| Gamma | 101 | 166,611,253 |
| Delta | 72 | 118,772,379 |
| Epsilon | 0 | 0 |
| **Total** | 391 | **645,000,000** |

The five rows add up to the original amount, so nothing is lost or created (`tests/test_pipeline.py` checks this for the whole dataset).

## Example 2 - a negative correction (`05_پشتیبانی_تیر_1405.xlsx`)

**Raw row**

| نام شرکت | عنوان هزینه | مبلغ | ماه | مبنای تسهیم | کد پیگیری | وضعیت |
|---|---|---|---|---|---|---|
| شرکت گاما | تعمیرات | -12,000,000 | 1405/04 | مستقیم | SUP-0403 | اصلاحیه |

| Step | Module | What happens to the row |
|---|---|---|
| 1-2 | `loader.py`, `cleaner.py` | read; columns standardised; `شرکت گاما` becomes `Gamma company`, `تعمیرات` becomes `Repair Service`, `مستقیم` becomes `Direct` |
| 3 | `validator.py`, `cleaner.py` | a warning shows the record: *Negative values found in column 'amount'*; the amount is replaced by 0 |
| 4 | `allocator.py` | a direct cost stays with its company |

**Final row:** `Gamma company | Repair Service | 1405/04 | Direct | SUP-0403 | 0`.

The status `اصلاحیه` (correction) shows that this negative amount is probably not an error but a correction that should **reduce** the cost; the prototype sets it to 0 and reports it. For production it is decided to keep the sign and reduce the cost ([05](05_open_decisions.md)); the prototype does not do this yet.
