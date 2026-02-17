from app.schemas.vectors import VectorCreate, SearchableVector
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
        WITH relaxed_results AS MATERIALIZED (
            SELECT vec_id, context, embedding <-> %s 
            AS distance 
            FROM vectors 
            WHERE bot_id = %s
            ORDER BY distance LIMIT %s
        ) 
        SELECT * FROM relaxed_results ORDER BY distance + 0;
    """

    result = supabase_admin.rpc('exec_sql', {
        'query': neighbor_query,
        'params': [vector_embedding["embedding"], bot_id, NEIGHBOR_LIMIT]
    }).execute()

    return result.data