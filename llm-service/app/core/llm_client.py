from transformers import pipeline
from app.schemas.llm import ChatMessage
from typing import List
from openai_harmony import (
    Author,
    Conversation,
    DeveloperContent,
    HarmonyEncodingName,
    Message,
    Role,
    SystemContent,
    load_harmony_encoding,
    ReasoningEffort,
)

MODEL_ID = "openai/gpt-oss-20b"
MAX_TOKENS = 100
MAX_CONVO_HISTORY = 10


class LLMClient:
    def __init__(self):
        self.pipe = pipeline(
            "text-generation",
            model=MODEL_ID,
            torch_dtype="auto",
            device_map="auto",
        )

    def get_llm_response(self, chat_history: List[ChatMessage], retrieved_context: List[str], user_input: str):
        context = "\n\n".join(retrieved_context)

        encoder = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)

        system_message = (
            SystemContent.new()
            .with_reasoning_effort(ReasoningEffort.LOW)
            .with_conversation_start_date("2025-06-28")
        )

        developer_message = (
            DeveloperContent.new()
            .with_instructions(
                "Answer questions using only the provided context." +
                "If the context doesn't contain the answer, say so."
            )
        )

        recent_history = chat_history[-MAX_CONVO_HISTORY:] if len(chat_history) > MAX_CONVO_HISTORY else chat_history

        previous_convo = []
        for msg in recent_history:
            role = Role.ASSISTANT if msg["role"] == "ASSISTANT" else Role.USER
            previous_convo.append(Message.from_role_and_content(role, msg["message"]))

        convo = Conversation.from_messages(
            [
                Message.from_role_and_content(Role.SYSTEM, system_message),
                Message.from_role_and_content(Role.DEVELOPER, developer_message),
            ] + previous_convo + [
                Message.from_role_and_content(Role.USER, user_input),

                Message.from_role_and_content(
                    Role.ASSISTANT,
                    f"User asks: {user_input} we need to get question context.",
                ).with_channel("analysis"),
                Message.from_role_and_content(Role.ASSISTANT, user_input)
                .with_channel("commentary")
                .with_recipient("functions.get_question_context")
                .with_content_type("<|constrain|> json"),
                Message.from_author_and_content(
                    Author.new(Role.TOOL, "functions.get_question_context"),
                    context
                ).with_channel("commentary"),
            ]
        )

        tokens = encoder.render_conversation_for_completion(convo, Role.ASSISTANT)

        outputs = self.pipe(
            encoder.decode_utf8(tokens),
            max_new_tokens=MAX_TOKENS,
        )

        return outputs[0]["generated_text"][-1]



