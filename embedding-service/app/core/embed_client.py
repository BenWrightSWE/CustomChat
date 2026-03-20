from sentence_transformers import SentenceTransformer


_embedder_instance = None


class EmbedClient:
    def __init__(self):
        """initializes and specifies the embedding model"""
        self.model = SentenceTransformer(
            "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True
        )

    def embed_document(self, texts):
        """embeddings for a list of strings"""
        formatted_texts = [
            "search_document: " + text
            for text in texts
        ]
        return self.model.encode(formatted_texts)

    def embed_text(self, text):
        """embedding for specifically a single string. This is different than user input due to formatting."""
        formatted_text = [
            "search_document: " + text
        ]
        return self.model.encode(formatted_text)

    def embed_input(self, text):
        """embedding for a user input. This is different than a single string due to formatting."""
        return self.model.encode("search_query: " + text)


def get_embedder() -> EmbedClient:
    """Singleton for the embedder so that only one embedder instance is created"""
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = EmbedClient()
    return _embedder_instance
