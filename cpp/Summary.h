// Summary.h — Expense Tracker (C++)
// Purpose: Declares functions for filtering and summarizing expenses.
// Responsibilities:
//   - Filter by date range or category.
//   - Calculate category totals and overall sum.


#pragma once
#include "Expense.h"
#include <string>
#include <vector>
#include <unordered_map>

namespace Summary {
    std::unordered_map<std::string, double> totalsByCategory(const std::vector<Expense>& items);
    double overall(const std::vector<Expense>& items);
    std::vector<Expense> filterByDate(const std::vector<Expense>& items,
                                      const std::string& startIso,
                                      const std::string& endIso);
    std::vector<Expense> filterByCategory(const std::vector<Expense>& items,
                                          const std::string& category);
}
