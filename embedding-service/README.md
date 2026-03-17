# Embedding Service API

## Use Case

The point of this API is to make embeddings of documents or text. This is done through possibly chunking the data with a
semantic chunker and then making embeddings of each chunk. These values are then passed back to the calling user.


## Calling the API

### Terminal

To call from terminal you can use the following command with various modifications:
```
curl -X POST {API_PREFIX}/{ENDPOINT_ROUTE} -H "Content-Type: application/json"  -H "X-API-Key: {API_KEY}" -d '{ROUTE_OBJECT}'
```

### Calling the endpoint (python)

to call from code (with possible variation), using python, you can use the following code to call it:
```
response = client.{ROUTE_TYPE}(
            f"{API_PREFIX}/{ENDPOINT_ROUTE}",
            json={ROUTE_OBJECT},
            headers={API_KEY}
        )
```

### Key

API_PREFIX: Where the API is hosted. If hosted locally it should look something like "http://localhost:{port}/api/v1/"<br>

ENDPOINT_ROUTE: The route that the chosen endpoint states. ex - "embed/str" <br>

API_KEY: This is needed to be passed to use the API. It is decided by the host of the API.<br>

ROUTE_OBJECT: What is needing to be passed to the route<br>

ROUTE_TYPE: The type of operation the route does. It is described by the route. ex: get, post, patch <br>

## ROUTES

### Embed User Input
Creates an embedding for user input. This is a different operation compared to embedding a string. Keep this in mind.

Type: post <br>
Route: /user_input <br>
Expected Parameter: {"user_input": "type-str"} <br>
Expected Response: {"chunk"="type-str","embedding"=[{embedding_float_vals}]}

Example Call:
```
response = client.post(
            f"{API_PREFIX}/embed/user_input",
            json={"user_input": "What is a user input?"},
            headers=test_api_key
        )
```

### Embed Txt Document
Creates an embedding for a text document. Unlike the other routes, this document will be semantically chunked before
embedding, meaning the response will contain multiple embedding objects. Keep this in mind.

Type: post <br>
Route: /txt <br>
Expected Parameter: {"document": "type-str"} <br>
Expected Response: {"embedding_objects"=[{"chunk"="type-str","embedding"=[{embedding_float_vals}]}]} <br>
Note: Document size is limited by the host configured MAX_DOCUMENT_SIZE.

Example Call:
```
response = client.post(
            f"{API_PREFIX}/embed/txt",
            json={"document": "This is an example document. It contains multiple sentences for chunking."},
            headers=test_api_key
        )
```

### Embed String
Creates an embedding for a string. This can be used for finetuning what a bot knows. This is a different operation 
compared to embedding a user input. Keep this in mind.

Type: post <br>
Route: /str <br>
Expected Parameter: {"string": "type-str"} <br>
Expected Response: {"chunk"="type-str","embedding"=[{embedding_float_vals}]} <br>
Note: String size is limited by the host configured MAX_STRING_SIZE_CHAR.

Example Call:
```
response = client.post(
            f"{API_PREFIX}/embed/str",
            json={"string": "This is an example string to embed."},
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

