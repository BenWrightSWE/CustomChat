from app.schemas.vectors import VectorCreate, VectorSearch
from app.core.supabase import supabase_admin

NEIGHBOR_LIMIT = 5


def create_vector(bot_id: int, doc_id: int, vector_data: VectorCreate):
    vec_dict = vector_data.model_dump()
    vec_dict["bot_id"] = bot_id
    vec_dict["doc_id"] = doc_id

    response = supabase_admin.table("vectors").insert(vec_dict).execute()
    return response.data[0]


def get_vector_neighbors(doc_id: int, vector_embedding: VectorSearch):
    query = """
        WITH relaxed_results AS MATERIALIZED (
            SELECT vec_id, context, embedding <-> %s 
            AS distance 
            FROM vectors 
            WHERE doc_id = %s
            ORDER BY distance LIMIT %s
        ) 
        SELECT * FROM relaxed_results ORDER BY distance + 0;
    """

    result = supabase_admin.rpc('exec_sql', {
        'query': query,
        'params': [vector_embedding["embedding"], doc_id, NEIGHBOR_LIMIT]
    }).execute()

    return result.data