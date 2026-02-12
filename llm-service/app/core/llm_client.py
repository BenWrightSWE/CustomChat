from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
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

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

MAX_TOKENS = 100
MAX_CONVO_HISTORY = 10

_llm_instance = None


class LLMClient:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float16,
            device_map="auto"
        )

    def generate(self, messages):
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        output = self.model.generate(
            **inputs,
            max_new_tokens=MAX_TOKENS,
            temperature=0.0
        )

        response = self.tokenizer.decode(
            output[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        )

        return response.strip()

    def get_llm_response(self, chat_history: List[ChatMessage], retrieved_context: List[str], user_input: str):
        context = "\n\n".join(retrieved_context)

        system_prompt = (
            "You are a helpful assistant.\n\n"
            "Answer questions from the most recent user message using ONLY the provided context.\n"
            "Answer these questions with a human-like response giving a sense of conversation.\n"
            "If the context does not contain the answer, say so.\n\n"
            f"CONTEXT:\n{context}"
        )

        messages = [
            {"role": "system", "content": system_prompt}
        ]

        recent_history = chat_history[-MAX_CONVO_HISTORY:] if len(chat_history) > MAX_CONVO_HISTORY else chat_history

        if recent_history and recent_history[0].role == "ASSISTANT":
            recent_history = recent_history[1:]

        for msg in recent_history:
            role = "assistant" if msg.role == "ASSISTANT" else "user"
            messages.append({"role": role, "content": msg.message})

        messages.append({"role": "user", "content": user_input})

        return self.generate(messages)


def get_llm() -> LLMClient:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMClient(MODEL_ID)
    return _llm_instance
