# src/responder.py
import os
from dotenv import load_dotenv
from groq import Groq
from src.prompts import SYSTEM_PROMPT

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])


def generate_reply(history: list, emotions: dict) -> str:
    emotion_str = ", ".join(f"{k} ({v:.0%})" for k, v in emotions.items()) or "neutral"
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(emotions=emotion_str)}]
    messages.extend(history)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=300,
        messages=messages,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    test_history = [{"role": "user", "content": "I had a really rough day, nothing went right."}]
    test_emotions = {"sadness": 0.7, "disappointment": 0.5}
    print(generate_reply(test_history, test_emotions))