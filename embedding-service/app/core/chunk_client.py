import semchunk
from transformers import AutoTokenizer


# possibly reduce to 256 or increase to 1024
CHUNK_SIZE = 512

_chunker_instance = None


class ChunkClient:
    def __init__(self):
        self.neox_chunker = semchunk.chunkerify("EleutherAI/gpt-neox-20b", CHUNK_SIZE) or \
            semchunk.chunkerify(AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b"), CHUNK_SIZE) or \
            semchunk.chunkerify(lambda text: len(text.split()), CHUNK_SIZE)

    def chunk_document(self, document_text):
        return self.neox_chunker(document_text)


def get_chunker() -> ChunkClient:
    global _chunker_instance
    if _chunker_instance is None:
        _chunker_instance = ChunkClient()
    return _chunker_instance

