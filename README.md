# 🖥️ IT Helpdesk AI 助手

一個結合 Claude AI 的智慧 IT 技術支援系統，能自動診斷問題、提供解決步驟、支援多輪對話追問，並完整記錄工單與對話歷史。

---

## 🚀 功能特色

### AI 核心功能
- 🤖 AI 自動診斷 IT 問題並提供逐步解決方案
- 💬 多輪對話追問（使用者可針對回答繼續追問）
- 📋 問題自動分類（硬體／軟體／網路／其他）
- ⚠️ 嚴重程度自動評估（低／中／高）

### 安全防禦
- 🛡️ 雙層 Prompt Injection 防禦（關鍵字過濾 + AI 語意分析）
- 🚨 安全違規自動記錄與管理員通知

### 工單管理
- 📁 自動建立工單並儲存完整對話歷史
- 🗂️ 工單明細查看（含篩選、排序、CSV 匯出）
- 💬 查看工單完整問答對話紀錄
- ✏️ 管理員更新工單狀態（待處理／處理中／已完成／已拒絕）
- 🗑️ 管理員刪除工單（含二次確認機制）

### 儀表板
- 📊 工單統計總覽（數量、類別分佈、嚴重程度）
- 📈 進階分析（趨勢圖、用戶分析）
- 🔐 權限管理（訪客／管理員雙角色）

---

## 🛠️ 技術架構

| 層級 | 技術 |
|------|------|
| AI 模型 | Anthropic Claude API（claude-haiku） |
| 後端框架 | FastAPI |
| 前端介面 | Streamlit |
| 語言 | Python 3 |
| 資料儲存 | JSON 檔案 |
| 安全防禦 | Prompt Injection 雙層防禦 |

---

## 📡 API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/` | 服務狀態 |
| POST | `/ask` | AI 診斷問題並建立工單 |
| POST | `/chat` | 多輪對話追問 |
| GET | `/tickets` | 取得所有工單 |
| PATCH | `/tickets/{id}/status` | 更新工單狀態 |
| DELETE | `/tickets/{id}` | 刪除工單 |
| POST | `/update_chat/{id}` | 更新工單對話歷史 |
| GET | `/security_logs` | 取得安全違規記錄 |

---

## ⚙️ 安裝與執行

### 1. 複製專案
```bash
git clone https://github.com/Nathennnn1/it-helpdesk-ai.git
cd it-helpdesk-ai
```

### 2. 安裝套件
```bash
pip install -r requirements.txt
```

### 3. 設定環境變數
建立 `.env` 檔案：
```
ANTHROPIC_API_KEY=你的API_KEY
ADMIN_PASSWORD=你的管理員密碼
```

### 4. 啟動後端
```bash
python -m uvicorn api:app --reload
```

### 5. 啟動前端
```bash
streamlit run streamlit_dashboard.py
```

### 6. 開啟 API 文件
```
http://127.0.0.1:8000/docs
```

---

## 💡 使用範例

發送 POST 請求到 `/ask`：
```json
{
  "message": "我的電腦無法連上網路",
  "user_name": "Nathen"
}
```

回應結果：
```json
{
  "category": "網路",
  "severity": "高",
  "solution": [
    "檢查網路線是否正確連接",
    "重新啟動路由器",
    "檢查 IP 設定是否正確"
  ],
  "follow_up": "請問是有線還是無線網路的問題？",
  "ticket_id": "20260507174419",
  "status": "待處理"
}
```

---

## 🔒 安全機制說明

本系統實作雙層 Prompt Injection 防禦：

1. **第一層：關鍵字過濾**  
   偵測常見的惡意指令關鍵字（如「忽略指令」、「扮演」等），即時攔截。

2. **第二層：AI 語意分析**  
   將輸入送交 AI 判斷是否為非 IT 相關的惡意提示，提高防禦精確度。

所有違規行為自動記錄，管理員可在儀表板查看完整記錄。

---

## 作者

- **Nathen** - SI/Helpdesk 工程師轉 AI 工程師
- GitHub: [@Nathennnn1](https://github.com/Nathennnn1)

---

## 線上 Demo

部署於 Render：https://it-helpdesk-ai.onrender.com
