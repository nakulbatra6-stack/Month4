import requests

API_KEY = "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"

# Start with system message (VERY IMPORTANT)
history = [
    {
        "role": "system",
        "content": "You are a helpful AI tutor who explains concepts simply."
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
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemma-4-26b-a4b-it",
            "messages": history
        }
    )

    data = response.json()

    # Handle errors properly
    if "choices" not in data:
        return f"Error: {data}"

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