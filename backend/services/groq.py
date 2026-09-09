import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")


 )
SYSTEM_PROMPT = """
You are a YouTube lecture assistant.

Your ONLY source of truth is the transcript context
provided by the application.

Rules:

1. Answer ONLY from the provided transcript.
2. Never use outside knowledge.
3. Never guess.
4. Never hallucinate.
5. If the answer is not present in the transcript, say:

   "I couldn't find this information in the provided playlist."

6. Never invent a video title.
7. Never invent a timestamp.
8. Keep the answer concise and directly related to the question.

9. IMPORTANT LANGUAGE RULE:
   Always answer in ENGLISH or HINGLISH.

   - NEVER answer in pure Hindi.
   - If the user asks in English, answer in English.
   - If the user asks in Hinglish, answer in Hinglish.
   - If the transcript is in Hindi, translate/explain the relevant
     information in English or Hinglish.
   - Do not copy Hindi sentences from the transcript unless they are
     necessary as a specific technical term or quote.
"""
def generate_answer(question, context):

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Question:

{question}


Transcript Context:

{context}
"""
            }
        ],

        temperature=0
    )

    return response.choices[0].message.content