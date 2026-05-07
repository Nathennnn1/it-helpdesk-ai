import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(

    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role":"user","content":"你好，請用繁體中文介紹一下你自己"}
    ]
)

print(message.content[0].text)




