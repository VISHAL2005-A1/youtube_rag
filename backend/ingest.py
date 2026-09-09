import os

from services.transcript import parse_vtt, create_chunks
from services.embedding import create_embeddings
from services.qdrant import create_collection, store_chunks


TRANSCRIPT_DIR = "transcripts"

PLAYLIST_ID = "PLW4OpyGE0RdY"

BATCH_SIZE = 100


def get_transcript_files():

    files = os.listdir(TRANSCRIPT_DIR)

    hindi_files = [
        file
        for file in files
        if file.endswith(".hi.vtt")
    ]

    english_files = [
        file
        for file in files
        if file.endswith(".en.vtt")
    ]

    selected_files = []

    hindi_video_ids = set()

    for file in hindi_files:

        video_id = file.split(".")[0]

        selected_files.append(file)

        hindi_video_ids.add(video_id)

    for file in english_files:

        video_id = file.split(".")[0]

        if video_id not in hindi_video_ids:

            selected_files.append(file)

    return selected_files


def process_batch(batch):

    if not batch:
        return

    # Extract text
    texts = [
        chunk["text"]
        for chunk in batch
    ]

    # Create embeddings
    embeddings = create_embeddings(texts)

    # Upload to Qdrant
    store_chunks(
        batch,
        embeddings
    )


def main():

    print("\n========== YOUTUBE RAG INGESTION ==========\n")

    files = get_transcript_files()

    print(
        f"Found {len(files)} transcript files\n"
    )

    if not files:

        print("No .vtt transcript files found.")

        return

    create_collection()

    total_chunks = 0

    batch = []

    for index, file in enumerate(files, start=1):

        print(
            f"[{index}/{len(files)}] Processing: {file}"
        )

        file_path = os.path.join(
            TRANSCRIPT_DIR,
            file
        )

        # --------------------------------
        # Extract video ID from filename
        # --------------------------------

        video_id = file.split(".")[0]

        # --------------------------------
        # Parse transcript
        # --------------------------------

        transcript = parse_vtt(
            file_path
        )

        # --------------------------------
        # Video title
        # --------------------------------

        video_title = video_id

        # --------------------------------
        # Create chunks
        # --------------------------------

        chunk_count = 0

        for chunk in create_chunks(
            transcript,
            video_id,
            video_title,
            PLAYLIST_ID
        ):

            batch.append(chunk)

            chunk_count += 1
            total_chunks += 1

            # --------------------------------
            # Process every 100 chunks
            # --------------------------------

            if len(batch) >= BATCH_SIZE:

                process_batch(batch)

                print(
                    f"   Uploaded {len(batch)} chunks"
                )

                batch.clear()

        print(
            f"   Created chunks: {chunk_count}"
        )

    # --------------------------------
    # Process remaining chunks
    # --------------------------------

    if batch:

        process_batch(batch)

        print(
            f"   Uploaded {len(batch)} chunks"
        )

        batch.clear()

    print("\n============================================")

    print(
        f"Total chunks processed: {total_chunks}"
    )

    print("============================================\n")

    print(
        "Ingestion completed successfully!"
    )


if __name__ == "__main__":
    main()