# BotRun Ask Folder

這個專案提供了一個從 Google Drive 資料夾下載文件並處理成嵌入式向量，最後將其上傳到 Qdrant 的工具。以下是如何使用這個工具的說明。

---

## 安裝

請先確保您已經安裝 Python 以及 pip。然後，您可以使用以下指令來安裝這個專案的依賴套件：

```sh
pip install -r requirements.txt
```

或者直接使用 `pyproject.toml` 來進行安裝：

```sh
pip install .
```

---

## 使用方法

### 調用 `botrun_ask_folder`

`botrun_ask_folder` 函數可以幫助您下載指定 Google Drive 資料夾中的文件，進行處理並上傳到 Qdrant。

```python
from botrun_ask_folder import botrun_ask_folder

# Google Drive 資料夾ID
google_drive_folder_id = "your_google_drive_folder_id"

botrun_ask_folder(google_drive_folder_id)
```

### 所需環境變數
在運行此工具前，請設置以下環境變數：

| 環境變數                  | 說明                                 |
| -------------------------- | -------------------------------------- |
| GOOGLE_APPLICATION_CREDENTIALS | 用於Google服務帳戶的憑證路徑          |
| QDRANT_HOST                | Qdrant 伺服器的主機名 (默認為 "qdrant") |
| QDRANT_PORT                | Qdrant 伺服器的埠號 (默認為 6333)      |

### 其他相關套件

請參考以下套件來幫助您實現完整的功能：

- `drive_download`: 從 Google Drive 下載文件。
- `run_split_txts`: 將下載的文件切分成指定大小的文本片段。
- `embeddings_to_qdrant`: 將文本片段轉換為嵌入式向量並上傳到 Qdrant。
- `botrun_drive_manager`: 管理和更新 Qdrant 上的資料。

---

## 版本資訊
當前版本：4.6.9

---

## 貢獻

歡迎各種形式的貢獻。請提交 pull requests 或創建 issue。

---

## 授權
本專案使用 MIT 授權。如需更多資訊，請查閱 LICENSE 文件。