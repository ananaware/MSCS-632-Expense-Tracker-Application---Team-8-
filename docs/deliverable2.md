# Deliverable 2 — Core Functionality Implementation

**Date:** 2025-10-25  
**Team:** 8 — Anushka Nanaware, Anusha Pittala  
**Repo:** MSCS-632-Expense-Tracker-Application---Team-8-

## Scope Completed
- Core features fully operational in **Python** and **C++**:
  - Add, List, Filter by Date, Filter by Category
  - **New:** Delete by ID, Edit by ID, Search (description/category)
  - Summary by Category, Overall Total
- Shared persistence: `expenses.csv` interoperable across languages.

## Language-Specific Features Demonstrated
- **Python:** dynamic typing with `dict` records; `datetime` parsing; list/dict comprehensions; validation helpers (`validate_iso`, `parse_amount`).
- **C++:** static typing with `struct/class Expense`; STL containers (`vector`, `unordered_map`); algorithms (`transform`); RAII file I/O; exceptions (`std::runtime_error`).

## Code Quality Practices
- Python: small functions, docstrings (store.py helpers), clear prints, validation on input.
- C++: header guards, split headers/impl, exceptions for invalid input, menu-driven CLI, `optional` for edit flow.

## Basic Testing Performed
- Manual tests:
  - Add two records → List → Search by keyword → Edit amount/category → Delete by ID → Summary + Overall.
  - Cross-language: add/edit/delete in one language, verify in the other.
- (Optional tests included in repo if added later: `python/test_store.py`, `cpp/test_main.cpp`.)

## How to Run
**Python**
```bash
cd python
python app.py

**C++ (MSVC)**
```bat
cd cpp
cl /std:c++17 /EHsc /O2 main.cpp Expense.cpp Store.cpp Summary.cpp /Fe:expense_tracker_cpp.exe
expense_tracker_cpp.exe
