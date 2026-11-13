"""Parser agent (CSV) + Categoriser agent (rules first, LLM for the rest)."""
import re
import pandas as pd
from categories import rule_category

GENERIC_PARTS = {"UPI", "POS", "NEFT", "IMPS", "P2P", "ACH", "ATM", "RTGS", "DR", "CR"}


def _num(series):
    cleaned = series.astype(str).str.replace(r"[₹,\s]", "", regex=True)
    return pd.to_numeric(cleaned, errors="coerce").fillna(0.0)


def _find(cols, keys):
    for c in cols:
        if any(k in c.lower() for k in keys):
            return c
    return None


def _merchant(desc):
    parts = [p.strip() for p in re.split(r"[/\-|]", str(desc))]
    parts = [p for p in parts if p and p.upper() not in GENERIC_PARTS and not re.fullmatch(r"[\d\s]+", p)]
    return (parts[0] if parts else str(desc)).upper()[:40]


def load_statement(file):
    """Accepts a path or an uploaded file. Detects columns by name."""
    raw = pd.read_csv(file)
    raw.columns = [str(c).strip() for c in raw.columns]
    cols = list(raw.columns)
    date_c = _find(cols, ["date"])
    desc_c = _find(cols, ["description", "narration", "particulars", "details", "remarks"])
    debit_c = _find(cols, ["debit", "withdrawal"])
    credit_c = _find(cols, ["credit", "deposit"])
    amount_c = _find(cols, ["amount"])
    if not date_c or not desc_c or not (debit_c or credit_c or amount_c):
        raise ValueError(
            f"Could not detect columns. Found: {cols}. Need a date, a description and debit/credit (or amount) column."
        )

    if debit_c or credit_c:
        debit = _num(raw[debit_c]) if debit_c else 0.0
        credit = _num(raw[credit_c]) if credit_c else 0.0
    else:  # single signed amount column: negative = money out
        amt = _num(raw[amount_c])
        debit, credit = -amt.clip(upper=0), amt.clip(lower=0)

    df = pd.DataFrame({
        "row": range(len(raw)),
        "date": pd.to_datetime(raw[date_c], dayfirst=True, errors="coerce"),
        "description": raw[desc_c].astype(str).str.strip(),
        "debit": debit,
        "credit": credit,
    }).dropna(subset=["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")
    df["merchant"] = df["description"].map(_merchant)
    return df.reset_index(drop=True)


def categorize(df, use_llm=True):
    """Rules first. Unknown merchants go to the LLM in batches of 30 (one call per batch)."""
    df = df.copy()
    df["category"] = df["description"].map(rule_category)
    df["category_source"] = df["category"].map(lambda c: "rules" if c else None)

    is_credit = (df["credit"] > 0) & (df["debit"] == 0)
    df.loc[is_credit, "category"] = "Income"
    df.loc[is_credit, "category_source"] = "rules"

    unknown = df["category"].isna()
    df.attrs["llm_error"] = None
    if unknown.any():
        mapping = {}
        if use_llm:
            from chains import llm_categorize
            merchants = sorted(df.loc[unknown, "merchant"].unique())
            for i in range(0, len(merchants), 30):
                try:
                    mapping.update(llm_categorize(merchants[i:i + 30]))
                except Exception as e:  # keep the app usable if the API fails
                    df.attrs["llm_error"] = str(e)
        df.loc[unknown, "category"] = df.loc[unknown, "merchant"].map(mapping).fillna("Other")
        df.loc[unknown, "category_source"] = "llm" if use_llm else "none"
    return df
