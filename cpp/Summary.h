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
