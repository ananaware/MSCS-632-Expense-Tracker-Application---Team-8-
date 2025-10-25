"""
app.py — CLI for the Expense Tracker (Python)

Responsibilities:
- Menu/UI only; delegates storage/filtering/validation to store.py
- Implements: add, view, filter (date/category), summary, overall, delete/edit/search

Language-specific notes:
- Simple, readable control flow; shows dynamic typing and quick iteration
"""


# Expense Tracker CLI (Python)
# Deliverable 2: complete core features + language-specific bits
# Uses dynamic typing (dicts) and datetime parsing where helpful

from store import (
    load_all, save_all,
    validate_iso, parse_amount,
    delete_by_id, edit_by_id, search
)

from datetime import datetime

# ---------- helpers ----------

def next_id(rows):
    if not rows:
        return 1
    # rows store id as int or str; normalize to int for max
    return max(int(r.get("id", 0)) for r in rows) + 1

def to_iso(d):
    """Just return the string; validate_iso already ensures YYYY-MM-DD."""
    return d

def list_all(rows):
    if not rows:
        print("(no expenses yet)")
        return
    print("ID   Date        Amount   Category     Description")
    print("--   ----------  -------  --------     -----------")
    for r in rows:
        print(f"{str(r.get('id')).ljust(4)} {str(r.get('date')).ljust(10)}  "
              f"${float(r.get('amount')):7.2f}  {str(r.get('category'))[:12].ljust(12)}  {str(r.get('description'))}")

def filter_by_date_range(rows, start_iso, end_iso):
    s = start_iso
    e = end_iso
    # ISO (YYYY-MM-DD) strings compare lexicographically for ranges
    return [r for r in rows if s <= str(r.get("date", "")) <= e]

def filter_by_category(rows, cat):
    t = (cat or "").strip().lower()
    return [r for r in rows if (str(r.get("category", "")).lower() == t)]

def summary_by_category(rows):
    totals = {}
    for r in rows:
        cat = str(r.get("category", "Uncategorized")).strip() or "Uncategorized"
        amt = float(r.get("amount", 0.0))
        totals[cat] = totals.get(cat, 0.0) + amt
    return totals

def overall_total(rows):
    return sum(float(r.get("amount", 0.0)) for r in rows)

# ---------- menu actions ----------

def action_add():
    rows = load_all()
    try:
        d = validate_iso(input("Date (YYYY-MM-DD): ").strip())
        a = parse_amount(input("Amount: ").strip())
        c = input("Category: ").strip()
        desc = input("Description: ").strip()
        new = {
            "id": next_id(rows),
            "date": to_iso(d),
            "amount": a,
            "category": c,
            "description": desc
        }
        rows.append(new)
        save_all(rows)
        print(f"Added: id={new['id']} {new['date']} ${new['amount']:.2f} {new['category']} - {new['description']}")
    except ValueError as ve:
        print(f"Input error: {ve}")

def action_view_all():
    rows = load_all()
    list_all(rows)
    print(f"\nTotal count: {len(rows)}  |  Overall total: ${overall_total(rows):.2f}")

def action_filter_date():
    rows = load_all()
    try:
        s = validate_iso(input("Start date (YYYY-MM-DD): ").strip())
        e = validate_iso(input("End date   (YYYY-MM-DD): ").strip())
        if s > e:
            print("Start date must be <= end date.")
            return
        out = filter_by_date_range(rows, s, e)
        list_all(out)
        print(f"\nMatches: {len(out)}  |  Total: ${overall_total(out):.2f}")
    except ValueError as ve:
        print(f"Input error: {ve}")

def action_filter_category():
    rows = load_all()
    cat = input("Category (exact match): ").strip()
    out = filter_by_category(rows, cat)
    list_all(out)
    print(f"\nMatches: {len(out)}  |  Total: ${overall_total(out):.2f}")

def action_summary_by_category():
    rows = load_all()
    totals = summary_by_category(rows)
    if not totals:
        print("(no data)")
        return
    print("Category          Total")
    print("--------          -----")
    for k in sorted(totals.keys()):
        print(f"{k[:16].ljust(16)}  ${totals[k]:.2f}")
    print(f"\nOverall total: ${overall_total(rows):.2f}")

def action_overall_total():
    rows = load_all()
    print(f"Overall total: ${overall_total(rows):.2f}")

def action_delete():
    rows = load_all()
    xid = input("ID to delete: ").strip()
    new_rows = delete_by_id(rows, xid)
    save_all(new_rows)
    if len(new_rows) < len(rows):
        print("Deleted.")
    else:
        print("ID not found.")

def action_edit():
    rows = load_all()
    xid = input("ID to edit: ").strip()
    print("Leave a field blank to keep unchanged.")
    nd = input("New date (YYYY-MM-DD): ").strip()
    na = input("New amount: ").strip()
    nc = input("New category: ").strip()
    nx = input("New description: ").strip()

    updates = {}
    try:
        if nd:
            updates["date"] = validate_iso(nd)
        if na:
            updates["amount"] = parse_amount(na)
        if nc:
            updates["category"] = nc
        if nx:
            updates["description"] = nx
        new_rows = edit_by_id(rows, xid, **updates)
        save_all(new_rows)
        print("Edited (if ID existed).")
    except ValueError as ve:
        print(f"Input error: {ve}")

def action_search():
    rows = load_all()
    q = input("Search text (in category/description): ").strip()
    out = search(rows, q)
    list_all(out)
    print(f"\nMatches: {len(out)}  |  Total: ${overall_total(out):.2f}")

# ---------- main loop ----------

def main():
    while True:
        print("\n==== Expense Tracker (Python) ====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter by Date Range")
        print("4. Filter by Category")
        print("5. Summary by Category")
        print("6. Overall Total")
        print("7. Delete by ID")
        print("8. Edit by ID")
        print("9. Search text")
        print("0. Exit")
        choice = input("Choose (0-9): ").strip()
        if choice == "1": action_add()
        elif choice == "2": action_view_all()
        elif choice == "3": action_filter_date()
        elif choice == "4": action_filter_category()
        elif choice == "5": action_summary_by_category()
        elif choice == "6": action_overall_total()
        elif choice == "7": action_delete()
        elif choice == "8": action_edit()
        elif choice == "9": action_search()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
