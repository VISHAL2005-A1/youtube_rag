import os
import uuid

from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
   
)


load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION",
    "youtube_playlist_chunks"
)


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=120
)
def create_collection():

    collections = client.get_collections()

    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections.collections
    )

    if exists:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )
def store_chunks(chunks, embeddings):

    points = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        point = PointStruct(

            id=str(uuid.uuid4()),

            vector=embedding,

            payload={
                "text": chunk["text"],
                "video_id": chunk["video_id"],
                "video_title": chunk["video_title"],
                "playlist_id": chunk["playlist_id"],
                "start_time": chunk["start_time"]
            }
        )

        points.append(point)

    # Upload in batches
    batch_size = 100

    for i in range(
        0,
        len(points),
        batch_size
    ):

        batch = points[
            i:i + batch_size
        ]

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )

        uploaded = min(
            i + batch_size,
            len(points)
        )

        print(
            f"Uploaded {uploaded}/{len(points)} points"
        )   

def search_chunks(
    query_embedding,
    limit=10,
    # score_threshold=0.45
):
   

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        # query_filter=playlist_filter,
        limit=limit,
        # score_threshold=score_threshold,
        with_payload=True
    )
    return results.points   

