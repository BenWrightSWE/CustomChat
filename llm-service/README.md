
# LLM Service API

## Use Case

Provides an LLM response for a chatbot based on a RAG pipeline. Hence, the need for input_context.

## Calling the API

### Terminal

To call from terminal you can use the following command with various modifications:
```
curl -X POST {API_PREFIX}/{ENDPOINT_ROUTE} -H "Content-Type: application/json"  -H "X-API-Key: {API_KEY}" -d '{ROUTE_OBJECT}'
```

### Calling the endpoint (python)

To call from code (with possible variation), using python, you can use the following code to call it:
```
response = client.{ROUTE_TYPE}(
            f"{API_PREFIX}/{ENDPOINT_ROUTE}",
            json={ROUTE_OBJECT},
            headers={API_KEY}
        )
```

### Key

API_PREFIX: Where the API is hosted. If hosted locally it should look something like "http://localhost:{port}/api/v1/"<br>

ENDPOINT_ROUTE: The route that the chosen endpoint states. ex - "llm/response" <br>

API_KEY: This is needed to be passed to use the API. It is decided by the host of the API.<br>

ROUTE_OBJECT: What is needing to be passed to the route<br>

ROUTE_TYPE: The type of operation the route does. It is described by the route. ex: get, post, patch <br>

## ROUTES

### LLM Response
Generates an LLM response given a user input, chat history, and input context. Input context is limited to a
maximum of 5 documents. Keep this in mind.

Type: post <br>
Route: /response <br>
Expected Parameter: {"chat_history"=[{"role": "type-str", "message": "type-str"}], "input_context"=["type-str"], "user_input": "type-str"} <br>
Expected Response: {"response": "type-str"} <br>
Note: user_input cannot be empty. input_context is limited to a max of 5 documents.

Example Call:
```
response = client.post(
            f"{API_PREFIX}/llm/response",
            json={
                "chat_history": [
                    {"role": "user", "message": "Hello!"},
                    {"role": "assistant", "message": "Hi, how can I help you?"}
                ],
                "input_context": ["This is a context document."],
                "user_input": "What can you tell me about the context?"
            },
            headers=test_api_key
        )
```

## Additional Routes

### Health Check
Returns the health status of the API.

Type: get <br>
Route: /health <br>
Expected Parameter: None <br>
Expected Response: {"status": "ok"}

Example Call:
```
response = client.get(
            f"{API_PREFIX}/health",
            headers=test_api_key
        )
```