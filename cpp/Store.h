#pragma once
#include "Expense.h"
#include <string>
#include <vector>

namespace Store {
    // Path to shared CSV at repo root (../ from cpp/)
    static const std::string DEFAULT_CSV = "../expenses.csv";

    // Loads/ensures CSV exists; header: id,date,amount,category,description
    std::vector<Expense> load(const std::string& path = DEFAULT_CSV);

    // Overwrites file with all expenses
    void save(const std::vector<Expense>& items, const std::string& path = DEFAULT_CSV);

    // Append one expense (loads, pushes, saves)
    void append(const Expense& e, const std::string& path = DEFAULT_CSV);

    // Helpers
    long nextId(const std::vector<Expense>& items);

    // Validation (throws std::runtime_error on bad input)
    void validateDate(const std::string& iso);
    double parseAmount(const std::string& s);
    std::string normalizeCategory(const std::string& s);

    // --- Deliverable 2: New operations ---
    std::vector<Expense> deleteById(const std::vector<Expense>& items, long id);

    std::vector<Expense> editById(
        const std::vector<Expense>& items,
        long id,
        const std::string* newDate,
        const double* newAmount,
        const std::string* newCategory,
        const std::string* newDesc
    );

    std::vector<Expense> search(const std::vector<Expense>& items, const std::string& text);

}
