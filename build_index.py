"""Run once: loads budgeting tips into ChromaDB."""
import json
from pathlib import Path

import chromadb

tips = json.loads((Path(__file__).parent / "data" / "budget_tips.json").read_text(encoding="utf-8"))
client = chromadb.PersistentClient(path="chroma_db")
try:
    client.delete_collection("finance_tips")
except Exception:
    pass
col = client.create_collection("finance_tips")
col.add(ids=[t["id"] for t in tips], documents=[t["tip"] for t in tips],
        metadatas=[{"category": t["category"]} for t in tips])
print(f"Indexed {len(tips)} budgeting tips into chroma_db/")
