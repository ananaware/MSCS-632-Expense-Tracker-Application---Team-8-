// Expense.h — Expense Tracker (C++)
// Purpose: Defines the Expense struct used to represent a single expense record.
// Responsibilities:
//   - Holds id, date, amount, category, description.
//   - Shared between Store.cpp, Summary.cpp, and main.cpp.
// Notes: Mirrors Python’s dict schema for CSV interoperability.


#pragma once
#include <string>

struct Expense {
    long id{};
    std::string date;        // ISO YYYY-MM-DD
    double amount{};         // non-negative
    std::string category;
    std::string description;
};
