import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation = []

SYSTEM_PROMPT = """你是IT Helpdesk工程師小幫。
只輸出JSON，不要有任何其他文字、符號或說明。
不要用markdown格式。
直接從{開始，到}結束。

{"category":"硬體或軟體或網路或其他","severity":"低或中或高","solution":["步驟1","步驟2","步驟3"],"follow_up":"一句話詢問用戶"}"""

def chat(user_input):
    conversation.append({"role": "user", "content": user_input})
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation
    )
    response = message.content[0].text
    conversation.append({"role": "assistant", "content": response})
    return response

def display_response(response_text):
    try:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        json_text = response_text[start:end]
        data = json.loads(json_text)
        print(f"\n📋 問題類型：{data['category']}")
        print(f"⚠️  嚴重程度：{data['severity']}")
        print(f"\n🔧 解決步驟：")
        for i, step in enumerate(data['solution']):
            print(f"   {i+1}. {step}")
        print(f"\n💬 {data['follow_up']}\n")
    except Exception as e:
        print(f"\n解析錯誤：{e}")
        print(f"原始回應：{response_text}\n")

print("=" * 50)
print("   IT Helpdesk AI 助手 🤖")
print("=" * 50)
print("輸入你的 IT 問題，輸入 quit 結束\n")

while True:
    user_input = input("你的問題：")
    if user_input.lower() == "quit":
        print("\n感謝使用 IT Helpdesk AI 助手！")
        break
    print("\n⏳ 分析中...")
    response = chat(user_input)
    display_response(response)