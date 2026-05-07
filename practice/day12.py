import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation =[]

def chat(user_input):
    conversation.append({
        "role":"user",
        "content":user_input
    })


    message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="你是一位專業的IT技術支援工程師，請用繁體中文回答",
    messages=conversation
)

    response = message.content[0].text

    conversation.append({
    "role":"assistant",
    "content":response
})

    return response

print("IT機器人啟動! 輸入quit結束對話\n")

while True:
    user_input = input("你:")
    if user_input == "quit":
        print("對話結束!")
        break

    response = chat(user_input)
    print(f"Claude:{response}\n")
    