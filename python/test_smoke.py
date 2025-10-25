# test_smoke.py — quick Deliverable 2 smoke test (no user input or file writes)
# Confirms core functions run without error in store.py

from store import load_all, delete_by_id, edit_by_id, search, parse_amount

print("Running smoke test...")

# load current expenses
rows = load_all()
base_count = len(rows)
print(f"Loaded {base_count} expenses.")

# create fake row (in memory only)
fake = {
    "id": 99999,
    "date": "2025-10-25",
    "amount": parse_amount("12.50"),
    "category": "Test",
    "description": "smoke test"
}
rows.append(fake)

# edit fake record
rows = edit_by_id(rows, 99999, date="2025-10-26", amount=20.00, category="UpdatedTest", description="edited")


# search by keyword
found = search(rows, "Test")
assert any(r["id"] == 99999 for r in found)

# delete fake record
rows = delete_by_id(rows, 99999)
assert len(rows) == base_count

print("✅ OK: smoke test passed (no file writes).")
