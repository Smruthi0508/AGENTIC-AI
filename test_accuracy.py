"""Measures categorisation accuracy on the sample data (uses the LLM for unknown merchants).
Run: python test_accuracy.py
Tip: also test on your own statement and label ~50 rows by hand for a more honest number."""
import pandas as pd

from ingest import categorize, load_statement

df = categorize(load_statement("data/sample_statement.csv"))
if df.attrs.get("llm_error"):
    print("LLM error:", df.attrs["llm_error"])
labels = pd.read_csv("data/sample_labels.csv")
m = df.merge(labels, on="row")
m["correct"] = m["category"] == m["true_category"]

print(f"Transactions: {len(m)}")
print(f"Overall accuracy: {m['correct'].mean() * 100:.1f}%")
for src, g in m.groupby("category_source"):
    print(f"  {src:>6}: {len(g):3d} rows, {g['correct'].mean() * 100:.1f}% correct")
wrong = m[~m["correct"]][["merchant", "category", "true_category"]].drop_duplicates()
if len(wrong):
    print("\nMistakes (merchant, predicted, true):")
    print(wrong.to_string(index=False))
