---
title: "Deskflow：一套鍵盤滑鼠控制所有電腦——開源軟體版 KVM（Synergy 的正統血統）"
date: 2026-11-06
description: Deskflow（30.7k stars，C++，GPL-2.0）：跨 Windows/macOS/Linux/BSD 的鍵盤滑鼠共享，滑過螢幕邊界就切到下一台電腦。TLS 預設加密、剪貼簿共用、Wayland 原生支援、與 Synergy 1/Input Leap/Barrier 網路互通。從 2001 年 Synergy 走來的開源正統分支。
tags: [github, productivity, keyboard-mouse-sharing, kvm, synergy, wayland, cross-platform, opensource, utility]
---

# Deskflow：一套鍵盤滑鼠控制所有電腦——開源軟體版 KVM

![Deskflow logo](/assets/images/deskflow/logo.png)

**Deskflow**（`deskflow/deskflow`，官方站 [deskflow.org](https://deskflow.org)）是一個**免費開源的鍵盤滑鼠共享應用**：用一台電腦的鍵盤、滑鼠或觸控板，直接控制旁邊的幾台電腦——**滑鼠指針移到螢幕邊界，就「滑進」另一台電腦**，像軟 KVM 但不含影像。

它是 Synergy 開源血統的正統繼承者：2001 年 Chris Schoeneman 創造 Synergy → 商業化後開源分支經歷 Synergy → Barrier（已死）→ Input Leap（停更）→ **Deskflow（活躍維護中）**。

## 專案概況

| 項目 | 資料 |
|---|---|
| 倉庫 | [github.com/deskflow/deskflow](https://github.com/deskflow/deskflow) |
| Star / Fork | **~30,700 / ~5,100**（2026-11-06 查證） |
| 語言 / 授權 | **C++**（Qt 6 GUI）/ GPL-2.0（含 OpenSSL exception） |
| 歷史 | 倉庫建於 2014，血統可追到 2001 年的 Synergy |
| 最新版本 | **v1.27.0**（2026-10-01）；continuous 版持續構建（最新 2026-11-03） |
| 平台 | Windows 10 1809+ / macOS 12+（Apple Silicon CI 版要 13+）/ Linux（X11 + **Wayland**）/ FreeBSD 官方支援 |
| 安裝 | GitHub Releases、各發行版套件、Flathub、macOS 官方 Homebrew tap |

## 它是怎麼運作的

- **一台 Server**（接鍵盤滑鼠那台）+ **N 台 Client**，走區域網路（預設 port 24800）
- 在 GUI 裡擺電腦方塊圖決定相鄰關係；滑鼠推到邊界即切換控制權
- 輸入事件由 Server 產生為「模擬輸入」注入 Client——所以**任何應用都適用**，不需要對方裝驅動或外掛
- **TLS 加密預設開啟**；支援 TLS 憑證指紋驗證防中間人

## 功能清單

| 功能 | 說明 |
|---|---|
| 邊界切換 | 滑鼠跨螢幕邊界自動切換鍵盤滑鼠控制權，支援多螢幕多排配置 |
| **剪貼簿共用** | 核心招牌功能：跨機複製貼上（文字/圖片），官方承諾長期維護 |
| TLS 加密 | 預設開啟，傳輸內容加密 |
| 鍵盤熱鍵綁定 | 可設定修飾鍵組合在切換時跟隨（如 Ctrl+Alt+Del 對應到目標機） |
| 螢幕鎖定同步 | Server 鎖定時 Client 一起鎖（安全合規場景常用） |
| **Wayland 原生支援** | 透過 `libei` + `libportal`，是開源鍵鼠共享裡最早做 Wayland 的 |
| 協議互通 | 與 Input Leap、Barrier「直接可用」；接 Synergy 1 server 直接可用；Synergy 1 client 需在 server 端選 Synergy 協議（Synergy 3 不相容） |
| 無伺服器模式 | Client 可快取設定，斷網時沿用上次配置 |

## 各平台安裝要點

- **Windows**：需裝 [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)；作為 client 控制需管理員權限時注意 UAC 場景
- **macOS**：要在「隱私與安全性」給 `Deskflow` app 和 `deskflow` process **輔助使用（Accessibility）**權限；Sequoia 起還要在 Local Network 放行。官方未做 Apple 公證，直接下載會報「damaged」——跑 `xattr -c Deskflow.app` 解 quarantine。**推薦用官方 tap**：
  ```bash
  brew tap deskflow/tap
  brew install deskflow        # 穩定版
  brew install deskflow-dev    # continuous 版
  ```
- **Linux**：native 套件需 libei 1.3+ / libportal 0.8+ / Qt 6.7+（GUI）；太舊的系統改裝 Flathub 版 `org.deskflow.deskflow`
- **FreeBSD**：官方支援；OpenBSD/NetBSD/Solaris 在支援清單願景中

## 適用場景

- **桌上多台機器**：工作筆電 + 個人桌機 + Linux 工作站，一套鍵盤滑鼠全部通，不用買 KVM 切換器
- **跨平台開發**：macOS 寫程式、Linux 編譯測試、Windows 測相容性——剪貼簿直接互貼
- **機房/測試/lab**：多台測試機集中操作；螢幕鎖定同步符合安全合規需求
- **筆電 + 桌機組合**：Home 用筆電、Office 用桌機，Deskflow 讓兩台共用一套Peripheral
- **Wayland Linux 用戶**：Input Leap 停更後，Deskflow 是 Wayland 鍵鼠共享的首選

## 與同類方案比較

| | **Deskflow** | Synergy（商業） | Input Leap | Lan Mouse | 硬體 KVM 切換器 |
|---|---|---|---|---|---|
| 授權/價格 | GPL-2.0 免費 | 付費（約 $10+） | GPL 免費 | MIT 免費 | 硬體一次購買 |
| 維護狀態 | ✅ 活躍（每週有 commit） | ✅ 商業支援 | ❌ inactive | ✅ 活躍（Rust） | — |
| 剪貼簿共用 | ✅ | ✅ | ✅ | ✅（文字） | 通常無 |
| Wayland | ✅ libei | ✅ | 部分 | ✅ | 不適用 |
| 與 Synergy 1 互通 | ✅ | ✅ | ✅(Barrier 系) | ❌ | — |
| 影像 | ❌ | ❌ | ❌ | ❌ | ✅（KVM 含螢幕） |

選擇邏輯：**要免費開源+活躍維護 → Deskflow；要商業支援與开箱精靈 → Synergy；只要純 Linux 輕量 → Lan Mouse；需要連螢幕影像一起切 → 硬體 KVM。**

## 已知注意事項

- macOS 未公證：直接下載的 zip 會被 Gatekeeper 擋，`xattr -c` 一行解決；用 Homebrew 最省事
- 升級版 macOS 權限問題：舊版在輔助使用清單裡的話要**先移除再重新授權**
- Wayland 部分功能仍有已知問題（官方討論區 #7499 追蹤中）
- 全部走內網，但建議只在可信網路使用並保留 TLS 預設開啟

## 參考資料

- 官方站：[https://deskflow.org](https://deskflow.org)
- GitHub：[https://github.com/deskflow/deskflow](https://github.com/deskflow/deskflow)
- Releases：[https://github.com/deskflow/deskflow/releases/latest](https://github.com/deskflow/deskflow/releases/latest)
- Flathub：[org.deskflow.deskflow](https://flathub.org/apps/org.deskflow.deskflow)
- 專案歷史 wiki：[History of Deskflow](https://github.com/deskflow/deskflow/wiki/History)
