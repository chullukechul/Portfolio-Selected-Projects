# Video Upload Automation Pipeline：YouTube 教學影片自動化發布系統

## 📝 專案概述與解決痛點
在教學場域中，每日將錄製好的教學影片上傳至 YouTube 並進行各項發布設定（如隱私權、兒童保護政策等），是一項高度重複且耗時的例行公事。人工操作不僅佔用寶貴的備課時間，也容易因疲勞導致設定遺漏或檔案重複上傳。

本專案旨在建立一套**無人值守（Unattended）的自動化上傳管線**。透過系統排程與網頁自動化技術，徹底消除人為操作介入，實現高可靠性的影片自動化佈署流程。

## 🎯 專案成效 (Impact)
* **解放勞動力**：實現夜間自動觸發機制，每日節省約 20 分鐘的繁瑣工時，讓精力回歸核心教學與研發任務。
* **零人為失誤**：透過程式邏輯嚴格把關上傳參數（自動勾選非兒童專屬、自動設為私人影片），完全消除手動設定的漏勾或點錯問題。
* **防呆與狀態管理**：上傳完成後自動修改本地端檔名（標記「已上傳」），避免系統重複抓取與上傳相同檔案。

## 🛠️ 系統架構與使用技術
* **核心語言**：Python 3
* **網頁自動化**：Selenium WebDriver (搭配 `webdriver_manager` 動態配置驅動程式)
* **系統排程與腳本**：Windows Task Scheduler, Batch Scripting ( `.bat` )

## ⚙️ 核心工程挑戰與實作亮點 (Engineering Highlights)

### 1. 動態網頁的非同步等待機制 (Asynchronous UI Handling)
YouTube Studio 是高度動態的單頁面應用程式 (SPA)。本專案棄用脆弱的硬編碼延遲 (`time.sleep`)，全面採用 `WebDriverWait` 與 `expected_conditions (EC)`，精準監聽 DOM 元素的渲染狀態（如 `presence_of_element_located` 與 `element_to_be_clickable`），確保腳本在網路延遲或 UI 載入緩慢時依然能穩定執行。

### 2. 身份驗證與異常處理 (Authentication & Exception Handling)
針對 Google 嚴格的登入驗證機制，腳本內建了雙重防護邏輯。透過 `try-except` 區塊主動偵測並捕捉可能隨機出現的「二次登入確認」要求，確保無人值守狀態下，登入流程不會因未預期的安全性攔截而中斷。

### 3. 多階段表單提交流程自動化 (Multi-step Wizard Automation)
利用精確的 XPath 定位，程式化模擬人類操作行為，精確穿越 YouTube 複雜的三階段上傳引導表單：
* 注入本地端檔案路徑至隱藏的 `<input type='file'>` 節點。
* 精準擊發表單中的特定選項（如「這不是為兒童設計」）。
* 依序點擊「下一步」並最終鎖定為「私人影片」後儲存。

### 4. 作業系統層級整合 (OS-Level Integration)
將 Python 腳本封裝入 Batch Script，並介接 Windows Task Scheduler，利用作業系統的排程器實現真正的全自動化，無需手動開啟終端機或 IDE 即可在背景完成每日任務。