# CustomChat Service API

## Use Case

This API allows you to access any data or services needed for the RAG project. 

## Calling the API

### Terminal

To call from terminal you can use the following command with various modifications:
```
curl -X {ROUTE_TYPE} {API_PREFIX}/{ENDPOINT_ROUTE} -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" -d '{ROUTE_OBJECT}'
```

### Calling the endpoint (python)

To call from code (with possible variation), using python, you can use the following code to call it:
```
response = client.{ROUTE_TYPE}(
            f"{API_PREFIX}/{ENDPOINT_ROUTE}",
            json={ROUTE_OBJECT},
            headers={AUTH_TOKEN}
        )
```

### Key

API_PREFIX: Where the API is hosted. If hosted locally it should look something like "http://localhost:{port}/api/v1"<br>

ENDPOINT_ROUTE: The route that the chosen endpoint states. ex - "bots/1/assistant" <br>

AUTH_TOKEN: This is needed to be passed to use the API for authenticated routes. It is a user level bearer token
decided by the auth provider.<br>

ROUTE_OBJECT: What is needing to be passed to the route<br>

ROUTE_TYPE: The type of operation the route does. It is described by the route. ex: get, post, patch, delete <br>

## ROUTES

### Assistant

#### Bot Contextual Response
Generates a contextual response from a bot given a user input and chat history. The bot uses its stored documents
to retrieve relevant context before generating a response. This route uses a bot level API key, not a user level
auth token. Keep this in mind.

Type: post <br>
Route: /bots/{bot_id}/assistant <br>
Expected Parameter: {"bot_api_key": "type-str", "chat_history": [{"role": "type-str", "message": "type-str"}], "user_input": "type-str"} <br>
Expected Response: {"role": "type-str", "message": "type-str"} <br>
Note: bot_id is passed as a path parameter. bot_api_key is a bot level key, not the user auth token.

Example Call:
```
response = client.post(
            f"{API_PREFIX}/bots/1/assistant",
            json={
                "bot_api_key": "your-bot-api-key",
                "chat_history": [
                    {"role": "user", "message": "Hello!"},
                    {"role": "ASSISTANT", "message": "Hi, how can I help you?"}
                ],
                "user_input": "What do my documents say about onboarding?"
            }
        )
```

### Users

#### Get User Profile
Returns the profile of the currently authenticated user.

Type: get <br>
Route: /me/ <br>
Expected Parameter: None <br>
Expected Response: {"user_id": "type-uuid", "first_name": "type-str", "last_name": "type-str", "company": "type-str",
"email": "type-str", "phone": "type-str"} <br>

Example Call:
```
response = client.get(
            f"{API_PREFIX}/me/",
            headers=auth_token
        )
```

#### Update User Profile
Updates the profile of the currently authenticated user. Only fields provided will be updated.

Type: patch <br>
Route: /me/ <br>
Expected Parameter: {"first_name": "type-str", "last_name": "type-str", "company": "type-str", "phone": "type-str"} <br>
Expected Response: {"user_id": "type-uuid", "first_name": "type-str", "last_name": "type-str", "company": "type-str",
"email": "type-str", "phone": "type-str"} <br>
Note: All fields are optional. At least one field must be provided. Phone must be exactly 10 digits.

Example Call:
```
response = client.patch(
            f"{API_PREFIX}/me/",
            json={
                "first_name": "John",
                "phone": "5550001234"
            },
            headers=auth_token
        )
```

#### Update User Email
Updates the email of the currently authenticated user.

Type: patch <br>
Route: /me/email <br>
Expected Parameter: {"email": "type-email-str"} <br>
Expected Response: {"message": "type-str"} <br>
Note: Email must be a valid email format.

Example Call:
```
response = client.patch(
            f"{API_PREFIX}/me/email",
            json={"email": "newemail@example.com"},
            headers=auth_token
        )
```

### Bots

#### Create Bot
Creates a new bot for the currently authenticated user. Returns the bot info along with the generated bot API key.
Keep the bot API key safe, it is used to call the assistant route.

Type: post <br>
Route: /bots/ <br>
Expected Parameter: {"bot_name": "type-str", "bot_desc": "type-str", "avatar": "type-str", "color": "type-str",
"storage": "type-int", "uses": "type-int"} <br>
Expected Response: {"bot_info": {"bot_id": "type-int", "bot_name": "type-str", "bot_desc": "type-str", "avatar":
"type-str", "color": "type-str", "storage": "type-int", "uses": "type-int"}, "bot_api_key": "type-str"} <br>

Example Call:
```
response = client.post(
            f"{API_PREFIX}/bots/",
            json={
                "bot_name": "Support Bot",
                "bot_desc": "Handles customer support queries",
                "avatar": "avatar-1",
                "color": "black",
                "storage": 0,
                "uses": 0
            },
            headers=auth_token
        )
```

#### Get All Bots
Returns all bots belonging to the currently authenticated user.

Type: get <br>
Route: /bots/ <br>
Expected Parameter: None <br>
Expected Response: [{"bot_id": "type-int", "bot_name": "type-str", "bot_desc": "type-str", "avatar": "type-str",
"color": "type-str", "storage": "type-int", "uses": "type-int"}] <br>

Example Call:
```
response = client.get(
            f"{API_PREFIX}/bots/",
            headers=auth_token
        )
```

#### Get Bot By ID
Returns a single bot by its ID. The bot must belong to the currently authenticated user.

Type: get <br>
Route: /bots/{bot_id} <br>
Expected Parameter: None <br>
Expected Response: {"bot_id": "type-int", "bot_name": "type-str", "bot_desc": "type-str", "avatar": "type-str",
"color": "type-str", "storage": "type-int", "uses": "type-int"} <br>
Note: bot_id is passed as a path parameter.

Example Call:
```
response = client.get(
            f"{API_PREFIX}/bots/1",
            headers=auth_token
        )
```

#### Update Bot By ID
Updates a bot by its ID. Only fields provided will be updated. The bot must belong to the currently authenticated user.

Type: patch <br>
Route: /bots/{bot_id} <br>
Expected Parameter: {"bot_name": "type-str", "bot_desc": "type-str", "avatar": "type-str", "color": "type-str",
"storage": "type-int", "uses": "type-int"} <br>
Expected Response: {"bot_id": "type-int", "bot_name": "type-str", "bot_desc": "type-str", "avatar": "type-str",
"color": "type-str", "storage": "type-int", "uses": "type-int"} <br>
Note: bot_id is passed as a path parameter. All fields are optional. At least one field must be provided.

Example Call:
```
response = client.patch(
            f"{API_PREFIX}/bots/1",
            json={"bot_name": "Updated Bot Name"},
            headers=auth_token
        )
```

#### Update Bot API Key
Regenerates the API key for a bot. The bot must belong to the currently authenticated user. Keep the new key safe,
it will replace the old one.

Type: patch <br>
Route: /bots/{bot_id}/api_key <br>
Expected Parameter: None <br>
Expected Response: {"bot_id": "type-int", "bot_api_key": "type-str"} <br>
Note: bot_id is passed as a path parameter. This will invalidate the previous bot API key.

Example Call:
```
response = client.patch(
            f"{API_PREFIX}/bots/1/api_key",
            headers=auth_token
        )
```

#### Delete Bot By ID
Deletes a bot by its ID. The bot must belong to the currently authenticated user.

Type: delete <br>
Route: /bots/{bot_id} <br>
Expected Parameter: None <br>
Expected Response: None (204 No Content) <br>
Note: bot_id is passed as a path parameter.

Example Call:
```
response = client.delete(
            f"{API_PREFIX}/bots/1",
            headers=auth_token
        )
```

### Documents

#### Create Document
Uploads a text document for a bot and creates embeddings for it. The document must be a plain text file and
cannot exceed 10MB. The bot must belong to the currently authenticated user.

Type: post <br>
Route: /bots/{bot_id}/documents/ <br>
Expected Parameter: multipart/form-data — doc_name: "type-str", file: "type-file (.txt)" <br>
Expected Response: {"doc_id": "type-int", "bot_id": "type-int", "doc_name": "type-str", "file_name": "type-str",
"doc_type": "type-str", "doc_size": "type-int"} <br>
Note: bot_id is passed as a path parameter. Only text/plain files are accepted. Max file size is 10MB. A document
with the same file name cannot be uploaded twice to the same bot.

Example Call:
```
with open("example.txt", "rb") as f:
    response = client.post(
                f"{API_PREFIX}/bots/1/documents/",
                data={"doc_name": "Example Doc"},
                files={"file": ("example.txt", f, "text/plain")},
                headers=auth_token
            )
```

#### Get All Documents
Returns all documents belonging to a bot. The bot must belong to the currently authenticated user.

Type: get <br>
Route: /bots/{bot_id}/documents/ <br>
Expected Parameter: None <br>
Expected Response: [{"doc_id": "type-int", "bot_id": "type-int", "doc_name": "type-str", "file_name": "type-str",
"doc_type": "type-str", "doc_size": "type-int"}] <br>
Note: bot_id is passed as a path parameter.

Example Call:
```
response = client.get(
            f"{API_PREFIX}/bots/1/documents/",
            headers=auth_token
        )
```

#### Get Document By ID
Returns a single document by its ID. The bot must belong to the currently authenticated user.

Type: get <br>
Route: /bots/{bot_id}/documents/{doc_id} <br>
Expected Parameter: None <br>
Expected Response: {"doc_id": "type-int", "bot_id": "type-int", "doc_name": "type-str", "file_name": "type-str",
"doc_type": "type-str", "doc_size": "type-int"} <br>
Note: bot_id and doc_id are passed as path parameters.

Example Call:
```
response = client.get(
            f"{API_PREFIX}/bots/1/documents/1",
            headers=auth_token
        )
```

#### Download Document By ID
Downloads the raw file of a document by its ID. The bot must belong to the currently authenticated user.

Type: get <br>
Route: /bots/{bot_id}/documents/{doc_id}/download <br>
Expected Parameter: None <br>
Expected Response: Raw file download (FileResponse) <br>
Note: bot_id and doc_id are passed as path parameters. The response is the raw file, not a JSON object.

Example Call:
```
response = client.get(
            f"{API_PREFIX}/bots/1/documents/1/download",
            headers=auth_token
        )
```

#### Delete Document By ID
Deletes a document by its ID from both the database and storage. The bot must belong to the currently
authenticated user.

Type: delete <br>
Route: /bots/{bot_id}/documents/{doc_id} <br>
Expected Parameter: None <br>
Expected Response: None (204 No Content) <br>
Note: bot_id and doc_id are passed as path parameters.

Example Call:
```
response = client.delete(
            f"{API_PREFIX}/bots/1/documents/1",
            headers=auth_token
        )
```

### Feedback

#### Create Feedback
Creates a feedback entry for a bot. The bot must belong to the currently authenticated user.

Type: post <br>
Route: /bots/{bot_id}/feedback/ <br>
Expected Parameter: {"fb_date": "type-date", "fb_time": "type-time", "is_neg": "type-bool", "fb_desc": "type-str",
"use_log": ["type-str"]} <br>
Expected Response: {"fb_id": "type-int", "bot_id": "type-int", "fb_date": "type-date", "fb_time": "type-time",
"is_neg": "type-bool", "fb_desc": "type-str", "use_log": ["type-str"]} <br>
Note: bot_id is passed as a path parameter. is_neg, fb_desc, and use_log are optional.

Example Call:
```
response = client.post(
            f"{API_PREFIX}/bots/1/feedback/",
            json={
                "fb_date": "2024-01-01",
                "fb_time": "12:00:00",
                "is_neg": False,
                "fb_desc": "The bot was very helpful.",
                "use_log": ["What is onboarding?", "How do I reset my password?"]
            },
            headers=auth_token
        )
```

#### Get All Feedback
Returns all feedback entries for a bot. The bot must belong to the currently authenticated user.

Type: get <br>
Route: /bots/{bot_id}/feedback/ <br>
Expected Parameter: None <br>
Expected Response: [{"fb_id": "type-int", "bot_id": "type-int", "fb_date": "type-date", "fb_time": "type-time",
"is_neg": "type-bool", "fb_desc": "type-str", "use_log": ["type-str"]}] <br>
Note: bot_id is passed as a path parameter.

Example Call:
```
response = client.get(
            f"{API_PREFIX}/bots/1/feedback/",
            headers=auth_token
        )
```

#### Get Feedback By ID
Returns a single feedback entry by its ID. The bot must belong to the currently authenticated user.

Type: get <br>
Route: /bots/{bot_id}/feedback/{fb_id} <br>
Expected Parameter: None <br>
Expected Response: {"fb_id": "type-int", "bot_id": "type-int", "fb_date": "type-date", "fb_time": "type-time",
"is_neg": "type-bool", "fb_desc": "type-str", "use_log": ["type-str"]} <br>
Note: bot_id and fb_id are passed as path parameters.

Example Call:
```
response = client.get(
            f"{API_PREFIX}/bots/1/feedback/1",
            headers=auth_token
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
response = client.get(f"{API_PREFIX}/health")
```

### Health Check (Supabase)
Returns the health status of the API and the Supabase connection.

Type: get <br>
Route: /health/user <br>
Expected Parameter: None <br>
Expected Response: {"status": "ok", "supabase_connected": {supabase_user_obj}}

Example Call:
```
response = client.get(f"{API_PREFIX}/health/user")
```