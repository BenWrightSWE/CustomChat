from tests.unit.conftest import API_PREFIX, TEST_TXT_SIZE
from fastapi import status
class TestIngestionPipeline:
    def test_ingestion_pipeline_txt(
            self, client, auth_headers, sample_bot_data, sample_txt_file
    ):
        create_bot_response = client.post(
            f"{API_PREFIX}/bots",
            json=sample_bot_data,
            headers=auth_headers
        )

        assert create_bot_response.status_code == status.HTTP_201_CREATED
        bot = create_bot_response.json()

        files = {"file": ("test.txt", sample_txt_file, "text/plain")}
        data = {
            "doc_name": "test",
            "doc_type": ".txt",
            "doc_size": TEST_TXT_SIZE
        }

        create_doc_response = client.post(
            f"{API_PREFIX}/bots/{bot["bot_info"]["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )
