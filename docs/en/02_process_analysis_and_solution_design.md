# 02 - Process analysis and solution design

How the monthly cost allocation works today, where it hurts, what can be automated, and how the prototype is designed.

## 1. Current process

| Step | Activity | Responsible | Input | Output |
|---|---|---|---|---|
| Sending files | The units send their Excel files | people of the different units | - | the units' Excel files |
| Collecting files | Files are received on the 5th of the month; missing ones are chased | analyst | units' Excel files | units' Excel files |
| Checking files | Structure, completeness, correct month and latest version are checked | analyst | units' Excel files | sent back to the unit if there is a serious problem; otherwise the files go on |
| Fixing and cleaning data | Different company names, empty values and odd numbers are corrected | analyst | units' Excel files | corrected files |
| Aggregation | The data of all files is entered into one main file | analyst | corrected files | main file |
| Calculating costs | Shared costs are calculated with the headcount file | HR analyst | main file + headcount file from HR | main file with direct and shared costs |
| Final control | Totals and possible problems are checked | analyst | main file with direct and shared costs | checked main file |
| Manager approval | Unusual items are reviewed | manager | checked main file | final file approved by the manager |
| BI preparation | Data is prepared and the Power BI data is refreshed | analyst | approved final file | Power BI dashboard |

## 2. Problems and risks

| Process step | Problem | Risk | Effect |
|---|---|---|---|
| Collecting files | Chasing the files is manual | the follow-up is forgotten | the calculations start late |
| Checking files | the files do not have the same structure, so checking takes long | manual checking wastes time and energy | longer data preparation |
| Fixing and cleaning data | fixing the files is manual | human error and a lot of time | a wrong final file and longer preparation |
| Aggregation | aggregation is manual | human error | a wrong final file and longer preparation |
| Calculating costs | the allocation logic lives in the analyst's experience | if the analyst is not available the calculation is in trouble | dependence on one person; new staff need a long time |
| Final control | the final control is done manually by the analyst | human error | takes a lot of the analyst's time and energy |

## 3. Where a human decision is needed, and why

| Step | Human decision | Why a human is needed |
|---|---|---|
| Collecting files | chasing the units that did not send their file | following up with the units needs a person |
| Checking files | deciding whether a problem in a file can be fixed or the file must be sent back | the severity and whether it is solvable or acceptable need human judgement |
| Fixing and cleaning data | deciding whether an unusual value is an error or real data | the system must not guess a value; a person validates it |
| Manager approval | final approval | the final financial and management decision needs a person |

## 4. Business questions that must be answered

| Area | Question | Why it matters |
|---|---|---|
| Format of the final file | What exactly is the format of the final file? | to automate, the final template must be known |
| Company names | What is the official list of company names, their similar spellings and the standard value? | to build the company-name mapping |
| Version control | If a unit sends several versions, what is the rule for choosing one (date sent, or confirmation by the unit, which needs a human)? | to avoid processing the wrong version |
| Data correction | How is an unusual amount defined? What is its range? | to know when an amount goes to a human for review |
| Data correction | Is the "equal" allocation method calculated differently from the shared method? (for now it is treated as shared) | important for the cost of each company |

## 5. Future process

| Step | Proposed activity | Done by | Note |
|---|---|---|---|
| Collecting files | the analyst manually checks whether the files were sent | human | |
| Checking files | check structure, completeness, correct month and latest version; the system also handles empty, negative or unusual values | automation first, then a human | the columns must be the right ones; at the end a person confirms there is no serious problem |
| Fixing and cleaning data | if a company name or a column name is wrong, mapping corrects it | automation first, then a human | the system works first; the human checks wrong column names and handles the empty values the system warns about |
| Aggregation | the system moves the data of the Excel files to the final file format | automation | |
| Calculating costs | direct costs are summed; shared costs are divided with the headcount file and the final amount results | automation | |
| Final control | the human does the final control | human | unusual amounts and unknown companies were already checked by the system and a person, so this should be short: one last check before it goes to the manager |
| Manager approval | final review by the manager | human | |
| Final dataset for BI | dataset ready for BI | automation | |

**Automated:** reading and first checks of the files; correcting and validating the data; standardising the structure; first cleaning; aggregation; allocation of costs; producing the final dataset for the dashboard.

**Left to humans:** confirming company names; deciding on unusual data; the manager's approval.

## 6. Scope of the prototype

| Process part | Implemented in the prototype? | Description |
|---|---|---|
| Receiving and reading files | yes | reading the sample input files |
| Checking files | yes | check the structure; the system also handles empty, negative or unusual values |
| Fixing and cleaning data | yes | wrong company names and column names are mapped |
| Aggregation | yes | the Excel data is moved to the final file format |
| Calculating costs | yes | |
| Final control | no | |
| Manager approval | no | |
| Final dataset for BI | yes | output usable for BI |

## 7. Pipeline flow

![Pipeline flow](../assets/pipeline_flow.png)

1. **Reading the files** - input: the sample files (IT services, support, headcount); the Excel files are read; output: first data frames.
2. **Checking the files** - input validation: is the structure right, do the required columns exist, are there problem values (empty, negative or unusual amounts); output: valid data plus warnings for the problem parts.
3. **Fixing and cleaning the data** - cleaning and transformation: standardising column names and company names; output: data ready for processing.
4. **Aggregation** - the processed data is combined into one dataset.
5. **Calculating the costs** - direct costs are summed directly; shared costs use the headcount file; output: the cost allocated to each company.
6. **Producing the final dataset for BI** - the final output that is later loaded into Power BI.

## 8. Input and output

**Input** - Excel files: IT-services cost files, support cost files and the headcount file. They contain the cost data and the information needed to allocate the shared costs.

**Output** - one final dataset for reporting and Power BI with: company, period, cost type, allocated amount, and allocation type (direct / shared).

## 9. Business rules

**Rule 1 - Direct cost allocation.** If `Allocation Type = Direct`, the cost stays with its company: `Allocated Company = Original Company`, `Allocated Amount = Original Amount`.
*Example:* input `Company: Alpha, Amount: 1,000,000, Type: Direct` gives `Company: Alpha, Allocated Amount: 1,000,000`.

**Rule 2 - Shared cost allocation.** If `Allocation Type = Shared`, the system finds the total headcount of the companies and divides the cost with
`Cost ÷ Total Headcount × Company Headcount`.

**Rule 3 - Company-name standardisation.** Names such as `Alpha`, `آلفا`, `شرکت آلفا` are mapped to one standard name. This is a plain mapping service, **not an intelligent one**, so a human must check afterwards because a name may still be wrong. In later phases an AI or fuzzy-matching service can be added to detect and correct a wider range of mistakes.

**Rule 4 - Data validation.** In the correction and validation step, if there is a missing value, a negative amount or an unknown company, then `Status = Warning` and a human review follows.

## 10. Code structure

```
src/
├── main.py
├── loader.py
├── validator.py
├── cleaner.py
├── aggregator.py
├── allocator.py
└── exporter.py
```

| File | Description |
|---|---|
| `main.py` | runs the main pipeline |
| `loader.py` | reads the input Excel files |
| `validator.py` | checks the structure and quality of the data |
| `cleaner.py` | standardises and cleans the data |
| `aggregator.py` | combines the processed data |
| `allocator.py` | calculates and allocates the costs |
| `exporter.py` | produces the final dataset |

The code and its outputs can still be improved; that was outside the scope of this task.
