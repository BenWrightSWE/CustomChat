from tests.unit.conftest import API_PREFIX
from app.crud.documents import create_document
from app.crud.vectors import get_vector_neighbors, create_vectors
from app.schemas.vectors import VectorCreate
from app.core.supabase import supabase_admin
from fastapi import status


class TestQueryPipeline:
    def test_query_pipeline(
        self,
        client,
        auth_headers,
        sample_bot_data,
        sample_injectable_doc,
        sample_injectable_embedding_objects,
        sample_assistant_request,
    ):
        # create a bot
        create_bot_response = client.post(
            f"{API_PREFIX}/bots", json=sample_bot_data, headers=auth_headers
        )

        assert create_bot_response.status_code == status.HTTP_201_CREATED
        bot = create_bot_response.json()
        assert (
            supabase_admin.table("bots")
            .select("*")
            .eq("bot_id", bot["bot_info"]["bot_id"])
            .execute()
        )

        doc_response = create_document(bot["bot_info"]["bot_id"], sample_injectable_doc)

        # inject the vectors for bot
        vector_objects = [
            VectorCreate(context=obj["chunk"], embedding=obj["embedding"])
            for obj in sample_injectable_embedding_objects
        ]
        create_vectors(
            bot["bot_info"]["bot_id"], doc_response["doc_id"], vector_objects
        )

        # create response using said vectors
        sample_assistant_request["bot_api_key"] = bot["bot_api_key"]

        assistant_response = client.post(
            f"{API_PREFIX}/bots/{bot["bot_info"]["bot_id"]}/assistant",
            json=sample_assistant_request,
        )

        # check if response has some basis for the response
        assert assistant_response.status_code == status.HTTP_200_OK
        chat_message = assistant_response.json()
        print(chat_message)
        assert "message" in chat_message
        assert chat_message["message"].strip() != ""
        assert "Athens" in chat_message["message"]
        assert "role" in chat_message
        assert chat_message["role"] == "ASSISTANT"
