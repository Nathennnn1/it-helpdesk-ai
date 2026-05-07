import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="你是一位專業的IT技術支援工程師，回答時請用 JSON 格式輸出，使用繁體中文",
    messages=[
        {"role":"user","content":"請列出電腦無法連網的3個常見原因，用 JSON 格式回傳，格式為：{reason:[原因1,原因2,原因3]}"}
    ]
)

respones_text=message.content[0].text
clean_text=respones_text.replace("```json","").replace("```","").strip()

data=json.loads(clean_text)
for i, reason in enumerate(data["reason"]):
    print(f"原因{i+1}:{reason}")

