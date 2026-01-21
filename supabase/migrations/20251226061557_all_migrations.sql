CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;

-- RELATIONAL DATABASE

-- Table storing user data that's connected to the auth.users table.
CREATE TABLE users (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    company TEXT,
    email TEXT NOT NULL,
    phone TEXT
);

-- Table storing the user's bots and its information.
CREATE TABLE bots (
    bot_id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    bot_name TEXT NOT NULL,
    bot_desc TEXT,
    avatar TEXT,
    color TEXT,
    storage INT, -- KB used in document storage
    uses INT -- perhaps switch to bigint if thought needed
);

-- Table storing the documents relating to each bot.
CREATE TABLE documents (
    doc_id BIGSERIAL PRIMARY KEY,
    bot_id BIGINT REFERENCES bots(bot_id) ON DELETE CASCADE,
    doc_name TEXT,
    doc_type TEXT,
    doc_size INT -- size of document in KB
);

-- Table storing the feedback for each bot.
CREATE TABLE feedback (
    fb_id BIGSERIAL PRIMARY KEY,
    bot_id BIGINT REFERENCES bots(bot_id) ON DELETE CASCADE,
    fb_date DATE NOT NULL,
    fb_time TIME NOT NULL
    is_neg BOOLEAN, -- true = negative, false = positive, null = not answered
    fb_desc TEXT,
    use_log TEXT[] -- AI and user transcription
);


-- DOCUMENT STORAGE
-- docs : https://supabase.com/docs/guides/storage/quickstart

-- bucket for bot avatars: will be stored as avatars/bot_avatars/{avatar_name}.png
-- no seeding option for this so need to set up a function on start up to insert files into the buckets.
-- this is low priority so bot avatars can be set up later
insert into storage.buckets
  (id, name)
values
  ('avatars', 'avatars');

-- bucket for bot documents: will be stored as documents/{bot_id}/{file_name}.pdf
insert into storage.buckets
  (id, name, allowed_mime_types, file_size_limit)
values
  ('documents', 'documents', ARRAY['text/plain','application/pdf'], '2048');


-- VECTOR DATABASE

-- enabling the vector database ability with supabase
-- docs : https://supabase.com/docs/guides/database/extensions/pgvector
create extension vector
with
    schema extensions;

-- Table storing the vectorized documents
