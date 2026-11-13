"""Creates a realistic 3-month sample statement + hidden labels for accuracy testing.
Some merchants (HOTEL MTR, AUTO RAMESH...) are NOT in the keyword rules, so the LLM fallback gets tested too."""
import csv
import math
import random

rng = random.Random(42)
MONTHS = [(2026, 8), (2026, 9), (2026, 10)]

# merchant, label, (min_count, max_count), (min_amt, max_amt), fixed_amount_or_None
SPEC = [
    ("SWIGGY", "Food & Dining", (7, 10), (150, 450), None),
    ("ZOMATO", "Food & Dining", (2, 4), (180, 500), None),
    ("STARBUCKS", "Food & Dining", (1, 3), (250, 450), None),
    ("HOTEL MTR", "Food & Dining", (3, 4), (120, 300), None),
    ("SRI SAI TIFFINS", "Food & Dining", (4, 6), (60, 160), None),
    ("BLINKIT", "Groceries", (3, 5), (200, 700), None),
    ("DMART", "Groceries", (1, 2), (900, 2200), None),
    ("NANDINI MILK PARLOUR", "Groceries", (5, 7), (30, 110), None),
    ("KRISHNA GENERAL STORE", "Groceries", (2, 3), (100, 450), None),
    ("UBER", "Transport", (3, 5), (120, 380), None),
    ("RAPIDO", "Transport", (4, 6), (50, 160), None),
    ("BMTC BUS PASS", "Transport", (1, 1), (0, 0), 1050),
    ("AUTO RAMESH", "Transport", (2, 4), (40, 120), None),
    ("AMAZON", "Shopping", (2, 3), (350, 2800), None),
    ("MYNTRA", "Shopping", (1, 2), (700, 2400), None),
    ("FLIPKART", "Shopping", (0, 1), (500, 1800), None),
    ("SHREE TAILORS", "Shopping", (0, 1), (300, 700), None),
    ("NETFLIX", "Entertainment", (1, 1), (0, 0), 649),
    ("SPOTIFY", "Entertainment", (1, 1), (0, 0), 119),
    ("BOOKMYSHOW", "Entertainment", (1, 2), (300, 800), None),
    ("AIRTEL PREPAID RECHARGE", "Bills & Utilities", (1, 1), (0, 0), 599),
    ("BESCOM ELECTRICITY", "Bills & Utilities", (1, 1), (350, 900), None),
    ("APOLLO PHARMACY", "Health", (1, 2), (150, 650), None),
    ("DR SHETTY CARE CENTRE", "Health", (0, 1), (300, 600), None),
    ("UDEMY", "Education", (0, 1), (449, 699), None),
    ("PG RENT", "Rent", (1, 1), (0, 0), 7000),
]
FRIENDS = ["ARJUN K", "MEERA S", "KAVYA R", "ROHAN M"]
OCT_BOOST = {"Shopping", "Entertainment"}  # makes the October overspending story visible


def txn_id():
    return "".join(str(rng.randint(0, 9)) for _ in range(12))


rows = []  # (day, month_tuple, description, debit, credit, label)
for (y, m) in MONTHS:
    rows.append((2, (y, m), f"UPI/PARENTS POCKET MONEY/{txn_id()}", 0, 15000, "Income"))
    rows.append((5, (y, m), f"NEFT/INTERNSHIP STIPEND/REF{rng.randint(10000, 99999)}", 0, 8000, "Income"))
    for merchant, label, (lo, hi), (a_lo, a_hi), fixed in SPEC:
        n = rng.randint(lo, hi)
        if m == 10 and label in OCT_BOOST and fixed is None:
            n = math.ceil(n * 1.8)
        for _ in range(n):
            amt = fixed if fixed else rng.randint(a_lo, a_hi)
            if m == 10 and label in OCT_BOOST and fixed is None:
                amt = int(amt * 1.3)
            day = 1 if "RENT" in merchant else rng.randint(1, 28)
            rows.append((day, (y, m), f"UPI/{merchant}/{txn_id()}/Payment", amt, 0, label))
    for _ in range(rng.randint(3, 5)):
        rows.append((rng.randint(1, 28), (y, m), f"UPI/P2P/{rng.choice(FRIENDS)}/{txn_id()}", rng.randint(200, 1500), 0, "Transfers"))

rows.sort(key=lambda r: (r[1], r[0]))
balance = 25000
with open("data/sample_statement.csv", "w", newline="", encoding="utf-8") as f, \
     open("data/sample_labels.csv", "w", newline="", encoding="utf-8") as g:
    w, lw = csv.writer(f), csv.writer(g)
    w.writerow(["Date", "Description", "Debit", "Credit", "Balance"])
    lw.writerow(["row", "true_category"])
    for i, (day, (y, m), desc, debit, credit, label) in enumerate(rows):
        balance += credit - debit
        w.writerow([f"{day:02d}/{m:02d}/{y}", desc, debit or "", credit or "", balance])
        lw.writerow([i, label])
print(f"Wrote {len(rows)} transactions to data/sample_statement.csv")
