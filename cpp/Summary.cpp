// Summary.cpp — Expense Tracker (C++)
// Purpose: Implements filtering and aggregation logic for expenses.
// Notes: Demonstrates STL algorithms, unordered_map aggregation, and numeric ops.


#include "Summary.h"
#include "Store.h"
#include <algorithm>
#include <cctype>
#include <stdexcept>


using std::string;
using std::vector;
using std::unordered_map;

namespace Summary {

    static string lower(string s) {
        std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c){ return std::tolower(c); });
        return s;
    }

    unordered_map<string, double> totalsByCategory(const vector<Expense>& items) {
        unordered_map<string, double> totals;
        for (const auto& e : items) {
            totals[e.category] += e.amount;
        }
        return totals;
    }

    double overall(const vector<Expense>& items) {
        double sum = 0.0;
        for (const auto& e : items) sum += e.amount;
        return sum;
    }

    vector<Expense> filterByDate(const vector<Expense>& items, const string& startIso, const string& endIso) {
        Store::validateDate(startIso);
        Store::validateDate(endIso);
        if (endIso < startIso) throw std::runtime_error("End date must be on/after start date.");
        vector<Expense> out;
        for (const auto& e : items) {
            if (e.date >= startIso && e.date <= endIso) out.push_back(e);
        }
        return out;
    }

    vector<Expense> filterByCategory(const vector<Expense>& items, const string& category) {
        string want = lower(Store::normalizeCategory(category));
        vector<Expense> out;
        for (const auto& e : items) {
            if (lower(e.category) == want) out.push_back(e);
        }
        return out;
    }
}
