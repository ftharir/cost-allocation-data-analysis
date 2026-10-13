# 05 - Business decisions

The prototype had to make assumptions where the business rule was not defined. This page lists each one, what the code does today and the decision (or proposal) for a production version.

**The prototype code is unchanged by these decisions.** A decision marked *decided* is the rule to implement in the production version; the sample report in `data/processed` still follows the prototype behaviour in the "today" column.

| # | Question | What the prototype does today | Decision / proposal for production | Status |
|---|---|---|---|---|
| 1 | A **negative amount**, for example the correction `-12,000,000` (its status column says `اصلاحیه`, "correction") | warns, shows the record, sets it to 0 | keep the sign: a negative amount marked as a correction **reduces** the cost and is reported; a negative amount without that status stops the run for a person to decide | **decided** |
| 2 | A **missing headcount** (Epsilon in month 2) | treated as 0, so the company gets no shared cost that month | use the company's **last known headcount** (Epsilon had 59 in month 1) and raise a warning; if there is none, stop | **decided** |
| 3 | The **"equal" allocation method** (`مساوی` / `Equal`) | treated like the headcount split | split **equally** between the companies that have a headcount record; keep it as its own allocation type, separate from the headcount split | **decided** |
| 4 | A **missing amount** | warns, sets it to 0 | stop and ask the unit for the value | proposal |
| 5 | An **unknown company** (such as `Omega`) | kept as its own company; its direct cost is reported, it gets no shared cost | add it to the official company list, or reject the row | proposal |
| 6 | An **unusual amount** | not detected | define the threshold (percentage change against the previous month) | proposal |
| 7 | The **same record entered twice** | the repeated row is removed with a warning | keep the rule, and report every removed row in a log | proposal |
| 8 | A row with the **month of another period** | kept, with a warning | reject it or ask the unit | proposal |
| 9 | **Several versions of a file** from one unit | not handled | define the rule (latest date, or confirmed by the unit) | proposal |
| 10 | **Who approves** data-quality exceptions | no workflow | name the approver and record the approval | proposal |

## What the decided rules would change

With the sample data, applying decisions 1 to 3 would change the report for month 2: Gamma's repair correction of -12,000,000 would reduce its cost; Epsilon would receive a share of the shared costs based on 59 people; and the two "equal" costs (420,000,000 and 250,000,000 for the collaboration tool and general support) would be split equally between the companies instead of by headcount. The decisions are recorded here and are not applied in the prototype.
