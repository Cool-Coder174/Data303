# HW2 — Exercise 2.01: EMPLOYEE DB (One-Row INSERT)

## What this does
- Creates an `EMPLOYEE` database, a simple `Employees` table, inserts **one** row, and displays the contents.
- Runs each `.sql` in `./sql` (numeric order).
- Any `SELECT`/`SHOW` results are exported to CSV in `./output` with headers.

## Setup
1. (Optional) Create/activate a virtualenv.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill DB creds. You can leave `DB_NAME` empty; scripts run `USE EMPLOYEE;`.

## Run
```bash
python main.py
````

After it runs, check `output/` for CSVs like:

* `10_select_all_employees.csv`
* `11_describe_employees.csv`

**Notes**

* This implements **Exercise 2.01** (create DB/table, single-row INSERT, display).
* If you prefer connecting directly to the DB, set `DB_NAME=EMPLOYEE` in `.env` after the first run.