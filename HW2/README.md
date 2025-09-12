# HW2 — SQL to CSV Export Pipeline

## What this does
- Runs every `.sql` file in `./sql` (in numeric order).
- Executes each SQL statement safely.
- Any `SELECT`/`SHOW` results are exported to CSV files in `./output` with headers.

## Setup
1. (Optional) Create and activate a virtualenv.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your DB credentials.

## Run
```bash
python main.py
```

After it runs, check the `output/` folder for CSV files like:

* `10_select_new_products_only.csv`
* `11_select_products_all.csv`
* `12_describe_products.csv`

**Notes**

* Assumes HW1 already created/populated the database.
* Change `DB_NAME` in `.env` if you need a different schema.
