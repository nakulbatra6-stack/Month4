import requests

API_KEY = "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"

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

    # Add user message
    history.append({"role": "user", "content": prompt})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
        "model": "google/gemma-4-26b-a4b-it", 
        "messages": history,
        "max_tokens": 200,
        # "max_tokens": 150 if short_mode else 400,
        "temperature": 0.7#controls randomness
        },
    )

    data = response.json()
    print(data)
    print(data.get("usage"))

    # Handle errors properly
    if "choices" not in data:
        return f"Error: {data}"

    #     {
    #   "id": "chatcmpl-xyz",
    #   "choices": [
    #     {
    #       "message": {    
    #         "role": "assistant",
    #         "content": "Machine Learning is a way for computers to learn..."
    #       }
    #     }
    #   ]
    # }
    assistant_reply = data["choices"][0]["message"]["content"]
    # Add assistant reply to history
    history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


print("Chatbot started (type 'exit' to quit)\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    reply = chat(user_input)
    print("Bot:", reply)
