# google/gemma-4-26b-a4b-it
import requests

API_KEY = "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"

history = []
# print(type(history))#<class 'list'>

def chat(prompt):
    global history
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
        # "messages": history --> this is used for history, everytime the entire messages are sent again in JSON format.
        #[
        #   {"role": "user", "content": "My name is Nakul"},
        #   {"role": "assistant", "content": "Nice to meet you, Nakul!"},
        #   {"role": "user", "content": "What is my name?"}
        # ]
    )
    try:
        data = response.json()
    except ValueError:
        return f"Error: could not parse JSON. Status: {response.status_code}, Body: {response.text}"
    if "choices" not in data:
        return f"Error from API. Status: {response.status_code}, Response: {data}"
    assistant_reply = data["choices"][0]["message"]["content"]
    history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

print("Chatbot started (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    print("Bot:", chat(user_input))
    print(history)