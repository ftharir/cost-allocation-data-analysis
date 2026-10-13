# 04 - Data dictionary and mappings

Every rule that turns the raw Excel files into one standard dataset. The mappings live in [`src/cleaner.py`](../../src/cleaner.py); this page lists them in one place. (In a production version they should move to configuration / master data, see [`03_production_improvements.md`](03_production_improvements.md).)

## 1. Standard columns of the cleaned cost data

| Column | Meaning |
|---|---|
| `company` | the company the cost belongs to (`ALL` for a shared cost) |
| `cost_title` | what the cost is for |
| `amount` | amount in rial |
| `period` | month, always written `YYYY/MM` (Jalali), for example `1405/03` |
| `allocation_type` | `Direct` or `Shared_Headcount` |
| `description`, `reference` | free text and a tracking code or cost centre (kept, not used in the calculation) |

Headcount data has `company`, `headcount` and `period`.

## 2. Column names that are mapped

| Standard column | Names found in the files |
|---|---|
| `company` | `نام شرکت`, `شرکت`, `Company`, `Company Name` |
| `amount` | `مبلغ`, `مبلغ (ریال)`, `Amount (Rial)` |
| `cost_title` | `شرح خدمت`, `نوع خدمت`, `عنوان هزینه`, `Cost Title` |
| `description` | `شرح`, `توضیحات` |
| `period` | `ماه`, `دوره`, `Period`, `Month` |
| `allocation_type` | `روش تخصیص`, `نحوه تخصیص`, `مبنای تسهیم`, `Allocation Basis` |
| `reference` | `Reference`, `کد پیگیری`, `مرکز هزینه` |
| `headcount` | `تعداد نفرات`, `Headcount` |

Columns removed because they only number the rows or give a status: `ردیف`, `شماره`, `وضعیت`.

## 3. Company names

| Standard name | Spellings mapped to it |
|---|---|
| `Alpha company` | `Alpha`, `آلفا`, `شرکت آلفا`, `Alpha Co` |
| `Beta company` | `بتا`, `شرکت بتا`, `Beta Co` |
| `Gamma company` | `Gamma Co`, `گاما`, `شرکت گاما` |
| `Delta company` | `دلتا`, `شرکت دلتا`, `Delta Co` |
| `Epsilon company` | `Epsilon`, `اپسیلون`, `شرکت اپسیلون` |
| `Omega company` | `شرکت امگا` (not in the headcount list, so it receives no shared cost) |
| `ALL` | `همه`, `همه شرکت‌ها` |

## 4. Allocation type

| Standard value | Values mapped to it |
|---|---|
| `Direct` | `مستقیم`, `Direct` |
| `Shared_Headcount` | `مشترک`, `Headcount`, `تعداد نفرات`, `مساوی`, `Equal` |

`مساوی` / `Equal` (equal split) is treated like the headcount split for now; see the open decisions.

## 5. Cost titles

| Standard title | Values mapped to it |
|---|---|
| `Software License` | `لایسنس نرم‌افزار` |
| `Cloud Infrastructure` | `زیرساخت ابری` |
| `System Support` | `پشتیبانی سامانه` |
| `Security License` | `لایسنس امنیتی` |
| `Storage` | `فضای ذخیره‌سازی` |
| `Monitoring Service` | `خدمات مانیتورینگ` |
| `Collaboration Tool Subscription` | `اشتراک ابزار همکاری` |
| `Data Analysis Service` | `خدمات تحلیل داده` |
| `Shared Office Space` | `فضای اداری مشترک`, `Shared Office` |
| `General Support` | `پشتیبانی عمومی` |
| `Courier` | `پیک و ارسال` |
| `Printing Service` | `خدمات چاپ` |
| `Catering Service` | `خدمات پذیرایی` |
| `Office Supplies` | `لوازم اداری` |
| `Repair Service` | `تعمیرات`, `Facility Repair` |

## 6. Value rules

| Situation | Rule |
|---|---|
| Period written `1405-03` | becomes `1405/03` |
| Missing number (amount or headcount) | 0, with a warning |
| Negative amount | 0, with a warning that shows the record |
| Row identical to another row (after removing the row-number columns) | kept once, with a warning |
| Row whose period differs from the rest of its file | kept, with a warning that shows the row |
| Direct cost | stays with its company |
| Shared cost | `cost ÷ total headcount of the month × company headcount` |
