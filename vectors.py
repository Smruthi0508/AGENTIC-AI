"""ChromaDB: budgeting tips (built once) + merchant embeddings (rebuilt per uploaded statement)."""
from threading import RLock

import chromadb

_client = chromadb.PersistentClient(path="chroma_db")
_merchant_index_lock = RLock()


def index_merchants(df):
    m = df[df["debit"] > 0].drop_duplicates("merchant")
    with _merchant_index_lock:
        col = _client.get_or_create_collection("txns")
        existing_ids = col.get()["ids"]
        if existing_ids:
            col.delete(ids=existing_ids)
        if len(m):
            col.add(ids=[str(i) for i in range(len(m))], documents=m["merchant"].tolist(),
                    metadatas=[{"category": c} for c in m["category"]])


def similar_merchants(query, n=3):
    """Fuzzy lookup: finds 'SWIGGY' for 'swigy' or 'food delivery'."""
    with _merchant_index_lock:
        try:
            col = _client.get_collection("txns")
        except Exception:
            return []
        res = col.query(query_texts=[query], n_results=n)
        return res["documents"][0]


def get_tips(category, query, n=2):
    try:
        col = _client.get_collection("finance_tips")
    except Exception:
        raise RuntimeError("Tips index not found. Run: python build_index.py")
    res = col.query(query_texts=[query], n_results=n, where={"category": category})
    return [{"text": d, "category": m["category"]} for d, m in zip(res["documents"][0], res["metadatas"][0])]
