import anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation =[]

SYSTEM_PROMT="""你是一位專業的IT Helpdesk 支援工程師，名字叫做「小幫」。

你的工作職責:
1. 診斷使用者的IT問題
2. 提供清楚的解決步驟
3. 每次回應都要先判斷問題類型


只輸出JSON，不要有任何其他文字、符號或說明。
不要用markdown格式。
直接從{開始，到}結束。
{

   "category":"硬體/軟體/網路/其他",
   "severity":"低/中/高",
   "solution":["步驟1","步驟2","步驟3"],
   "followup":"詢問使用者的後續問題"

}

禁止在 JSON 前後加任何文字。

"""

def chat(user_input):
    conversation.append({"role":"user","content":user_input})

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMT,
        messages=conversation
        )
    
    response = message.content[0].text
    conversation.append({"role":"assistant","content":response})
    return response

def display_reponse(response_text):
    try:
        start = reponse.text.find("{")
        end = reponse.text.rfind("}") +1
        json_text = response_text[start:end]
        data = json.loads(json_text)

        print(f"\n問題類型:{data['category']}")
        print(f"嚴重程度:{data['severity']}")
        print(f"\n解決步驟:")
        for i, step in enumerate(data['solution']):
            print(f" {i+1}. {step}")
        print(f"\n {data['follow_up']}\n")
    except Exception as e:
        print(f"\n解析錯誤:{e}")
        print(f"原始回應:{response_text}\n")
        


print("=" * 50)
print("  IT Helpdesk 助手")
print("=" * 50)
print("輸入你的IT問題，輸入quit結束\n")

while True:
    user_input = input("你的問題:")
    if user_input.lower() == "quit":
        print(f"\n感謝使用IT Helpdesk AI助手！")
        break

    print("\n分析中...")
    reponse = chat(user_input)
    display_reponse(reponse)

