// Store.cpp — Expense Tracker (C++)
// Purpose: Implements the CSV load/save/append/delete/edit/search logic.
// Notes: Demonstrates STL (vector, unordered_map), exception handling,
//        and C++17 RAII for file streams.


#include "Store.h"
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <iomanip>
#include <filesystem>
#include <cctype>
#include <algorithm>

using std::string;
using std::vector;

static const char* HEADER = "id,date,amount,category,description";

// --- tiny CSV helpers (quote-aware for description) ---
static string escape_csv(const string& s) {
    bool needQuotes = s.find_first_of(",\"\n\r") != string::npos;
    if (!needQuotes) return s;
    std::string out = "\"";
    for (char c : s) {
        if (c == '"') out += "\"\""; else out += c;
    }
    out += "\"";
    return out;
}

// Reads one CSV line into 5 fields (id,date,amount,category,description).
// Handles quotes for the last field; simple but sufficient for our use.
static vector<string> parse_csv_line(const string& line) {
    vector<string> fields;
    fields.reserve(5);
    bool inQuotes = false;
    string cur;

    for (size_t i = 0; i < line.size(); ++i) {
        char c = line[i];
        if (inQuotes) {
            if (c == '"') {
                if (i + 1 < line.size() && line[i + 1] == '"') { cur += '"'; ++i; }
                else { inQuotes = false; }
            } else {
                cur += c;
            }
        } else {
            if (c == '"') { inQuotes = true; }
            else if (c == ',') { fields.push_back(cur); cur.clear(); }
            else { cur += c; }
        }
    }
    fields.push_back(cur);
    return fields;
}

namespace Store {

    static void ensure_csv(const string& path) {
        namespace fs = std::filesystem;
        fs::path p(path);
        if (!fs::exists(p.parent_path()) && !p.parent_path().empty()) {
            fs::create_directories(p.parent_path());
        }
        if (!fs::exists(p)) {
            std::ofstream out(path, std::ios::out);
            out << HEADER << "\n";
        }
    }

    vector<Expense> load(const string& path) {
        ensure_csv(path);
        vector<Expense> items;
        std::ifstream in(path);
        if (!in.good()) throw std::runtime_error("Failed to open CSV: " + path);

        string line;
        // skip header
        if (!std::getline(in, line)) return items;

        while (std::getline(in, line)) {
            if (line.empty()) continue;
            auto fields = parse_csv_line(line);
            if (fields.size() < 5) continue;
            Expense e{};
            try {
                e.id = std::stol(fields[0]);
                e.date = fields[1];
                e.amount = std::stod(fields[2]);
                e.category = fields[3];
                e.description = fields[4];
                items.push_back(e);
            } catch (...) {
                // skip malformed lines
            }
        }
        return items;
    }

    void save(const vector<Expense>& items, const string& path) {
        ensure_csv(path);
        std::ofstream out(path, std::ios::out | std::ios::trunc);
        if (!out.good()) throw std::runtime_error("Failed to write CSV: " + path);
        out << HEADER << "\n";
        for (const auto& e : items) {
            out << e.id << ","
                << e.date << ","
                << std::fixed << std::setprecision(2) << e.amount << ","
                << escape_csv(e.category) << ","
                << escape_csv(e.description) << "\n";
        }
    }

    void append(const Expense& e, const string& path) {
        auto items = load(path);
        items.push_back(e);
        save(items, path);
    }

    long nextId(const vector<Expense>& items) {
        long mx = 0;
        for (const auto& e : items) if (e.id > mx) mx = e.id;
        return mx + 1;
    }

    // --- validation ---
    static bool is_digit4(const string& s) {
        return s.size() == 4 && std::all_of(s.begin(), s.end(), ::isdigit);
    }
    static bool is_digit2(const string& s) {
        return s.size() == 2 && std::all_of(s.begin(), s.end(), ::isdigit);
    }

    void validateDate(const string& iso) {
        // Minimal YYYY-MM-DD checks
        if (iso.size() != 10 || iso[4] != '-' || iso[7] != '-')
            throw std::runtime_error("Invalid date. Use YYYY-MM-DD.");
        string y = iso.substr(0,4), m = iso.substr(5,2), d = iso.substr(8,2);
        if (!is_digit4(y) || !is_digit2(m) || !is_digit2(d))
            throw std::runtime_error("Invalid date. Use YYYY-MM-DD.");
        int mi = std::stoi(m), di = std::stoi(d);
        if (mi < 1 || mi > 12 || di < 1 || di > 31)
            throw std::runtime_error("Invalid date range.");
    }

    double parseAmount(const string& s) {
        try {
            double v = std::stod(s);
            if (v < 0.0) throw std::runtime_error("Amount must be non-negative.");
            return v;
        } catch (...) {
            throw std::runtime_error("Amount must be numeric.");
        }
    }

    std::string normalizeCategory(const std::string& s) {
        std::string t = s;
        // trim
        while (!t.empty() && std::isspace((unsigned char)t.front())) t.erase(t.begin());
        while (!t.empty() && std::isspace((unsigned char)t.back())) t.pop_back();
        if (t.empty()) throw std::runtime_error("Category cannot be empty.");
        return t;
    }
}

// ===================== Deliverable 2: implementations =====================

std::vector<Expense> Store::deleteById(const std::vector<Expense>& items, long id) {
    std::vector<Expense> out;
    out.reserve(items.size());
    for (const auto& e : items) {
        if (e.id != id) out.push_back(e);
    }
    return out;
}

std::vector<Expense> Store::editById(
    const std::vector<Expense>& items,
    long id,
    const std::string* newDate,
    const double* newAmount,
    const std::string* newCategory,
    const std::string* newDesc
) {
    std::vector<Expense> out = items; // copy, then modify in place
    for (auto& e : out) {
        if (e.id == id) {
            if (newDate) {
                validateDate(*newDate);
                e.date = *newDate;
            }
            if (newAmount) {
                if (*newAmount < 0.0) throw std::runtime_error("Amount must be >= 0");
                e.amount = *newAmount;
            }
            if (newCategory) {
                e.category = normalizeCategory(*newCategory);
            }
            if (newDesc) {
                e.description = *newDesc;
            }
            break;
        }
    }
    return out;
}

std::vector<Expense> Store::search(const std::vector<Expense>& items, const std::string& text) {
    // lowercase query
    std::string q = text;
    std::transform(q.begin(), q.end(), q.begin(), [](unsigned char c){ return std::tolower(c); });

    std::vector<Expense> out;
    out.reserve(items.size());
    for (const auto& e : items) {
        std::string cat = e.category;
        std::string desc = e.description;
        std::transform(cat.begin(), cat.end(), cat.begin(), [](unsigned char c){ return std::tolower(c); });
        std::transform(desc.begin(), desc.end(), desc.begin(), [](unsigned char c){ return std::tolower(c); });
        if (cat.find(q) != std::string::npos || desc.find(q) != std::string::npos) {
            out.push_back(e);
        }
    }
    return out;
}
