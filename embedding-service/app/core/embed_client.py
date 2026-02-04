from sentence_transformers import SentenceTransformer


class EmbedClient:
    def __init__(self):
        self.document_model = SentenceTransformer(
            "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True
        )
        self.input_model = SentenceTransformer(
            "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True
        )

    def embed_document(self, texts):
        return self.document_model.encode(texts)

    def embed_input(self, text):
        return self.input_model.endcode(text)
