CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;

--
CREATE TABLE users (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    company TEXT,
    email TEXT NOT NULL,
    phone TEXT
);

--
CREATE TABLE bots (
    bot_id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    bot_name TEXT NOT NULL,
    bot_desc TEXT,
    color TEXT,
    uses INT -- perhaps switch to bigint if thought needed
);

--
CREATE TABLE feedback (
    fb_id BIGSERIAL PRIMARY KEY,
    bot_id BIGINT REFERENCES bots(bot_id) ON DELETE CASCADE,
    fb_date DATE NOT NULL,
    fb_time TIME NOT NULL
    is_neg BOOLEAN, -- true = negative, false = positive, null = not answered
    fb_desc TEXT,
    use_log TEXT[] -- AI and user transcription
);

