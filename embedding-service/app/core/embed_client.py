from sentence_transformers import SentenceTransformer


_embedder_instance = None


class EmbedClient:
    def __init__(self):
        self.model = SentenceTransformer(
            "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True
        )

    def embed_document(self, texts):
        formatted_texts = [
            "search_document: " + text
            for text in texts
        ]
        return self.model.encode(formatted_texts)

    def embed_input(self, text):
        return self.model.encode("search_query: " + text)


def get_embedder() -> EmbedClient:
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = EmbedClient()
    return _embedder_instance
