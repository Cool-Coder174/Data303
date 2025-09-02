# HW1 — Observations Report

## Scope I completed
I worked through **Exercise 1.01**, **Exercise 1.02**, and **Activity 1.01** from *The SQL Workshop* Chapter 1 (SQL Basics). These cover creating the `PACKT_ONLINE_SHOP` database and tables, inserting rows into `Customers`, and then populating a `Products` table from a spreadsheet.

---

## What I learned

1. **How to set up a database and tables**
   - I learned the basic flow: `CREATE DATABASE`, `USE <db>`, then `CREATE TABLE` with appropriate data types and keys. The chapter’s Student/Customers examples helped me reason about types (for example, when to use `VARCHAR`, `CHAR`, `INT`) and how/why to define a `PRIMARY KEY`.
   - I also learned to verify results in MySQL Workbench by right-clicking the table and choosing **Select Rows – Limit 1000** to confirm my schema/rows are actually there.

2. **How to insert data (single and multi-row)**
   - I practiced `INSERT INTO ... VALUES (...)` and switching databases with `USE` before running inserts so rows land in the correct schema.
   - I learned that blanks in the provided sheet should be inserted as `NULL` (not empty strings), and that multi-row inserts are efficient for loading several records at once.

3. **How to follow a data-from-spreadsheet workflow**
   - For **Exercise 1.02**, I used the given customer spreadsheet/CSV to compose a single multi-row `INSERT` for the `Customers` table, using `NULL` where appropriate.
   - For **Activity 1.01**, I created a `Products` table mirroring the sheet’s columns, then inserted the rows from that dataset.

---

## Challenges I encountered

1. **Choosing correct data types and lengths**
   - Deciding column types/lengths (e.g., `VARCHAR(50)` vs `VARCHAR(30)`) was a little tricky without over- or under-allocating. The Student table example clarified how to map real values to sensible types and sizes.

2. **Handling `NULL` vs empty strings**
   - The source sheet had blanks; I needed to be intentional about inserting `NULL` instead of `''`, per the exercise instructions.

3. **Case/typo issues with database names**
   - Switching between `PACKT_ONLINE_SHOP`/`packt_online_shop` required me to be consistent with `USE` so statements targeted the right database. The book’s examples reminded me to explicitly run `USE` before inserts.

4. **Validating that data actually loaded**
   - After inserting, I wasn’t 100% sure it worked until I used the Workbench “Select Rows – Limit 1000” view to confirm.

---

## How I solved those challenges

1. **Types & lengths:** I referenced the chapter’s examples (Student/Customers) to pick types that match expected values and to define a clear `PRIMARY KEY`. This guided consistent column sizing and constraints.  
2. **`NULL` handling:** I followed the exercise’s direction to map empty cells to `NULL` directly in the `INSERT` statements.  
3. **Correct schema selection:** I prefixed inserts with `USE PACKT_ONLINE_SHOP;` so all subsequent statements ran against the intended database.  
4. **Verification:** I used the Workbench result grid to visually confirm table structure and rows after each step.

---

## Quick reflection
These tasks gave me a clean, end-to-end picture of early SQL workflows: define a schema, create tables with types and keys, load real-world data from a sheet (including blanks → `NULL`), and verify results. It set a solid foundation for later chapters on updating, querying, and joining data.

---

## Screenshots attached
- Screenshots are located under `assets` folder in repo 
- `Customers` after the multi-row insert.  
- `Products` after populating the table per the activity steps.

