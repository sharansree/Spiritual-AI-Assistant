from groq import Groq
from app.core.config import get_settings
from app.services.embeddings import embed_text
from app.db.client import get_db
import json

settings = get_settings()

def get_groq_client() -> Groq:
    return Groq(api_key=settings.groq_api_key)

def retrieve_relevant_suttas(question: str, top_k: int = 5) -> list[dict]:
    db = get_db()
    question_embedding = embed_text(question)
    result = db.rpc(
        'match_suttas',
        {
            'query_embedding': question_embedding,
            'match_threshold': 0.1,
            'match_count': top_k
        }
    ).execute()
    return result.data or []

def generate_response(question: str, suttas: list[dict]) -> dict:
    if not suttas:
        return {
            "answer": "I was unable to find relevant teachings for your question. Please try rephrasing it.",
            "sources": []
        }

    context = ""
    for i, sutta in enumerate(suttas, 1):
        context += f"\n[Teaching {i}]\n"
        context += f"Source: {sutta.get('title', 'Unknown')} ({sutta.get('reference', '')})\n"
        context += f"Collection: {sutta.get('collection', '')}\n"
        context += f"Text: {sutta.get('content', '')}\n"

    system_prompt = """You are a wise guide who answers questions by drawing directly from the Buddha's recorded teachings in the Pali Canon.

Your role:
- Respond with warmth, depth, and calm clarity
- Ground every part of your response in the specific teachings provided
- Cite which teaching you are drawing from using the format [Teaching N]
- Do not invent teachings or paraphrase beyond what the texts support
- Speak in clear, accessible language
- If the question involves suffering, anxiety, or difficulty, respond with compassion first
- End with one short reflection question for the person to sit with"""

    user_prompt = f"""The person has asked: "{question}"

Here are the most relevant teachings from the Pali Canon:
{context}

Please respond to their question drawing from these specific teachings. Cite your sources inline using [Teaching N] notation."""

    client = get_groq_client()
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    answer = completion.choices[0].message.content
    sources = [
        {
            "title": s.get("title", ""),
            "reference": s.get("reference", ""),
            "collection": s.get("collection", ""),
            "similarity": round(s.get("similarity", 0), 3)
        }
        for s in suttas
    ]
    return {"answer": answer, "sources": sources}

def ask_sathya(question: str, user_id: str) -> dict:
    suttas = retrieve_relevant_suttas(question)
    response = generate_response(question, suttas)
    db = get_db()
    db.table("questions").insert({
        "user_id": user_id,
        "question": question,
        "answer": response["answer"],
        "sources": json.dumps(response["sources"])
    }).execute()
    return response