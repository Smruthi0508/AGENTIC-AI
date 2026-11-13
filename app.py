import html

import pandas as pd
import streamlit as st

import tools as T
import vectors as V
from agents import handle_message
from ingest import categorize, load_statement
from llm import is_llm_configured
from prompts import CATEGORIZER_SYSTEM, EXPLAINER_SYSTEM, ROUTER_SYSTEM

st.set_page_config(page_title="Finora | Money dashboard", page_icon="💸", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #172b25;
        --muted: #71817a;
        --green: #187653;
        --line: #e6ece8;
        --surface: #ffffff;
        --canvas: #f5f8f6;
    }
    .stApp { background: var(--canvas); color: var(--ink); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 1440px;
        padding: 2rem 3rem 4rem;
    }
    [data-testid="stSidebar"] {
        background: #fff;
        border-right: 1px solid var(--line);
        color: var(--ink) !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: var(--ink) !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: var(--muted) !important;
    }
    h1, h2, h3, [data-testid="stMetricValue"] {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
    }
    p, label, .stCaption { font-family: 'DM Sans', sans-serif; }
    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 3px 12px rgba(27, 55, 42, .035);
    }
    [data-testid="stMetricLabel"] p {
        color: var(--muted);
        font-size: .82rem;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] { font-size: 1.65rem; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface);
        border-color: var(--line);
        border-radius: 18px;
        box-shadow: 0 3px 12px rgba(27, 55, 42, .035);
    }
    div.stButton > button,
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"] {
        border-radius: 10px;
        font-weight: 600;
        transition: all .15s ease;
    }
    [data-testid="stBaseButton-primary"] {
        background: var(--green) !important;
        border-color: var(--green) !important;
        color: #fff !important;
    }
    [data-testid="stBaseButton-primary"] *,
    [data-testid="stBaseButton-secondary"] * {
        color: inherit !important;
    }
    div.stButton > button[data-testid="stBaseButton-primary"] p,
    div.stButton > button[data-testid="stBaseButton-primary"] span,
    div.stButton > button[data-testid="stBaseButton-primary"] div {
        color: #fff !important;
        -webkit-text-fill-color: #fff !important;
    }
    div.stButton > button[data-testid="stBaseButton-secondary"] p,
    div.stButton > button[data-testid="stBaseButton-secondary"] span,
    div.stButton > button[data-testid="stBaseButton-secondary"] div {
        color: #173c2c !important;
        -webkit-text-fill-color: #173c2c !important;
    }
    [data-testid="stBaseButton-secondary"] {
        background: #eaf3ed !important;
        border: 1px solid #d5e5da !important;
        color: #173c2c !important;
    }
    [data-testid="stBaseButton-primary"]:hover {
        background: #126345 !important;
        border-color: #126345 !important;
        color: #fff !important;
    }
    [data-testid="stBaseButton-secondary"]:hover {
        background: #dcece2 !important;
        border-color: #a9cbb6 !important;
        color: #123b29 !important;
    }
    [data-testid="stFileUploader"] {
        background: #f8faf9;
        border-radius: 12px;
    }
    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 16px;
        background: #fff;
        padding: .8rem 1rem;
        color: var(--ink) !important;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
        color: var(--ink) !important;
    }
    [data-testid="stChatInput"] {
        border-color: #dce6e0;
        border-radius: 14px;
        background: #fff !important;
    }
    [data-testid="stChatInput"] textarea {
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #71817a !important;
        -webkit-text-fill-color: #71817a !important;
        opacity: 1;
    }
    .brand {
        display: flex; align-items: center; gap: .65rem;
        margin: 0 0 1.8rem; color: var(--ink);
        font: 800 1.28rem 'Manrope', sans-serif; letter-spacing: -.04em;
    }
    .brand-mark {
        display: grid; place-items: center; width: 36px; height: 36px;
        border-radius: 11px; color: white; background: var(--green);
        font-size: 1.05rem;
    }
    .eyebrow {
        color: var(--green); font: 700 .72rem 'DM Sans', sans-serif;
        letter-spacing: .12em; text-transform: uppercase; margin-bottom: .45rem;
    }
    .hero-title {
        font: 800 clamp(1.8rem, 3vw, 2.45rem)/1.15 'Manrope', sans-serif;
        letter-spacing: -.055em; color: var(--ink); margin: 0;
    }
    .hero-subtitle {
        color: var(--muted); font: 400 1rem 'DM Sans', sans-serif;
        margin-top: .65rem;
    }
    .status-pill {
        display: inline-flex; align-items: center; gap: .45rem;
        background: #e8f4ee; color: #176444; border-radius: 999px;
        padding: .5rem .8rem; font: 700 .75rem 'DM Sans', sans-serif;
        white-space: nowrap;
    }
    .section-heading {
        color: var(--ink); font: 700 1.12rem 'Manrope', sans-serif;
        letter-spacing: -.025em; margin: .25rem 0 .2rem;
    }
    .section-copy { color: var(--muted); font: .88rem 'DM Sans', sans-serif; }
    .empty-state {
        text-align: center; padding: 4rem 1.5rem;
        border: 1px dashed #cbd9d0; border-radius: 22px;
        background: linear-gradient(145deg, #fff 5%, #f0f7f2 100%);
    }
    .empty-icon {
        display: inline-grid; place-items: center; width: 64px; height: 64px;
        background: #e5f2ea; color: var(--green); border-radius: 20px;
        font-size: 1.8rem; margin-bottom: 1rem;
    }
    .empty-title {
        color: var(--ink); font: 800 1.5rem 'Manrope', sans-serif;
        letter-spacing: -.04em;
    }
    .empty-copy {
        color: var(--muted); font: 1rem 'DM Sans', sans-serif;
        max-width: 520px; margin: .55rem auto 1rem;
    }
    @media (max-width: 760px) {
        [data-testid="stAppViewContainer"] .main .block-container {
            padding: 1.25rem 1rem 2.5rem;
        }
        .hero-title { font-size: 1.8rem; }
        .stHorizontalBlock:has([data-testid="stMetric"]) {
            flex-wrap: wrap !important;
            gap: .65rem;
        }
        .stHorizontalBlock:has([data-testid="stMetric"]) > [data-testid="column"] {
            flex: 1 1 calc(50% - .65rem) !important;
            min-width: calc(50% - .65rem) !important;
        }
        .stHorizontalBlock:not(:has([data-testid="stMetric"])) > [data-testid="column"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

ss = st.session_state
ss.setdefault("messages", [])
ss.setdefault("df", None)
ss.setdefault("loaded", None)
ss.setdefault("pending_question", None)


def load(source, name):
    with st.spinner("Parsing and categorising transactions..."):
        llm_available = is_llm_configured()
        df = categorize(load_statement(source), use_llm=llm_available)
        try:
            V.index_merchants(df)
            merchant_index_error = None
        except Exception as error:
            merchant_index_error = error
    ss.df, ss.loaded, ss.messages = df, name, []
    ss.llm_available = llm_available
    if merchant_index_error:
        st.warning(f"Merchant similarity search is unavailable: {merchant_index_error}")
    if df.attrs.get("llm_error"):
        st.warning(f"AI categorisation could not run; unmatched merchants were marked 'Other'. {df.attrs['llm_error']}")


def show_tables(tables):
    if tables:
        with st.expander("See the data behind this answer"):
            for title, table in tables.items():
                st.caption(title)
                st.dataframe(table, use_container_width=True, hide_index=True)


with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">₹</span> finora</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">YOUR WORKSPACE</div>', unsafe_allow_html=True)
    st.subheader("Statement")
    st.caption("Upload a bank or UPI statement to get started.")
    upload = st.file_uploader("CSV file", type="csv", label_visibility="collapsed")
    if st.button("Use sample statement", use_container_width=True, type="primary"):
        load("data/sample_statement.csv", "Sample statement")
    if upload is not None and ss.loaded != upload.name:
        try:
            load(upload, upload.name)
        except Exception as error:
            st.error(f"Could not read the file: {error}")

    if ss.loaded:
        st.success(f"Loaded: {ss.loaded}")
    if ss.loaded and not is_llm_configured():
        st.info("AI chat and merchant categorisation need a Google Gemini API key. Add GOOGLE_API_KEY to your .env file and restart the app. Dashboard analytics work without it.")

    st.divider()
    st.subheader("Monthly budgets")
    st.caption("Optional limits used for overspending alerts.")
    budgets = {}
    for category in ["Food & Dining", "Shopping", "Entertainment", "Transport"]:
        value = st.number_input(category, min_value=0, step=500, value=0, key=f"budget_{category}")
        if value > 0:
            budgets[category] = value

    with st.expander("How the assistant works"):
        st.caption("Router · categoriser · advisor")
        for title, prompt_text in [
            ("Router prompt", ROUTER_SYSTEM),
            ("Categoriser prompt", CATEGORIZER_SYSTEM),
            ("Advisor prompt", EXPLAINER_SYSTEM),
        ]:
            st.caption(title)
            st.code(prompt_text, language="text")

df = ss.df
if df is None:
    st.markdown(
        """
        <div class="empty-state">
          <div class="empty-icon">✦</div>
          <div class="eyebrow">YOUR MONEY, MADE CLEAR</div>
          <div class="empty-title">A clearer view of your finances starts here.</div>
          <div class="empty-copy">Upload a bank or UPI CSV statement from the sidebar, or explore the dashboard with sample data to see where your money goes.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

summary = T.summary(df)
safe_name = html.escape(str(ss.loaded or "Statement"))
start_date = df["date"].min().strftime("%d %b %Y")
end_date = df["date"].max().strftime("%d %b %Y")
st.markdown(
    f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:1rem;margin:.5rem 0 1.6rem;flex-wrap:wrap">
      <div>
        <div class="eyebrow">PERSONAL FINANCE OVERVIEW</div>
        <h1 class="hero-title">Your money, at a glance.</h1>
        <div class="hero-subtitle">{start_date} – {end_date} &nbsp;·&nbsp; {safe_name}</div>
      </div>
      <div class="status-pill">● &nbsp; STATEMENT READY</div>
    </div>
    """,
    unsafe_allow_html=True,
)

rules_pct = (df["category_source"] == "rules").mean() * 100
metric_columns = st.columns(4)
for column, label, value, help_text in [
    (metric_columns[0], "Total spending", f"₹{summary['total_spend']:,.0f}", "Total debits in this statement"),
    (metric_columns[1], "Money in", f"₹{summary['total_income']:,.0f}", "Total credits in this statement"),
    (
        metric_columns[2],
        "Net cash flow",
        f"{'-' if summary['net_savings'] < 0 else ''}₹{abs(summary['net_savings']):,.0f}",
        "Income minus spending",
    ),
    (metric_columns[3], "Transactions", f"{summary['spend_transactions']:,}", f"{rules_pct:.0f}% categorised by rules"),
]:
    with column:
        st.metric(label, value, help=help_text)

st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
chart_left, chart_right = st.columns([1, 1], gap="large")
category_totals = pd.DataFrame(T.spend_by_category(df))
monthly_totals = pd.DataFrame(T.monthly_trend(df))

with chart_left:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Spending by category</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-copy">See what is taking the biggest share.</div>', unsafe_allow_html=True)
        if category_totals.empty:
            st.info("No spending transactions found in this statement.")
        else:
            st.bar_chart(category_totals, x="category", y="amount", color="#187653", use_container_width=True)
            st.dataframe(
                category_totals[["category", "amount", "share_percent"]].rename(
                    columns={"category": "Category", "amount": "Spent (₹)", "share_percent": "Share (%)"}
                ),
                use_container_width=True,
                hide_index=True,
            )

with chart_right:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Income & spending trend</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-copy">Monthly cash flow across your statement.</div>', unsafe_allow_html=True)
        st.line_chart(monthly_totals.set_index("month")[["spend", "income"]], color=["#187653", "#94b9a5"])
        merchant_totals = pd.DataFrame(T.top_merchants(df, 5))
        if merchant_totals.empty:
            st.info("No merchants with spending found.")
        else:
            st.markdown('<div class="section-heading" style="font-size:.98rem;margin-top:.7rem">Top merchants</div>', unsafe_allow_html=True)
            st.dataframe(
                merchant_totals.rename(
                    columns={"merchant": "Merchant", "amount": "Spent (₹)", "transactions": "Transactions"}
                ),
                use_container_width=True,
                hide_index=True,
            )

st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown('<div class="section-heading">Recent transactions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">A quick look at the latest activity in your statement.</div>', unsafe_allow_html=True)
    recent = df.sort_values("date", ascending=False).head(8).copy()
    recent["Date"] = recent["date"].dt.strftime("%d %b %Y")
    recent["Amount (₹)"] = recent.apply(
        lambda row: row["credit"] if row["credit"] > 0 else -row["debit"], axis=1
    )
    recent["Type"] = recent.apply(lambda row: "Income" if row["credit"] > 0 else "Expense", axis=1)
    st.dataframe(
        recent[["Date", "merchant", "description", "category", "Amount (₹)", "Type"]].rename(
            columns={"merchant": "Merchant", "description": "Description", "category": "Category"}
        ),
        use_container_width=True,
        hide_index=True,
    )

st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown('<div class="section-heading">Ask your money copilot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Get a grounded answer based on your statement.</div>', unsafe_allow_html=True)
    suggestions = st.columns(3)
    starter_questions = [
        "Where is my money going?",
        "How much did I spend on Swiggy?",
        "Am I overspending?",
    ]
    for column, question in zip(suggestions, starter_questions):
        with column:
            if st.button(question, use_container_width=True, key=f"ask_{question}"):
                ss.pending_question = question

    for message in ss.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("intent"):
                st.caption(f"{message['intent'].title()} · Tools: {', '.join(message['tools_used']) or 'none'}")
            show_tables(message.get("tables"))

    typed_question = st.chat_input("Ask about spending, merchants, trends, or ways to save...")
    question = ss.pending_question or typed_question
    if question:
        ss.pending_question = None
        ss.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Looking through your statement..."):
                if not is_llm_configured():
                    result = {
                        "answer": "AI chat needs a Google Gemini API key. Add GOOGLE_API_KEY to your .env file and restart the app. Your dashboard and transaction analytics are still available.",
                        "intent": "setup",
                        "tools_used": [],
                        "tables": {},
                        "tips": [],
                    }
                else:
                    try:
                        result = handle_message(question, df, budgets)
                    except Exception as error:
                        st.error(f"The assistant could not complete that request: {error}")
                        result = {
                            "answer": "I couldn't complete that request just now. Please try again.",
                            "intent": "error",
                            "tools_used": [],
                            "tables": {},
                            "tips": [],
                        }
            st.markdown(result["answer"])
            if result.get("intent"):
                st.caption(f"{result['intent'].title()} · Tools: {', '.join(result['tools_used']) or 'none'}")
            show_tables(result.get("tables"))
        ss.messages.append(
            {
                "role": "assistant",
                "content": result["answer"],
                "intent": result["intent"],
                "tools_used": result["tools_used"],
                "tables": result["tables"],
            }
        )
        st.rerun()
