#pragma once
#include <string>

struct Expense {
    long id{};
    std::string date;        // ISO YYYY-MM-DD
    double amount{};         // non-negative
    std::string category;
    std::string description;
};
