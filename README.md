# MSCS 632 — Expense Tracker (Python & C++)
Two-language CLI app to add/list/filter expenses and compute summaries.

## Structure
- `python/` — dict-based storage, datetime, csv
- `cpp/` — struct/class + STL, fstreams
- `docs/` — design & usage
- `sample_data/` — demo CSV

## Run
See `docs/usage-python.md` and `docs/usage-cpp.md`.

## C++ (Windows / MSVC)
Open “x64 Native Tools Command Prompt for VS 2022”, then:
cd cpp
cl /std:c++17 /EHsc /O2 main.cpp Expense.cpp Store.cpp Summary.cpp /Fe:expense_tracker_cpp.exe
expense_tracker_cpp.exe

