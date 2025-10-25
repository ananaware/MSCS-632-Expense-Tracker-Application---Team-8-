from __future__ import annotations
import csv
from datetime import datetime

CSV_FILE = "../expenses.csv"  # adjust path if needed

def load_all():
    """Load all expenses from the shared CSV file and return a list of dicts."""
    rows = []
    try:
        with open(CSV_FILE, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        pass  # start empty if no file yet
    return rows

def save_all(rows):
    """Write all expenses back to CSV file, preserving the schema."""
    fieldnames = ["id", "date", "amount", "category", "description"]
    with open(CSV_FILE, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "id": r.get("id"),
                "date": r.get("date"),
                "amount": r.get("amount"),
                "category": r.get("category"),
                "description": r.get("description"),
            })
# python/store.py

from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
import csv
from typing import List, Dict, Iterable, Optional

# We keep a single CSV at the repo root so Python & C++ share the same data.
DEFAULT_CSV = (Path(__file__).resolve().parents[1] / "expenses.csv")

HEADER = ["id", "date", "amount", "category", "description"]


@dataclass
class Expense:
    id: int
    date: date
    amount: Decimal  # store with cents precision
    category: str
    description: str = ""

    def to_csv_row(self) -> Dict[str, str]:
        return {
            "id": str(self.id),
            "date": self.date.isoformat(),
            # normalize to 2 decimals for consistent C++ parsing later
            "amount": f"{self.amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}",
            "category": self.category,
            "description": self.description,
        }

    @staticmethod
    def from_csv_row(row: Dict[str, str]) -> "Expense":
        # Minimal validation when loading; we assume file is well-formed
        return Expense(
            id=int(row["id"]),
            date=date.fromisoformat(row["date"]),
            amount=Decimal(row["amount"]),
            category=row["category"],
            description=row.get("description", ""),
        )


# ---------- file utilities ----------

def _ensure_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=HEADER)
            writer.writeheader()


def load_expenses(path: Path = DEFAULT_CSV) -> List[Expense]:
    """Load all expenses from CSV. Returns a list of Expense objects."""
    _ensure_csv(path)
    out: List[Expense] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            out.append(Expense.from_csv_row(row))
    return out


def save_expenses(expenses: Iterable[Expense], path: Path = DEFAULT_CSV) -> None:
    """Write all expenses to CSV (overwrites file)."""
    _ensure_csv(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        for e in expenses:
            writer.writerow(e.to_csv_row())


# ---------- validations & helpers ----------

def _parse_date(iso_str: str) -> date:
    try:
        return date.fromisoformat(iso_str.strip())
    except Exception:
        raise ValueError("Invalid date. Use YYYY-MM-DD (e.g., 2025-10-24).")


def _parse_amount(value: str | float | int | Decimal) -> Decimal:
    try:
        amt = Decimal(str(value))
    except Exception:
        raise ValueError("Amount must be a number.")
    if amt < 0:
        raise ValueError("Amount must be non-negative.")
    # normalize to cents
    return amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _normalize_category(cat: str) -> str:
    cat = (cat or "").strip()
    if not cat:
        raise ValueError("Category cannot be empty.")
    # Simple normalization (case-insensitive match in filters later)
    return cat


def next_id(existing: Iterable[Expense]) -> int:
    mx = 0
    for e in existing:
        if e.id > mx:
            mx = e.id
    return mx + 1


# ---------- public API used by CLI ----------

def add_expense(
    date_str: str,
    amount: str | float | int | Decimal,
    category: str,
    description: str = "",
    path: Path = DEFAULT_CSV,
) -> Expense:
    """Validate inputs, assign an id, append a new expense to CSV, and return it."""
    items = load_expenses(path)
    e = Expense(
        id=next_id(items),
        date=_parse_date(date_str),
        amount=_parse_amount(amount),
        category=_normalize_category(category),
        description=(description or "").strip(),
    )
    items.append(e)
    save_expenses(items, path)
    return e


def list_expenses(path: Path = DEFAULT_CSV) -> List[Expense]:
    return load_expenses(path)


def filter_by_date(start_iso: str, end_iso: str, path: Path = DEFAULT_CSV) -> List[Expense]:
    start_d = _parse_date(start_iso)
    end_d = _parse_date(end_iso)
    if end_d < start_d:
        raise ValueError("End date must be on/after start date.")
    return [e for e in load_expenses(path) if start_d <= e.date <= end_d]


def filter_by_category(category: str, path: Path = DEFAULT_CSV) -> List[Expense]:
    cat_norm = _normalize_category(category).lower()
    return [e for e in load_expenses(path) if e.category.lower() == cat_norm]


def summary_by_category(path: Path = DEFAULT_CSV) -> Dict[str, Decimal]:
    totals: Dict[str, Decimal] = {}
    for e in load_expenses(path):
        key = e.category
        totals[key] = totals.get(key, Decimal("0.00")) + e.amount
    # Keep cents normalized
    for k in totals:
        totals[k] = totals[k].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return totals


def summary_overall(path: Path = DEFAULT_CSV) -> Decimal:
    total = sum((e.amount for e in load_expenses(path)), Decimal("0.00"))
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

# ========= Deliverable 2 helpers: delete/edit/search + validation =========

def delete_by_id(rows, xid):
    """Return a new list with the expense having id=xid removed."""
    xid = str(xid)
    return [r for r in rows if str(r.get("id")) != xid]

def edit_by_id(rows, xid, **updates):
    """
    Return a new list with the expense having id=xid updated.
    Pass updates like date="YYYY-MM-DD", amount=12.34, category="Food", description="text".
    Blank/None updates are ignored.
    """
    xid = str(xid)
    out = []
    for r in rows:
        if str(r.get("id")) == xid:
            nr = dict(r)
            for k, v in updates.items():
                if v is not None and v != "":
                    nr[k] = v
            out.append(nr)
        else:
            out.append(r)
    return out

def search(rows, text):
    """Case-insensitive substring search in category or description."""
    t = (text or "").lower().strip()
    return [
        r for r in rows
        if t in str(r.get("category", "")).lower() or t in str(r.get("description", "")).lower()
    ]

# ---- simple validation helpers you can call before saving/using data ----

def validate_iso(date_str):
    """Ensure YYYY-MM-DD format; return the same string if valid, else raise ValueError."""
    import re
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", (date_str or "").strip()):
        raise ValueError("Date must be in YYYY-MM-DD format")
    return date_str.strip()

def parse_amount(s):
    """Parse a string to a non-negative float with 2 decimals; raise ValueError on bad input."""
    try:
        val = float(s)
        if val < 0:
            raise ValueError
        return round(val, 2)
    except Exception:
        raise ValueError("Amount must be a non-negative number (e.g., 12.50)")

