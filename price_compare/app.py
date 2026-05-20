import streamlit as st
import requests
import os 
import anthropic
from dotenv import load_dotenv


load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


st.set_page_config(
    page_title="廚房比價網",
    page_icon="🍳",
    layout="wide"
)
st.title("🍳 廚房用品比價網")
st.markdown("輸入關鍵字，一次搜尋各大購物平台商品價格")
st.markdown("---")

 # part 2 搜尋函式



def search_products(keyword):
    url="https://google.serper.dev/shopping"
    headers = {
        "X-API-KEY":  SERPER_API_KEY,
        "Content-Type":"application/json"
    }
    payload = {
        "q":keyword,
        "gl":"tw",
        "hl":"zh-tw"
    }
    response = requests.post(url,headers=headers,json=payload)
    data = response.json()
    print("回傳的欄位:",list(data.keys()))
    print("shoppingResults 筆數:",len(data.get("shoppingResults",[])))

    results = []
    for item in data.get("shopping",[]):
        results.append({
            "title": item.get("title",""),
            "price": item.get("price",""),
            "source": item.get("source",""),
            "link": item.get("link",""),
            "rating": item.get("rating",None),
            "reviews": item.get("reviews",None),
            "imageUrl": item.get("imageUrl",""),
        })
    return results

def analyze_products(results, keyword):
    """請 Claude 分析搜尋結果，推薦 CP 值最高的商品"""

    product_text = ""
    for i, r in enumerate(results[:10],1):
        product_text += f"{i}.商品:{r['title']}\n"
        product_text += f"   價格:{r['price']}\n"
        product_text += f"   來源:{r['source']}\n"
        if r ['rating']:
            product_text += f"   評分:{r['rating']}({r['reviews']}評論)\n"
        product_text += "\n"
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{
            "role":"user",
            "content":f"""以下是「{keyword}」的購物搜尋結果，請幫我：
            1. 推薦 CP 值最高的商品（說明原因）
            2. 分析價格區間分布
            3. 購買建議

            商品列表:
            {product_text}
            請用繁體中文回答，條列式呈現。"""
            
        }]
    )
    return response.content[0].text

# part3 搜尋介面

keyword = st.text_input("🔍 搜尋商品", placeholder="例如：廚房收納架、保鮮盒、刀架")

col1, col2 = st.columns(2)
with col1:
    price_min = st.number_input("最低價格",min_value=0,value=0,step=100)
with col2:
    price_max = st.number_input("最高價格",min_value=0,value=10000,step=100)

def parse_price(price_str):
    """把價格字串轉成數字，例如399.00 → 399"""
    try:
        return float(price_str.replace("$","").replace(",","").strip())
    except:
        return None
if "results" not in st.session_state:
    st.session_state.results = []
if "keyword" not in st.session_state:
    st.session_state.keyword = ""
if "analysis" not in st.session_state:
    st.session_state.analysis = ""

if st.button("搜尋",type="primary"):
    if not keyword.strip():
        st.warning("⚠️ 請輸入關鍵字")
    else:
        with st.spinner("🔍 搜尋中..."):
            results = search_products(keyword)

            if price_max > 0:
                filtered = []
                for r in  results:
                    p = parse_price(r["price"])
                    if p is not None and price_min <= p <= price_max:
                        filtered.append(r)
                results = filtered

                st.session_state.results = results
                st.session_state.keyword = keyword
                st.session_state.analysis = ""

if st.session_state.results:
    results = st.session_state.results
    st.success(f"✅ 找到 {len(results)} 筆商品")

    if st.button("🤖 Claude AI 分析推薦"):
        with st.spinner("🤖 AI 正在分析商品..."):
            st.session_state.analysis = analyze_products(
                results, st.session_state.keyword
            )
    if st.session_state.analysis:
        st.subheader("🤖 Claude AI 分析結果")
        st.markdown(st.session_state.analysis)
        st.markdown("---")
    
    for r in results:
        with st.expander(f"{r['title']}|{r['price']}"):
            col1, col2 = st.columns(2)
            col1.metric("價格",r["price"])
            col2.metric("來源",r["source"])
            st.link_button("前往購買 →",f"https://www.google.com/search?q={r['source']}+{st.session_state.keyword}")



    