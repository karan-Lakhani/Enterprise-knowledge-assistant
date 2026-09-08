import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(
    question,
    retrieved_chunks
):
    if isinstance(retrieved_chunks, str):
        retrieved_chunks = [retrieved_chunks]

    if not retrieved_chunks:
        return "I could not find this information in the knowledge base."

    context = "\n\n".join(
        f"[Retrieved chunk {index}]\n{chunk}"
        for index, chunk in enumerate(retrieved_chunks, start=1)
    )

    prompt = f"""
You are an Enterprise Knowledge Assistant.

Answer the question using factual statements from the retrieved chunks below.
The chunks can contain unrelated information. Find and use a direct answer when
one is present; do not return the fallback merely because other chunks are irrelevant.
Keep the answer concise and include any conditions or thresholds stated in the context.

Only if no retrieved chunk contains the answer, say exactly:

I could not find this information in the knowledge base.

Retrieved chunks:
{context}

Question:
{question}
"""

    print(f"\nRetrieved chunks passed to Gemini: {len(retrieved_chunks)}")
    print(f"Context length: {len(context)}")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text
