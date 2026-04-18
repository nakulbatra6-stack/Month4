import requests
import os
from dotenv import load_dotenv
import json
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_max_tokens(prompt):
    if len(prompt) < 50:
        return 100
    elif len(prompt) < 200:
        return 200
    else:
        return 400


# print(API_KEY)

# Start with system message (VERY IMPORTANT)
# {
#   "Authorization": "Bearer YOUR_API_KEY",
#   "Content-Type": "application/json"
# }
# Actual message that is being sent.
# {
#   "model": "google/gemma-4-26b-a4b-it",
#   "messages": [
#     {"role": "system", "content": "You are a helpful AI tutor..."},
#     {"role": "user", "content": "What is ML?"}
#   ]
# }

history = [
    {
        "role": "system",
        "content": "You are a helpful AI tutor who explains concepts simply.",
    }
]



def chat(prompt):
    global history

    MAX_HISTORY = 2

    # Trim history
    if len(history) > MAX_HISTORY:
        history = [history[0]] + history[-MAX_HISTORY:]

    # Add user message
    history.append({"role": "user", "content": prompt})

    # 🧠 SHOW HISTORY BEFORE REQUEST
    print("\n================= REQUEST =================")
    print(f"📏 History length BEFORE request: {len(history)}")
    print("📤 History sent to API:")
    for msg in history:
        print(f"{msg['role'].upper()}: {msg['content']}")
    print("==========================================\n")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "google/gemma-4-26b-a4b-it",
            "messages": history,
            "max_tokens": get_max_tokens(prompt),
            "temperature": 0.7,
        },
    )

    data = response.json()

    # ❌ Error handling
    if response.status_code != 200:
        return f"HTTP Error: {response.status_code}"

    if "error" in data:
        return f"API Error: {data['error']}"

    if "choices" not in data:
        return "Unexpected response format"

    # 📥 Extract assistant reply
    assistant_reply = data["choices"][0]["message"]["content"]
    finish_reason = data["choices"][0]["finish_reason"]

    # 🧾 SHOW RESPONSE CLEANLY
    print("================= RESPONSE =================")
    print("🤖 Assistant Reply:\n")
    print(assistant_reply)
    print("\n------------------------------------------")
    print(f"🛑 Finish reason: {finish_reason}")
    print("------------------------------------------")

    # 📊 Token usage
    usage = data.get("usage", {})
    print("📊 Token Usage:")
    print(json.dumps(usage, indent=2))
    print("===========================================\n")

    # Add assistant reply to history
    history.append({"role": "assistant", "content": assistant_reply})

    # 🧠 SHOW UPDATED HISTORY
    print("🧠 Updated History:")
    print(f"📏 History length AFTER response: {len(history)}")

    # Optional: count types
    user_count = sum(1 for m in history if m["role"] == "user")
    assistant_count = sum(1 for m in history if m["role"] == "assistant")

    print(f"👤 User messages: {user_count}")
    print(f"🤖 Assistant messages: {assistant_count}")
    print("-------------------------------------------")

    for msg in history:
        print(f"{msg['role'].upper()}: {msg['content'][:60]}...")

    print("===========================================\n")

    return assistant_reply
# def chat(prompt):
#     global history
#     MAX_HISTORY = 2  # most recent 2 convers.
#     if len(history) > MAX_HISTORY:
#         history = [history[0]] + history[-MAX_HISTORY:]

#     # Add user message
#     history.append({"role": "user", "content": prompt})

#     response = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json",
#         },
#         json={
#             "model": "google/gemma-4-26b-a4b-it",
#             "messages": history,
#             # "max_tokens": 200,
#             "max_tokens": get_max_tokens(prompt),
#             # "max_tokens": 150 if short_mode else 400,
#             "temperature": 0.7,  # controls randomness
#         },
#     )

#     data = response.json()
#     print(f"{data},\n ")
#     print(data.get("usage"))
#     #     Response in JSON {
#     #    {'id': 'gen-1776499549-aQv4XfyctGDusDH0t2qW', 'object': 'chat.completion', 'created': 1776499549, 'model': 'google/gemma-4-26b-a4b-it-20260403', 'provider': 'Ionstream', 'system_fingerprint': None, 'choices': [{'index': 0, 'logprobs': None, 'finish_reason': 'length', 'native_finish_reason': 'length', 'message': {'role': 'assistant', 'content': "Hello! I am happy to see you. \n\nI am your AI tutor, and I am here to help you learn. Whether you are struggling with a tricky math problem, trying to understand a scientific concept, or just want to practice a new language, I am ready to help.\n\n**How I work:**\n*
#     #   **I keep it simple:** I won't use big, scary words unless I explain them first.\n*   **I use examples:** I like to use",
#     # 'refusal': None, 'reasoning': None}}], 'usage': {'prompt_tokens': 43, 'completion_tokens': 100, 'total_tokens': 143, 'cost': 4.344e-05, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 4.344e-05, 'upstream_inference_prompt_cost': 3.44e-06, 'upstream_inference_completions_cost': 4e-05}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}},

#     # Handle errors properly
#     if response.status_code != 200:
#         return f"HTTP Error: {response.status_code}"

#     if "error" in data:
#         return f"API Error: {data['error']}"

#     if "choices" not in data:
#         return "Unexpected response format"

#     assistant_reply = data["choices"][0]["message"]["content"]
#     # Add assistant reply to history
#     history.append({"role": "assistant", "content": assistant_reply})
#     print(history)
#     return assistant_reply
    


print("Chatbot started (type 'exit' to quit)\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    reply = chat(user_input)
    print("Bot:", reply)
