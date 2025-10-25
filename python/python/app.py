# python/app.py
from store import add_expense, list_expenses, summary_overall

if __name__ == "__main__":
    # Demo: add one expense and show total (safe to run multiple times)
    e = add_expense("2025-10-24", 9.99, "Food", "Demo lunch")
    print(f"Added: id={e.id} {e.date} ${e.amount} {e.category} - {e.description}")

    all_rows = list_expenses()
    print(f"Now have {len(all_rows)} expenses. Overall total = ${summary_overall()}")
