import streamlit as st
import requests
import pandas as pd
import json
import matplotlib
import matplotlib.pyplot as plt


# 設定中文字體
matplotlib.rc("font", family="Microsoft JhengHei")
plt.rcParams["axes.unicode_minus"] = False

API_URL     = "http://127.0.0.1:8000"


  
# ── 頁面設定 ──
st.set_page_config(
    page_title="IT Helpdesk Dashboard",
    page_icon="🖥️",
    layout="wide"
)

st.title("🖥️ IT Helpdesk 工單分析報告")
st.markdown("---")

# 登入狀態
if "role" not in st.session_state:
    st.session_state["role"] = "user"
    st.session_state["username"] = "訪客"
    st.session_state["admin_logged_in"] = False


# ── 側邊欄：功能選擇 ──
st.sidebar.title("📂 功能選單")
st.sidebar.markdown(f"👤 **{st.session_state['username']}**")
st.sidebar.markdown(f"🔑 權限:{'管理員' if st.session_state['role'] == 'admin' else '一般用戶'}")
st.sidebar.markdown("---")

# Admin 登入區塊
if st.session_state["role"] != "admin":
    with st.sidebar.expander("🔐 管理員登入"):
        with st.form("admin_login_form"):
            admin_account = st.text_input("帳號", key="admin_account")
            admin_password = st.text_input("密碼", type="password", key="admin_password")
            submitted = st.form_submit_button("登入")

            if submitted:
               if admin_account == "admin" and admin_password == "admin123":
                   st.session_state["role"] = "admin"
                   st.session_state["username"] = "Admin"
                   st.rerun()
               else:
                   st.error("帳號或密碼錯誤")
else:
    if st.sidebar.button("登出管理員"):
        st.session_state["role"] = "user"
        st.session_state["username"] = "訪客"
        st.rerun()

if st.session_state["role"] == "admin":
    pages = ["📊 總覽", "📈 進階分析", "🗂️ 工單明細","➕ 新增工單"]
else:
    pages = ["📊 總覽", "🗂️ 工單明細","➕ 新增工單"]

page = st.sidebar.radio("選擇頁面",pages)

# ── 讀取資料 ──
@st.cache_data(ttl=10)
def fetch_stats():
    try:
        res = requests.get(f"{API_URL}/stats")
        return res.json()
    except:
        return None

@st.cache_data(ttl=10)
def fetch_tickets():
    try:
        res = requests.get(f"{API_URL}/tickets")
        return res.json().get("tickets", [])
    except:
        return []

@st.cache_data(ttl=10)
def load_df():
    tickets = fetch_tickets()
    if not tickets:
        return pd.DataFrame()
    
    rows = []
    for t in tickets:
        rows.append({
            "ticket_id": t["ticket_id"],
            "user_name": t["user_name"],
            "timestamp": t["timestamp"],
            "question": t["question"],
            "category": t["response"]["category"],
            "severity": t["response"]["severity"],
            "status": t["response"].get("status", "待處理"),
        })
    df = pd.DataFrame(rows)
    df["timestamp"]       = pd.to_datetime(df["timestamp"])
    df["severity_score"]  = df["severity"].map({"低": 1, "中": 2, "高": 3})
    df["weekday"]         = df["timestamp"].dt.day_name()
    df["date"]            = df["timestamp"].dt.date
    return df

stats   = fetch_stats()
tickets = fetch_tickets()
df      = load_df()

# ── API 連線失敗 ──
if stats is None:
    st.error("❌ 無法連線到 API，請先執行：python -m uvicorn api:app --reload")
    st.stop()

if stats["total"] == 0 or df.empty:
    st.warning("⚠️ 目前沒有任何工單，請先用 /ask 新增工單")
    st.stop()

# ════════════════════════════════════════
# 頁面 1：總覽
# ════════════════════════════════════════
if page == "📊 總覽":

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("工單總數",   stats["total"])
    col2.metric("最多類別",   max(stats["by_category"], key=stats["by_category"].get))
    col3.metric("高嚴重工單", stats["by_severity"].get("高", 0))
    col4.metric("待處理工單", stats["by_status"].get("待處理", 0))
    col5.metric("⚠️ 安全違規", stats["by_category"].get("安全違規", 0))

    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 圖表", "📋 摘要"])
    with tab1:    
       col_l, col_r = st.columns(2)
       with col_l:
        st.subheader("📂 各類別工單數量")
        df_cat = pd.DataFrame({
            "類別": list(stats["by_category"].keys()),
            "數量": list(stats["by_category"].values())
        }).set_index("類別")
        st.bar_chart(df_cat)

        st.subheader("📋 工單狀態分布")
        df_status = pd.DataFrame({
            "狀態": list(stats["by_status"].keys()),
            "數量": list(stats["by_status"].values())
        }).set_index("狀態")
        st.bar_chart(df_status)

       with col_r:
        st.subheader("⚠️ 嚴重程度分布")
        df_sev = pd.DataFrame({
            "嚴重程度": list(stats["by_severity"].keys()),
            "數量":    list(stats["by_severity"].values())
        }).set_index("嚴重程度")
        st.bar_chart(df_sev)

        st.subheader("👤 各用戶工單數量")
        df_user = pd.DataFrame({
            "用戶": list(stats["by_user"].keys()),
            "數量": list(stats["by_user"].values())
        }).set_index("用戶")
        st.bar_chart(df_user)

    with tab2:    
      st.subheader("📋 工單統計摘要")

      with st.expander("📂 類別詳細",expanded=True):
          for k, v in stats["by_category"].items():
              st.progress(v / stats["total"])
              st.write(f" {k}:**{v}**張 ({v/stats['total']*100:.1f}%) ")

      with st.expander("⚠️ 嚴重程度詳細",expanded=True):
          for k, v in stats["by_severity"].items():
              st.progress(v / stats["total"])
              st.write(f"  {k}: **{v}**張 ({v/stats['total']*100:.1f}%) ")
      with st.expander("📋 狀態詳細",expanded=True):
          for k, v in stats["by_status"].items():
              st.progress(v / stats["total"])
              st.write(f"  {k}: **{v}** 張 ({v/stats['total']*100:.1f}%)")

# ════════════════════════════════════════
# 頁面 2：進階分析（Pandas Part 2）
# ════════════════════════════════════════
elif page == "📈 進階分析":

    st.subheader("📊 用戶 × 類別 樞紐分析表")
    pivot = pd.pivot_table(
        df, values="ticket_id", index="user_name",
        columns="category", aggfunc="count", fill_value=0
    )
    st.dataframe(pivot, use_container_width=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("🏆 各用戶平均嚴重程度")
        user_sev = df.groupby("user_name")["severity_score"].mean().sort_values(ascending=False).reset_index()
        user_sev.columns = ["用戶", "平均分數"]
        st.bar_chart(user_sev.set_index("用戶"))

        st.subheader("📅 每日工單趨勢")
        daily = df.groupby("date").size().reset_index(name="工單數")
        st.line_chart(daily.set_index("date"))

    with col_r:
        st.subheader("📅 星期幾最多工單")
        weekday = df.groupby("weekday").size().reset_index(name="數量")
        st.bar_chart(weekday.set_index("weekday"))

        st.subheader("🔴 高嚴重度 Top 工單")
        top = df.sort_values("severity_score", ascending=False)[
            ["user_name", "question", "severity", "timestamp"]
        ].head(5)
        top.columns = ["用戶", "問題", "嚴重程度", "時間"]
        st.dataframe(top, use_container_width=True)
    

# ════════════════════════════════════════
# 頁面 3：工單明細
# ════════════════════════════════════════
elif page == "🗂️ 工單明細":

    st.subheader("🗂️ 工單明細")

    df_view = df

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_cat  = st.selectbox("篩選類別",    ["全部"] + list(df["category"].unique()))       
    with col2:
        filter_sev  = st.selectbox("篩選嚴重程度", ["全部"] + list(df["severity"].unique()))
    with col3:
        filter_user = st.selectbox("篩選用戶",    ["全部"] + list(df["user_name"].unique()))

    col_check1, col_check2 = st.columns(2)
    with col_check1:
        show_pending = st.checkbox("只顯示待處理工單", value=False)
    with col_check2:
        show_high = st.checkbox("只顯示高嚴重程度工單", value=False)
        

    filtered = df.copy()
    if filter_cat  != "全部": filtered = filtered[filtered["category"]  == filter_cat]
    if filter_sev  != "全部": filtered = filtered[filtered["severity"]  == filter_sev]
    if filter_user != "全部": filtered = filtered[filtered["user_name"] == filter_user]
    if show_pending:          filtered = filtered[filtered["status"]    ==  "待處理"]
    if show_high:             filtered = filtered[filtered["severity"]  == "高"]

    st.write(f"共 **{len(filtered)}** 筆工單")
    display = filtered[["ticket_id","user_name","timestamp","question","category","severity","status"]].copy()
    display.columns = ["工單ID","用戶","時間","問題","類別","嚴重程度","狀態"]

    def highlight_security(row):
        # 安全違規永遠顯示紅色
        if row["類別"] == "安全違規":
            return ["background-color: #ffcccc"] * len(row)
        # 高嚴重程度工單只在勾選時顯示橘色
        if highlight_security and row["嚴重程度"] == "高":
            return ["background-color: #fff9c4"] * len(row)      
        return [""] * len(row)
    
    display.index = range(1, len(display) + 1)
    st.dataframe(
        display.style.apply(highlight_security, axis=1),
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("💬 查看工單對話紀錄")

    selected_id = st.selectbox(
        "選擇工單",
        options=filtered["ticket_id"].tolist()
    )

    if st.button("🔍 查看對話"):
        filename = f"../tickets/ticket_{selected_id}.json"
        
        with open (filename, "r", encoding="utf-8") as f:
            ticket = json.load(f)
        
        chat_history = ticket.get("chat_history", [])

        if not chat_history:
            st.info("此工單沒有對話紀錄")
        else:
            for msg in chat_history:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    with st.chat_message("assistant"):
                        if isinstance(msg["content"], list):
                            st.write("**解決步驟:**")
                            for i, step in enumerate(msg["content"], 1):
                                st.write(f"{i}. {step}")
                        else:
                            st.write(msg["content"])



    csv = display.to_csv(index=False, encoding="big5", errors="replace")
    st.download_button(
        label="⬇️ 下載工單 CSV",
        data=csv,
        file_name="tickets_export.csv",
        mime="text/csv"
     )
    
    # 只有 Admin 才能看到的管理功能
    
    if st.session_state["role"] == "admin":
        st.markdown("---")
        st.subheader("⚙️ 工單管理")

        col_manage1, col_manage2 = st.columns(2)

        # 刪除工單
        with col_manage1:
            st.markdown("**🗑️ 刪除工單**")
            delete_id = st.selectbox(
                "選擇要刪除的工單",
                options=filtered["ticket_id"].tolist(),
                key="delete_select"
            )
            if st.button("🗑️ 確認刪除", type="primary"):
                st.session_state["confirm_delete"] = delete_id
            if "confirm_delete" in st.session_state:
                st.warning(f"⚠️ 確定要刪除工單 {st.session_state['confirm_delete']} 嗎？")
                col_yes, col_no = st.columns(2)

                with col_yes:
                    if st.button("✅ 確認"):
                        res = requests.delete(f"{API_URL}/tickets/{st.session_state['confirm_delete']}")
                        result = res.json()
                        if "message" in result:
                            st.session_state["delete_success"] = result["message"]
                            del st.session_state["confirm_delete"]
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('error', '刪除失敗')}")
                with col_no:
                    if st.button("❌ 取消"):
                        del st.session_state["confirm_delete"]
                        st.rerun()
            if "delete_success" in st.session_state:
                st.success(f"✅ {st.session_state['delete_success']}")
                del st.session_state["delete_success"]

        
        # 更新工單狀態
        with col_manage2:
            st.markdown("**✏️ 更新工單狀態**")
            update_id = st.selectbox(
                "選擇要更新的工單",
                options=filtered["ticket_id"].tolist(),
                key="update_select"
            )
            new_status = st.selectbox(
                "選擇更新狀態",
                ["待處理", "處理中", "已完成", "已拒絕"],
                key="status_select"
            )
            if st.button("✏️ 確認更新"):
                res = requests.patch(
                    f"{API_URL}/tickets/{update_id}/status",
                    json={"status": new_status}
                )
                result = res.json()
                if "message" in result:
                    st.session_state["update_success"] = result["message"]
                    st.cache_data.clear()
                    st.rerun()
                elif "error" in result:
                    st.error(f"❌ {result['error']}") 
                else:
                    st.error(f"❌ 未知錯誤:{result}")
            if "update_success" in st.session_state:
                st.success(f"✅ {st.session_state['update_success']}")
                del st.session_state["update_success"]

        
    if st.session_state["role"] == "admin":
        st.markdown("---")
        st.subheader("🚨 安全違規紀錄")

        try:
            res = requests.get(f"{API_URL}/security_logs")
            security_data = res.json()
            logs = security_data.get("logs", [])

            if logs:
                df_logs = pd.DataFrame(logs)
                df_logs = df_logs[["user_name", "timestamp", "message"]]
                df_logs.columns = ["用戶", "時間", "問題內容"]
                df_logs.index = range(1, len(df_logs) + 1)
                st.dataframe(df_logs, use_container_width=True)
            else:
                st.info("目前沒有安全違規紀錄")
        except:
                st.error("無法載入安全違規紀錄")
    

    

# ════════════════════════════════════════
# 頁面 4：新增工單
# ════════════════════════════════════════


elif page == "➕ 新增工單":
    st.subheader("➕ 新增工單")

    user_name = st.text_input("👤 你的名字",placeholder="例如:Alice")
    message   = st.text_input("❓ 問題描述",placeholder="例如:我的電腦無法開機")

    if st.button("🚀 提交工單", type="primary"):
       
       if not user_name.strip():
           st.warning("⚠️ 請輸入你的名字")
       elif not message.strip():
           st.warning("⚠️ 請輸入你的問題描述")
       else:
           with st.spinner("⏳ AI 正在分析問題..."):
               try:
                   res = requests.post(
                       f"{API_URL}/ask",
                       json={"message":message,"user_name":user_name}
                   )
                   data = res.json()
                   if data.get("category") == "安全違規":
                       st.error("❌ 此問題已被安全系統攔截，不予建立工單")
                   else:
                       st.toast("✅ 工單提交成功！",icon="🎉")
                       st.success(f"✅ 工單已建立！編號:{data.get('ticket_id','')}")
                       
                       st.session_state["chat_history"] = [
                           {"role": "user", "content":message},
                           {"role": "assistant", "content": data.get("solution", [])}
                       ]
                       st.session_state["username"] = user_name
                       st.session_state["ticket_id"] = data.get("ticket_id", "")

                   with st.expander("📋 查看 AI 分析結果", expanded=True):
                       col1,col2 = st.columns(2)
                       col1.metric("類別",   data.get("category",""))
                       col2.metric("嚴重程度", data.get("severity",""))

                       st.write("**解決步驟：**")
                       for i,step in enumerate(data.get("solution",[]),1):
                           st.write(f" {i}. {step}")
                       st.info(f"💬 {data.get('follow_up','')}")
               except Exception as e:
                   st.error(f"❌ 連線失敗:{e}")
    if st.session_state.get("chat_history"):
        st.markdown("---")

        for msg in st.session_state["chat_history"][2:]:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    if isinstance(msg["content"], list):
                        st.write("**解決步驟:**")
                        for i, step in enumerate(msg["content"], 1):
                            st.write(f"{i}. {step}")
                    else:
                        st.write(msg["content"])

        if "input_key" not in st.session_state:
            st.session_state["input_key"] = 0
        with st.form(key="follow_up_form", clear_on_submit=True):
             follow_up = st.text_input("💬 繼續追問", placeholder="輸入你的問題...")
             send = st.form_submit_button("送出")
        if send :
            if not follow_up:
                st.warning("⚠️ 請輸入問題")
            else:
                with st.spinner("⏳ AI 正在回答..."):
                   res = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": follow_up,
                        "user_name": st.session_state["username"],
                        "history": st.session_state["chat_history"]
                    }
                )
                   result = res.json()
                   if "error" not in result:

                     if result["type"] == "structured":
                        display_content = (result["data"]["solution"])
                     else:
                        display_content = result.get("content","")
                     st.session_state["chat_history"].append(
                        {"role":"user", "content": follow_up}
                    )
                     st.session_state["chat_history"].append(
                        {"role":"assistant", "content": display_content}
                    )
                     if st.session_state.get("ticket_id"):
                        requests.post(
                            f"{API_URL}/update_chat/{st.session_state['ticket_id']}",
                            json={
                            "user_name": st.session_state["username"],
                            "chat_history": st.session_state["chat_history"]
                            }
                        )
                     st.rerun()
                   else:
                     st.error(f"❌ {result['error']}")


# ── 重新整理按鈕 ──
st.markdown("---")
if st.button("🔄 重新整理資料"):
    st.cache_data.clear()
    st.rerun()
