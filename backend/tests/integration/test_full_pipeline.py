from tests.unit.conftest import API_PREFIX
from app.crud.vectors import get_all_vector_embeddings_by_doc_id
from app.core.supabase import supabase_admin
from fastapi import status


class TestFullPipeline:
    def test_full_pipeline(
        self, client, auth_headers, sample_bot_data, sample_txt_file, sample_assistant_request
    ):
        create_bot_response = client.post(
            f"{API_PREFIX}/bots",
            json=sample_bot_data,
            headers=auth_headers
        )

        assert create_bot_response.status_code == status.HTTP_201_CREATED
        bot = create_bot_response.json()
        assert supabase_admin.table("bots").select("*").eq("bot_id", bot["bot_info"]["bot_id"]).execute()

        files = {"file": ("test.txt", sample_txt_file, "text/plain")}
        data = {
            "doc_name": "test"
        }

        create_doc_response = client.post(
            f"{API_PREFIX}/bots/{bot["bot_info"]["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )

        assert create_doc_response.status_code == status.HTTP_201_CREATED
        doc = create_doc_response.json()
        db_doc = supabase_admin.table("documents").select("*").eq("bot_id", doc["bot_id"]).eq("doc_id", doc[
            "doc_id"]).execute().data
        assert len(db_doc) == 1
        doc_list = supabase_admin.storage.from_("documents").list(f"documents/{doc['bot_id']}/")
        assert len(doc_list) > 0
        file_names = [f["name"] for f in doc_list]
        assert doc["file_name"] in file_names

        vectors_response = get_all_vector_embeddings_by_doc_id(
            doc["bot_id"],
            doc["doc_id"]
        )

        assert len(vectors_response) > 0

        for vector_embedding in vectors_response:
            assert vector_embedding["bot_id"] == doc["bot_id"]
            assert vector_embedding["doc_id"] == doc["doc_id"]

        sample_assistant_request["bot_api_key"] = bot["bot_api_key"]

        assistant_response = client.post(
            f"{API_PREFIX}/bots/{bot["bot_info"]["bot_id"]}/assistant",
            json=sample_assistant_request
        )

        assert assistant_response.status_code == status.HTTP_200_OK
        chat_message = assistant_response.json()
        print(chat_message)
        assert "message" in chat_message
        assert "role" in chat_message
        assert chat_message["role"] == "ASSISTANT"
        assert chat_message["message"].strip() != ""
