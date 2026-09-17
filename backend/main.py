from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas.chat import ChatRequest

from services.embedding import create_embedding
from services.qdrant import create_collection, search_chunks
from services.groq import generate_answer


# ==========================================
# FastAPI App
# ==========================================

app = FastAPI(
    title="YouTube Playlist RAG"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://52.207.251.20:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def format_timestamp(seconds: float):
    seconds = int(seconds)

    # hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{minutes:02d}:{seconds:02d}"

# ==========================================
# CORS
# ==========================================




# ==========================================
# Startup
# ==========================================

@app.on_event("startup")
def startup():

    create_collection()


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message": "YouTube RAG backend is running"
    }


# ==========================================
# Chat / RAG
# ==========================================

@app.post("/api/chat")
def chat(request: ChatRequest):

    try:

        # --------------------------------------
        # 1. Convert user question into embedding
        # --------------------------------------

        query_embedding = create_embedding(
            request.question
        )


        # --------------------------------------
        # 2. Search Qdrant
        # --------------------------------------

        results = search_chunks(
            query_embedding,
            limit=10
        )


        # --------------------------------------
        # 3. Check if anything was found
        # --------------------------------------

        if not results:

            return {
                "answer": (
                    "I couldn't find this information "
                    "in the provided playlist."
                ),
                "source": None
            }


        # --------------------------------------
        # 4. Debug retrieved chunks
        # --------------------------------------

        print("\n========== QDRANT RESULTS ==========")

        for i, result in enumerate(results):
            print("\nResult:", i + 1)
            print("TYPE:", type(result))
            print("VALUE:", result)

        print("====================================\n")


        # --------------------------------------
        # 5. Build transcript context
        # --------------------------------------

        context_parts = []


        for result in results:

            payload = result.payload

            context_parts.append(
                f"""
Video: {payload["video_title"]}

Timestamp: {payload["start_time"]}

Transcript:
{payload["text"]}
"""
            )


        context = "\n\n".join(
            context_parts
        )


        # --------------------------------------
        # 6. Send ONLY transcript to Groq
        # --------------------------------------

        answer = generate_answer(
            request.question,
            context
        )


        # --------------------------------------
        # 7. Get BEST source directly from Qdrant
        # --------------------------------------

        best_result = results[0]

        payload = best_result.payload


        video_id = payload["video_id"]

        video_title = payload["video_title"]

        timestamp = payload["start_time"]
        formatted_timestamp = format_timestamp(timestamp)

        score = best_result.score
       

        # --------------------------------------
        # 8. Convert timestamp to integer seconds
        # --------------------------------------

        start_time = int(timestamp)


        # --------------------------------------
        # 9. Normal YouTube URL
        # --------------------------------------

        youtube_url = (
            "https://www.youtube.com/watch?v="
            f"{video_id}"
            f"&t={start_time}s"
        )


        # --------------------------------------
        # 10. YouTube Embed URL
        # --------------------------------------

        embed_url = (
            "https://www.youtube.com/embed/"
            f"{video_id}"
            f"?start={start_time}"
        )


        # --------------------------------------
        # 11. Return answer + source
        # --------------------------------------

        return {

            "answer": answer,

            "source": {

                "video_id": video_id,

                "video_title": video_title,

                "timestamp": formatted_timestamp,

                "youtube_url": youtube_url,

                "embed_url": embed_url,

                "score": score
            }
        }


    except Exception as error:

        print(
            "Error while processing question:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )