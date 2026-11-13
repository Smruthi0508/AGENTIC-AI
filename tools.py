"""Analysis tools: exact numbers come from pandas, never from the LLM."""
import pandas as pd

FIXED_CATEGORIES = {"Rent", "Bills & Utilities", "Transfers", "Income"}


def _spend(df, month=None):
    s = df[df["debit"] > 0]
    return s[s["month"] == month] if month else s


def summary(df):
    s = _spend(df)
    months = sorted(df["month"].unique())
    income = float(df["credit"].sum())
    spend = float(s["debit"].sum())
    return {
        "period": f"{df['date'].min():%d %b %Y} to {df['date'].max():%d %b %Y}",
        "months": months,
        "total_spend": round(spend, 2),
        "total_income": round(income, 2),
        "net_savings": round(income - spend, 2),
        "spend_transactions": int(len(s)),
        "avg_monthly_spend": round(spend / max(len(months), 1), 2),
    }


def spend_by_category(df, month=None):
    s = _spend(df, month)
    g = s.groupby("category")["debit"].sum().sort_values(ascending=False)
    total = g.sum() or 1
    return [{"category": c, "amount": round(float(a), 2), "share_percent": round(float(a) / total * 100, 1)}
            for c, a in g.items()]


def monthly_trend(df):
    spend = _spend(df).groupby("month")["debit"].sum()
    income = df.groupby("month")["credit"].sum()
    return [{"month": m, "spend": round(float(spend.get(m, 0)), 2), "income": round(float(income.get(m, 0)), 2)}
            for m in sorted(df["month"].unique())]


def category_by_month(df):
    return _spend(df).pivot_table(index="category", columns="month", values="debit", aggfunc="sum", fill_value=0)


def top_merchants(df, n=5, month=None):
    s = _spend(df, month)
    g = s.groupby("merchant")["debit"].agg(["sum", "count"]).sort_values("sum", ascending=False).head(n)
    return [{"merchant": m, "amount": round(float(r["sum"]), 2), "transactions": int(r["count"])} for m, r in g.iterrows()]


def search_transactions(df, keyword=None, category=None, month=None, limit=8):
    s = _spend(df, month)
    if category:
        s = s[s["category"] == category]
    if keyword:
        mask = (s["description"].str.contains(keyword, case=False, regex=False)
                | s["merchant"].str.contains(keyword, case=False, regex=False))
        s = s[mask]
    s = s.sort_values("debit", ascending=False) if not keyword and not category else s.sort_values("date", ascending=False)
    rows = [{"date": f"{r.date:%d %b %Y}", "merchant": r.merchant, "amount": round(float(r.debit), 2), "category": r.category}
            for r in s.head(limit).itertuples()]
    return {"count": int(len(s)), "total": round(float(s["debit"].sum()), 2), "rows": rows}


def overspending_flags(df, budgets=None):
    """Deterministic rules the Advisor explains: user budgets, month-on-month jumps, dominant categories."""
    budgets = budgets or {}
    months = sorted(df["month"].unique())
    latest, earlier = months[-1], months[:-1]
    pivot = category_by_month(df)
    flags = []

    for cat, limit in budgets.items():
        spent = float(pivot.loc[cat, latest]) if cat in pivot.index and latest in pivot.columns else 0.0
        if spent > limit:
            flags.append({"category": cat, "type": "over_budget",
                          "message": f"{cat}: ₹{spent:,.0f} in {latest}, above your budget of ₹{limit:,.0f}"})

    if earlier:
        for cat in pivot.index:
            if cat in FIXED_CATEGORIES:
                continue
            now = float(pivot.loc[cat, latest]) if latest in pivot.columns else 0.0
            prev = float(pivot.loc[cat, earlier].mean())
            if prev > 0 and now > 1.25 * prev and now - prev >= 500:
                flags.append({"category": cat, "type": "jump",
                              "message": f"{cat}: ₹{now:,.0f} in {latest}, up {((now / prev) - 1) * 100:.0f}% vs the ₹{prev:,.0f} monthly average of earlier months"})

    total = float(pivot.sum().sum()) or 1
    for cat in ("Food & Dining", "Shopping", "Entertainment"):
        if cat in pivot.index:
            share = float(pivot.loc[cat].sum()) / total * 100
            if share > 30:
                flags.append({"category": cat, "type": "dominant",
                              "message": f"{cat} is {share:.0f}% of all spending"})

    seen, unique = set(), []
    for f in flags:  # one flag per category and type
        if (f["category"], f["type"]) not in seen:
            seen.add((f["category"], f["type"]))
            unique.append(f)
    return unique
