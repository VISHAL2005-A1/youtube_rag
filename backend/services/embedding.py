from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
def create_embeddings(texts):

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()
def create_embedding(text):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()