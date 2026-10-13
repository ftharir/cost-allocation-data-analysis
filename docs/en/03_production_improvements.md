# 03 - From prototype to a monthly production process

> What is missing in the current prototype, and what has to change to make it a reliable monthly process?

## 1. A defined input format and schema validation

The first requirement is a fixed format that every unit uses when it sends its file, together with **schema validation** to manage company names and the values of the columns more reliably.
An AI component could help here and reduce how often a person has to check. However much mapping is done, and even with fuzzy matching, a wrong value or name can still get into a file, so the format has to be enforced at the source as well.

## 2. Handling invalid values

In the prototype, for negative or missing (NaN) numbers the system prints a warning, shows the record and then treats the value as 0. In a real project this is wrong: **the system must not guess**. It is better to stop the program completely until a person decides what the negative or missing value should be.

* For columns that are not required in the calculation, such as `description` or `reference`, a NaN does not affect the numbers.
* It must be decided whether the output really needs these columns. If it does, they must not be NaN and should even be shown in the dashboard; if not, the columns can be removed.

## 3. Configuration and master data

Today the knowledge (mappings and rules) lives in the code. In a real version, **the company mappings, the allocation rules and the validation rules should be kept as configuration / master data**. Then adding a company or changing a rule does not require someone to extract the logic from an expert's head, and not necessarily a change in the code.

## 4. Logging and traceability

A real version needs more attention to logging: which files were processed, which errors occurred, which version was used, and how each cost was assigned.

## 5. Minimal human intervention

The final pipeline should need as little human intervention as possible. Not everything has to be automated, but the human effort can be reduced as much as possible.

## Summary of improvements

| Area | Prototype today | Production version |
|---|---|---|
| Input | files in any structure | one defined format, schema validation |
| Invalid values | warning, then replaced by 0 | stop and ask a person to decide |
| Rules and mappings | inside the code | configuration / master data |
| Traceability | printed warnings | logs of files, errors, versions and assignments |
| Human work | many manual steps | only approvals and decisions on exceptions |
