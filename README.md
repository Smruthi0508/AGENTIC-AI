# 💸 Finora
### Your bank statement, turned into a clearer picture of your money.

Finora is a personal-finance dashboard for **bank and UPI statements in CSV format**. Explore spending and income, understand where your money goes, set budgets, and ask an AI assistant questions about your transactions.

> 🔒 Your statement is analysed by this app. Keep your Gemini API key private and never commit it to source control.

---

## ✨ What you can do

| Feature | What it shows |
|---|---|
| 📊 **Money overview** | Total spending, income, net cash flow, and transaction count |
| 🧾 **Spending breakdown** | Category totals and each category’s share of spending |
| 📈 **Monthly trends** | Compare monthly spending with income |
| 🏪 **Merchant insights** | See your top merchants and search statement transactions |
| 💬 **Ask the money copilot** | Ask questions about merchants, categories, trends, or saving |
| 🎯 **Budget alerts** | Add optional monthly budgets and get overspending insights |
| 🧠 **Merchant matching** | ChromaDB can find similar merchants when an exact search misses |
| 💡 **Savings tips** | Retrieve relevant budgeting tips for savings questions |

### Example questions

- “How much did I spend on Swiggy?”
- “Where is my money going?”
- “Show my transport spending in 2026-09.”
- “Am I overspending? Give me tips to save.”

> 🧮 **Numbers are grounded in code:** pandas tools calculate financial figures; Gemini interprets the question and explains the results.

---

## 🚀 Get started

### 1. Install the dependencies

Run these commands from the project folder:

```powershell
python -m pip install -r requirements.txt
```

### 2. Configure Gemini (optional, required for AI features)

Create a file named **`.env`** beside `app.py` and add your own Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace `your_gemini_api_key` with your key. Do not include quotes unless required by your environment.

🔐 **Keep `.env` private.** It is listed in `.gitignore`. Never paste your API key into chat, screenshots, source code, or a commit.

Without a key, you can still load statements and use the dashboard’s pandas-based analytics. **AI chat and Gemini-based categorisation need a working key and an available model.**

### 3. Build the tips index

Run this once to load the budgeting tips into ChromaDB:

```powershell
python build_index.py
```

### 4. Start Finora

```powershell
python -m streamlit run app.py
```

Open the **Local URL** shown in the terminal (usually `http://localhost:8501`). In the sidebar, click **Use sample statement** or upload your own CSV.

### 5. Try the accuracy script (optional)

```powershell
python test_accuracy.py
```

This script measures category predictions against labels for the synthetic sample. It may call Gemini for unknown merchants, so results can vary with model availability and API configuration.

---

## 📄 CSV statement requirements

Upload a `.csv` file with column headings that the parser can recognise:

| Required information | Recognised heading examples |
|---|---|
| 📅 Transaction date | `Date`, `Transaction Date` |
| 📝 Transaction description | `Description`, `Narration`, `Particulars`, `Details`, `Remarks` |
| 💰 Transaction amount | Separate `Debit` / `Credit` columns, or one signed `Amount` column |

For a single signed amount column, **negative means money out** and **positive means money in**. Dates are parsed using day-first handling. Rows without a parseable date are skipped.

> ✅ CSV is supported today. PDF statements and other file formats are not.

---

## 🧭 How the app works

```text
CSV statement
     ↓
Parser detects date, description, debit and credit
     ↓
Categoriser applies merchant rules → Gemini for unknown merchants
     ↓
Question router selects lookup, analysis, savings, or chitchat
     ↓
Pandas tools compute the figures ──→ ChromaDB retrieves relevant tips/merchants
     ↓
Gemini explains the tool results in plain language
```

### Project map

| File | Responsibility |
|---|---|
| `app.py` | Streamlit dashboard, upload, budgets, charts, and chat |
| `ingest.py` | CSV parsing, column detection, and transaction categorisation |
| `categories.py` | Spending categories and keyword-based merchant rules |
| `agents.py` | Intent routing and orchestration of tools and retrieval |
| `tools.py` | Deterministic spending, trend, lookup, and budget calculations |
| `llm.py` | Gemini client and API-key configuration |
| `chains.py` | LangChain prompt/model/output-parser pipelines |
| `prompts.py` | Router, categoriser, and answer-generation prompts |
| `vectors.py` | ChromaDB tips and merchant similarity search |
| `build_index.py` | Builds the budgeting tips collection |
| `data/sample_statement.csv` | Synthetic sample bank statement |
| `data/sample_labels.csv` | Expected categories for sample accuracy checks |
| `data/budget_tips.json` | Tips indexed for savings answers |

---

## ⚠️ Notes and limitations

- 📁 Only CSV statements are supported; there is no PDF parsing.
- 🇮🇳 Merchant rules are tuned for Indian transactions; unknown merchants may need Gemini categorisation.
- 🧪 Sample statement data is synthetic and intended for demonstration.
- 🌐 Gemini requests require internet access, a valid API key, and a model available to your account.
- 💡 Insights are general budgeting information, **not financial advice**.
