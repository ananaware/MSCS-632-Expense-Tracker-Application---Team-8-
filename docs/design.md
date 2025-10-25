# Expense Tracker — Design & Plan
Repository: https://github.com/ananaware/MSCS-632-Expense-Tracker-Application---Team-8
Team: <Your Name> (Python Lead), <Teammate Name> (C++ Lead)
Course: MSCS 632 — Advanced Programming Languages
Deliverable 1 Date: Oct 24, 2025

## 1) Application Design (cross-language)
**Features:** add expense (id, date YYYY-MM-DD, amount, category, description), list, filter by date range or category, summary by category, overall total.  
**Storage:** CSV file `expenses.csv` with header `id,date,amount,category,description`.  
**UI:** CLI menu for both languages (deterministic for grading).  
**Core ops:** add_expense, list_expenses, filter_by_date, filter_by_category, summary_by_category, summary_overall.  
**Validation:** non-negative amounts, ISO date, category non-empty.

## 2) Language-Specific Designs
**Python (dynamic typing, dicts, datetime, csv)**
- In-memory: list[dict] like `{"id": int, "date": date, "amount": float, "category": str, "description": str}`
- Modules: `app.py` (CLI), `store.py` (CSV I/O), `model.py` (validation), `summary.py` (aggregations).

**C++ (static typing, STL, RAII)**
- `struct Expense { long id; std::string date; double amount; std::string category; std::string description; };`
- Files: `main.cpp` (CLI), `Expense.h/.cpp`, `Store.h/.cpp` (CSV I/O with fstreams), `Summary.h/.cpp` (maps, sort).

## 3) Key Differences & Rationale
Typing (dynamic vs static), data structures (dict/list vs struct+vector), I/O (csv module vs manual parsing), date handling (datetime vs string validation), error handling (exceptions vs explicit checks).

## 4) Repository Layout
docs/ # design & usage
python/ # Python CLI implementation
cpp/ # C++ implementation (CMake)
sample_data/ # demo CSV for testing
tests/python/ # (optional) basic tests

## 5) Task Assignment
- **Python Lead:** <Name> — Python CLI, storage, summaries; write docs/usage-python.md.
- **C++ Lead:** <Name> — C++ CLI, storage, summaries; write docs/usage-cpp.md.
- **QA & Data:** (shared) — sample CSV, validation checklist.
- **Documentation:** (shared) — maintain design.md, README, screenshots/gifs.

## 6) Timeline & Milestones
- **Day 1 (today):** Repo + design.md (this doc), add sample CSV, stubs build/run.
- **Day 2:** Python `store.py` (CSV load/save) + C++ `Store` prototype.
- **Day 3:** Python CLI + summaries; C++ CLI skeleton.
- **Day 4:** C++ summaries + parity check + polish.
- **Day 5:** Final docs, screenshots, validation edge cases.

## 7) Anticipated Language-Specific Challenges
Python: float formatting, date parsing errors, input sanitation.  
C++: quoted CSV fields, safe string→number conversion, sorting/aggregation boilerplate.

## 8) Acceptance Criteria
Parity across languages, robust validation, non-crashing CLI, matching summaries on same CSV, clear README with run instructions.
