"""Router -> tools (pandas) -> optional RAG -> advisor."""
import json

import pandas as pd

import tools as T
import vectors as V
from categories import SPEND_CATEGORIES
from chains import run_explainer, run_router

INTENTS = ("lookup", "analysis", "savings", "chitchat")


def route(message, months):
    out = run_router(message, months)
    out = out if isinstance(out, dict) else {}
    intent = out.get("intent") if out.get("intent") in INTENTS else "analysis"
    category = out.get("category") if out.get("category") in SPEND_CATEGORIES else None
    month = out.get("month") if out.get("month") in months else None
    keyword = out.get("keyword") or None
    return intent, keyword, category, month


def _block(tag, obj):
    return f"[{tag}] {json.dumps(obj, ensure_ascii=False, default=str)}"


def handle_message(message, df, budgets=None):
    months = sorted(df["month"].unique())
    intent, keyword, category, month = route(message, months)

    if intent == "chitchat":
        return {"answer": "Hi! Ask me things like 'How much did I spend on Swiggy?', 'Break down my spending' "
                          "or 'Am I overspending?'.",
                "intent": intent, "tools_used": [], "tables": {}, "tips": []}

    blocks, tools_used, tables, tips, note = [], [], {}, [], "none"

    if intent == "lookup":
        res = T.search_transactions(df, keyword, category, month)
        tools_used.append("search_transactions")
        if keyword and res["count"] == 0:
            # Agentic RAG: exact match failed, so retrieve similar merchants from ChromaDB
            tools_used.append("similar_merchants (ChromaDB)")
            for cand in V.similar_merchants(keyword):
                alt = T.search_transactions(df, cand, category, month)
                if alt["count"]:
                    res, note = alt, f"No exact match for '{keyword}'. Showing the closest merchant: {cand}."
                    break
        blocks.append(_block("search_transactions", res))
        tables["Matching transactions"] = pd.DataFrame(res["rows"])
    else:
        cats = T.spend_by_category(df, month)
        blocks += [
            _block("summary", T.summary(df)),
            _block("spend_by_category", {"month": month or "all months", "categories": cats}),
            _block("monthly_trend", T.monthly_trend(df)),
            _block("top_merchants", T.top_merchants(df, 5, month)),
        ]
        tools_used += ["summary", "spend_by_category", "monthly_trend", "top_merchants"]
        tables["Spending by category"] = pd.DataFrame(cats)
        tables["Monthly trend"] = pd.DataFrame(T.monthly_trend(df))

        if intent == "savings":
            flags = T.overspending_flags(df, budgets)
            blocks.append(_block("overspending_flags", flags or "no overspending flags found"))
            tools_used.append("overspending_flags")
            focus = [f["category"] for f in flags][:3] or [c["category"] for c in cats if c["category"] not in T.FIXED_CATEGORIES][:3]
            for cat in dict.fromkeys(focus):  # RAG: budgeting tips for the categories that matter
                tips += V.get_tips(cat, message, 2)
            tools_used.append("get_tips (ChromaDB)")

    answer = run_explainer(
        question=message, intent=intent, note=note,
        tool_results="\n".join(blocks),
        tips="\n".join(f"- ({t['category']}) {t['text']}" for t in tips) or "(none retrieved)",
    )
    return {"answer": answer, "intent": intent, "tools_used": tools_used, "tables": tables, "tips": tips}
