import anthropic
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = FastAPI()

SYSTEM_PROMPT = """你是IT Helpdesk工程師。只能輸出JSON，不要有任何其他文字。
直接從{開始，到}結束。

{"category":"硬體/軟體/網路/其他","severity":"低/中/高","solution":["步驟1","步驟2","步驟3"],"follow_up":"一句話詢問用戶"}"""

class Question(BaseModel):
    message:str
    user_name:str = "匿名用戶"
def save_ticket(user_name,message,response):
    os.makedirs("tickets",exist_ok=True)

    ticket = {
        "ticket_id":datetime.now().strftime("%Y%m%d%H%M%S"),
        "user_name":user_name,
        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question":message,
        "response":response
    }

    filename = f"tickets/ticket_{ticket['ticket_id']}.json"
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(ticket, f,ensure_ascii=False,indent=2)

    return ticket["ticket_id"]

@app.get("/")
def home():
    return {"message":"IT Helpdesk助手啟動成功！"}

@app.post("/ask")
def ask(question:Question):

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role":"user","content":question.message}
        ]
    )

    response_text = response.content[0].text
    
    try:
        start = response_text.find("{")
        end = response_text.rfind("}") +1
        data = json.loads(response_text[start:end])


        ticket_id = save_ticket(question.user_name,question.message,data)
        data["ticket_id"] = ticket_id

        return data
    except:
        return{"error":"解析失敗","raw":response_text}
    

@app.get("/tickets")
def get_tickets():

    if not os.path.exists("tickets"):
        return{"tickets":[]}
    
    tickets = []
    for filename in os.listdir("tickets"):
        if filename.endswith(".json"):
            with open(f"tickets/{filename}","r",encoding="utf-8") as f:
                tickets.append(json.load(f))
    return {"total": len(tickets), "tickets": tickets}

    
