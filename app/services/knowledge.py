import json
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parents[1] / "knowledge" / "imadi.json").read_text(encoding="utf-8"))

def retrieve(query: str, limit: int = 1):
    q = set((query or "").lower().replace("/", " ").split())
    scored = []
    for item in DATA:
        words = set(item["content"].lower().split()) | set(item["title"].lower().split())
        score = len(q & words)
        if score:
            scored.append((score, item))
    return [item for _, item in sorted(scored, key=lambda x: x[0], reverse=True)[:limit]]


def knowledge_prompt(query: str) -> str:
    docs = retrieve(query)
    if not docs:
        return "No specific verified knowledge was retrieved. Do not invent details."
    return "\n\n".join(f"SOURCE: {d['source']}\nTOPIC: {d['title']}\n{d['content']}" for d in docs)

IMADI_KNOWLEDGE = knowledge_prompt("Imadi Technologies AI automation software WhatsApp ERP SaaS")
