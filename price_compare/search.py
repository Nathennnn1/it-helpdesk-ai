import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_products(keyword):
    """用關鍵字搜尋各平台商品"""
    url = "https://google.serper.dev/shopping"
    headers = {
        "X-API-KEY":  SERPER_API_KEY,
        "Content-Type":"application/json"
    }
    payload ={
        "q": keyword,
        "gl":"tw",
        "hl":"zh-tw"
    }
    

    response = requests.post(url,headers=headers,json=payload)
    print("狀態碼：",response.status_code)
    print("錯誤內容:",response.text)
    data = response.json()

    results = []
    for item in data.get("shopping",[]):
        results.append({
            "title":  item.get("title",""),
            "price":  item.get("price",""),
            "source": item.get("source",""),
            "link":   item.get("link",""),
        })
    return results

if __name__ == "__main__":
    results = search_products("廚房收納架")
    for r in results:
        print(f"商品:{r['title']}")
        print(f"價格:{r['price']}")
        print(f"來源:{r['source']}")
        print(f"連結:{r['link']}")
        print("---")