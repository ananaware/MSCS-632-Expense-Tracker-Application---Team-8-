#include <iostream>
#include <iomanip>
#include "Store.h"
#include "Summary.h"

using namespace std;

static void printExpenses(const std::vector<Expense>& v) {
    if (v.empty()) { cout << "No expenses found.\n"; return; }
    cout << left << setw(5) << "ID" << setw(12) << "Date" << setw(10) << "Amount"
         << setw(15) << "Category" << "Description\n";
    cout << string(60, '-') << "\n";
    for (const auto& e : v) {
        cout << left << setw(5) << e.id
             << setw(12) << e.date
             << setw(10) << fixed << setprecision(2) << e.amount
             << setw(15) << e.category
             << e.description << "\n";
    }
}

int main() {
    try {
        while (true) {
            cout << "\n==== Expense Tracker (C++) ====\n"
                 << "1. Add Expense\n"
                 << "2. View All Expenses\n"
                 << "3. Filter by Date Range\n"
                 << "4. Filter by Category\n"
                 << "5. Summary by Category\n"
                 << "6. Overall Total\n"
                 << "7. Exit\n"
                 << "Choose (1-7): ";
            string choice; getline(cin, choice);

            if (choice == "1") {
                auto items = Store::load();
                Expense e{};
                e.id = Store::nextId(items);
                cout << "Date (YYYY-MM-DD): "; getline(cin, e.date); Store::validateDate(e.date);
                cout << "Amount: "; { string s; getline(cin, s); e.amount = Store::parseAmount(s); }
                cout << "Category: "; { string s; getline(cin, s); e.category = Store::normalizeCategory(s); }
                cout << "Description (optional): "; getline(cin, e.description);
                Store::append(e);
                cout << "Added expense ID " << e.id << " — $" << fixed << setprecision(2) << e.amount << " " << e.category << "\n";

            } else if (choice == "2") {
                auto items = Store::load();
                printExpenses(items);

            } else if (choice == "3") {
                string s, e;
                cout << "Start date (YYYY-MM-DD): "; getline(cin, s);
                cout << "End date (YYYY-MM-DD): "; getline(cin, e);
                auto items = Store::load();
                auto res = Summary::filterByDate(items, s, e);
                printExpenses(res);

            } else if (choice == "4") {
                string c; cout << "Category: "; getline(cin, c);
                auto items = Store::load();
                auto res = Summary::filterByCategory(items, c);
                printExpenses(res);

            } else if (choice == "5") {
                auto items = Store::load();
                auto totals = Summary::totalsByCategory(items);
                cout << "\nCategory Totals:\n";
                for (auto& kv : totals) cout << left << setw(15) << kv.first << " $" << fixed << setprecision(2) << kv.second << "\n";
                cout << "Overall total: $" << fixed << setprecision(2) << Summary::overall(items) << "\n";

            } else if (choice == "6") {
                auto items = Store::load();
                cout << "Overall total: $" << fixed << setprecision(2) << Summary::overall(items) << "\n";

            } else if (choice == "7" || cin.eof()) {
                cout << "Goodbye!\n";
                break;
            } else {
                cout << "Invalid choice.\n";
            }
        }
    } catch (const std::exception& ex) {
        cerr << "Error: " << ex.what() << "\n";
        return 1;
    }
    return 0;
}
