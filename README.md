# JeiKai DDoS

![License](https://img.shields.io/badge/license-MIT-green)  
**作者：GogoZin**

---

## 🔍 簡介

**JeiKai** 是一款免費且開源的壓力測試工具，專為開發者與測試人員設計。

你可以使用 JeiKai 進行網站抗攻擊能力測試，包括：

- 每秒請求上限
- HTTP/2 特性測試
- 標頭 (Header) 規則測試
- TCP 連線數測試

讓你能夠更輕鬆地找到適合你網站的防火牆設定。

---

## 💻 安裝方式

### Windows

1. 確保你已安裝 [Python 3](https://www.python.org/)。
2. 下載此專案的 `.zip` 並解壓縮至任意目錄。
3. 安裝必要模組：

   ```bash
   py -m pip install colorama h2
   ```

### Linux

1. 使用 Git 下載或解壓縮 ZIP。
2. 安裝必要模組：

   ```bash
   pip3 install colorama h2
   ```

---

## 🚀 使用方式

開啟終端機並移動到專案所在目錄：

- **Windows:**

  ```bash
  py jeikaidos.py
  ```

- **Linux:**

  ```bash
  python3 jeikaidos.py
  ```

---

## 🖥️ 系統建議需求

- 至少 **4 核心 CPU**
- 至少 **4GB RAM**

---

## 🔧 支援的請求模式

JeiKai 提供 4 種請求模式來模擬不同攻擊方式：

1. **Http Plain Flood**  
   傳統的 HTTP 請求方式，內含常見標頭。

2. **HTTP/2 Rapid Reset + Continuation Flood**  
   模擬 HTTP/2 連線重置與大標頭混合攻擊。

3. **PPS（Package per Second）Flood**  
   模擬最大封包傳輸量，只包含 `Connection` 標頭。

4. **Bypass 模式**  
   加入 `sec-ch` 與 `fetch` 標頭，更貼近真實瀏覽器行為。

5. **Basic UDP Flood**

   最常見的 UDP 洪流 , 不關閉socket持續發送random udp
---

## 📜 授權條款

本專案使用 [MIT License](LICENSE)。

---

## ⚠️ 使用規章

> ⚠️ **請勿濫用此腳本**，此工具僅供開發與安全測試用途。  
>  
> 若您將其用於非法用途，一切後果與作者無關。  
> 下載或使用本專案即表示您同意此規章。不同意者請勿下載或使用。

---

感謝使用 JeiKai，歡迎 star ⭐ 支持！
