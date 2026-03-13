from app.schemas.vectors import VectorCreate, SearchableVector, VectorSearchResponse
from app.core.supabase import supabase_admin
from typing import List

NEIGHBOR_LIMIT = 5


def create_vectors(bot_id: int, doc_id: int, vector_data: List[VectorCreate]):
    vectors_to_insert = [
        {**v.model_dump(), "bot_id": bot_id, "doc_id": doc_id}
        for v in vector_data
    ]

    response = supabase_admin.table("vectors").insert(vectors_to_insert).execute()
    return response.data


def get_vector_neighbors(bot_id: int, vector_embedding: SearchableVector):
    neighbor_query = """
        SELECT vec_id, context <-> $1 AS distance
        FROM vectors
        WHERE bot_id = $2
        ORDER BY distance
        LIMIT $3
    """

    # have to use rpc because the python client for supabase doesn't have the pgvector distance operators.
    result = supabase_admin.rpc(
        "exec_sql",
        {
            "query": neighbor_query,
            "params": [
                vector_embedding["embedding"],
                bot_id,
                NEIGHBOR_LIMIT
            ]
        }
    ).execute()

    neighbors = result.data or []

    return VectorSearchResponse(neighbors=neighbors)


def get_all_vector_embeddings_by_doc_id(bot_id: int, doc_id: int):
    result = supabase_admin.table("vectors") \
        .select("*") \
        .eq("bot_id", bot_id) \
        .eq("doc_id", doc_id) \
        .execute()

    return result.data