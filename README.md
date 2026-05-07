# IT Helpdesk AI 助手

一個結合 Claude AI 的智慧 IT 技術支援系統，能自動診斷問題、提供解決步驟並記錄工單。

## 功能特色

- 🤖 AI 自動診斷 IT 問題
- 📋 問題自動分類（硬體／軟體／網路／其他）
- ⚠️ 嚴重程度評估（低／中／高）
- 🔧 提供逐步解決方案
- 📁 自動建立工單記錄
- 🌐 RESTful API 服務

## 技術架構

- **語言**：Python 3
- **AI 模型**：Anthropic Claude API
- **後端框架**：FastAPI
- **部署平台**：Render

## 安裝與執行

### 1. 複製專案
git clone https://github.com/Nathennnn1/it-helpdesk-ai.git
cd it-helpdesk-ai

### 2. 安裝套件
pip install -r requirements.txt

### 3. 設定環境變數
建立 .env 檔案：
ANTHROPIC_API_KEY=你的API_KEY

### 4. 啟動服務
python -m uvicorn api:app --reload

### 5. 開啟 API 文件
http://127.0.0.1:8000/docs

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | / | 服務狀態 |
| POST | /ask | 詢問 AI 診斷問題 |
| GET | /tickets | 查看所有工單 |

## 使用範例

發送 POST 請求到 /ask：

{
  "message": "我的電腦無法連上網路",
  "user_name": "Nathen"
}

回應結果：

{
  "category": "網路",
  "severity": "高",
  "solution": [
    "檢查網路線是否正確連接",
    "重新啟動路由器",
    "檢查 IP 設定"
  ],
  "follow_up": "請問是有線還是無線網路的問題？",
  "ticket_id": "20260507174419"
}

## 作者

- **Nathen** - SI/Helpdesk 工程師轉 AI 工程師
- GitHub: [@Nathennnn1](https://github.com/Nathennnn1)

## 線上 Demo

部署於 Render：https://it-helpdesk-ai.onrender.com