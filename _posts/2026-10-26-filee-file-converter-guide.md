---
title: "Filee：把檔案格式轉換做成「滑鼠圓環」的免費離線轉檔工具"
date: 2026-10-26
description: "Filee 是開源的 Windows／Linux 離線檔案轉換器，拖到游標旁的圓環就能轉檔。本文整理它的核心功能、支援的格式、命令列用法、2.1.0 新功能與專案現況。"
tags: [Filee, 檔案轉換, 開源專案, Windows, 生產力工具, GitHub]
---

![Filee](/assets/images/filee/banner-en.jpg)

多數人對「轉檔工具」的印象，大概是開一個網頁、上傳檔案、等它跑完，然後下載一個改了名字的檔案——順便祈禱裡面的合約不要被留在別人的伺服器上。**Filee** 走的是完全相反的路線：它是一個裝在電腦裡的桌面程式，把轉檔這件事情變成「把檔案拖到游標旁邊的圓環上」這樣一個手勢。

專案網址：[github.com/KnifeLemon/Filee](https://github.com/KnifeLemon/Filee) · 官網：[filee.sh](https://filee.sh)

- **技術堆疊**：C#／.NET 10
- **平台**：Windows、Linux（macOS 預覽版）
- **授權**：MIT
- **作者**：Myeonggu Kim（KnifeLemon），36 位貢獻者
- **最新版本**：2.1.0（2026-10-24 發佈），GitHub Releases 累計下載約 34.5 萬次

## 一、核心互動：游標旁的圓環（Donut）

Filee 最具辨識度的設計，是把所有格式與操作排成一個**跟著滑鼠游標出現的圓環工具列**：

1. 按住快捷鍵，圓環出現在游標旁邊。
2. 把檔案拖進圓環，游標移到想要的格式上放開，轉換就開始。

圓環只顯示**適合這批檔案的格式**——拖一張 HEIC 進來，它不會給你 PDF 以外一堆用不到的選項；拖一個 PDF 進來，它給的是圖片、DOCX、TXT 這些。這消除了傳統轉檔軟體「先選類別、再選格式、再看它到底支不支援」的來回摸索。

幾個延伸設計：

- **圓環有背面**：圓環打開時按 <kbd>Tab</kbd> 或滾動滑鼠滾輪可以「翻面」，背面放的是不常用的格式與工具，讓正面保持乾淨。
- **每種檔案類型一個工具列**：版面可以拖放排列，順序自己決定。
- **直接從瀏覽器拖**：Chrome、Edge、Firefox、Safari 裡的圖片、檔案連結、下載項目都能直接往圓環上拖；Filee 會先存到「下載」資料夾（也可設定只保留轉換後的結果），再進行轉換，而且連結下載**不會使用瀏覽器的登入資訊**。
- **多入口操作**：除了圓環，還有右鍵選單、鍵盤快速鍵、首頁的拖放區，以及 `filee` 命令列。

## 二、轉換前可先調整：預設與裁剪

單純的格式轉換之外，Filee 也把常見的「轉檔前微調」做進了同一條流程：

- **每種格式都有專屬預設**：品質、尺寸、DPI；PDF 的頁面範圍與壓縮；影片的音訊參數；輸出的儲存位置與檔名規則。
- **轉換前先裁剪**：選「裁剪」後會逐張開啟圖片，拖曳選框、挑選比例，只儲存選取的區域。
- **批次與多步轉換**：一次可以丟多個檔案（平行處理）；需要多個步驟才能完成的格式（例如 HWP → HWPX → DOCX）會**自動找出轉換路線**，不需要使用者自己拼流程。
- **監視資料夾**：指定一個資料夾，丟進去的檔案自動轉換，適合固定的收件／輸出流程。
- **最近的轉換**：首頁列出最近處理的項目，每項都有縮圖，可以直接「開啟檔案」，或用「開啟方式」改用其他應用程式打開。

另外，介面提供淺色／深色主題、自選強調色、圓環工具列透明度，並支援 **18 種語言**：English、Español、日本語、한국어、简体中文、繁體中文、Polski、हिन्दी、Русский、العربية（支援從右到左）、Português (Brasil)、Français、नेपाली、ไทย、Türkçe、Português (Portugal)、Deutsch 等。

<table>
  <tr>
    <td width="50%"><img src="/assets/images/filee/page-toolbar-en.png" alt="用預設與描述檔編輯圓環工具列"></td>
    <td width="50%"><img src="/assets/images/filee/page-home-en.png" alt="帶拖放區和最近轉換記錄的首頁"></td>
  </tr>
  <tr>
    <td align="center"><sub>拖放排列圓環，每種檔案類型一個設定檔</sub></td>
    <td align="center"><sub>首頁的拖放區與最近轉換記錄</sub></td>
  </tr>
</table>

## 三、支援格式：從手機照片到 CAD 圖紙

Filee 支援的廣度是它最有殺傷力的地方。下表整理主要類別（完整清單見 repo 內的 README）：

| 類別 | 代表來源格式 | 主要目標格式 |
|---|---|---|
| **圖片** | JPG、PNG、WEBP、AVIF、TIFF、HEIC、JPEG XL、PSD、相機 RAW（CR2/CR3/NEF/ARW/DNG）、DICOM、OpenEXR、HDR、FITS、iPhone 原況照片 | 彼此互轉、PDF、SVG（描摹）、縮放、灰階；原況／動態照片取出影片，或影片製作原況照片（實驗） |
| **向量圖** | SVG、SVGZ、EMF、WMF、AI、EPS、PS、CDR、VSD、CGM、ODG | PDF（向量）、PNG、SVG ↔ SVGZ、SVG → DXF/DWG 等 |
| **PDF** | PDF | DOCX、HWPX、TXT、PNG、JPG、TIFF、CBZ、PPTX；合併、拆分、頁碼範圍、壓縮 |
| **文件** | DOCX、DOCM、EML、Outlook MSG、OFD、DOC、ODT、RTF、WPS、Pages | PDF、DOCX、HWPX、EPUB、TXT、HTML；MSG → EML |
| **試算表** | XLSX、XLS、ODS、CSV、TSV、Numbers | PDF、XLSX、ODS、CSV、TSV、JSON、HWPX、HTML |
| **簡報** | PPTX、PPT、ODP、Keynote | PDF、PNG、JPG、DOCX、HWPX |
| **HWP** | HWP、HWPX（韓國文書格式） | PDF、PNG、DOCX、TXT、Markdown、HTML、HWP ↔ HWPX |
| **文字** | TXT、Markdown、HTML、MHTML、reST、LaTeX、Org、AsciiDoc、Typst、Jupyter | UTF-8 TXT、PDF、DOCX、HWPX、EPUB、PPTX |
| **電子書** | EPUB、MOBI、AZW3、FB2、CBZ、CBR、CHM | PDF、EPUB、KEPUB、AZW3 等 |
| **影片／音訊** | MP4、MKV、AVI、MOV、HEVC、AV1、MP3、FLAC、WAV、DSD、AC3 | MP4（H.264/HEVC/AV1）、WEBM、MKV、GIF、MP3、M4A，含字幕（SRT/ASS/WebVTT） |
| **壓縮檔** | ZIP、7Z、RAR、TAR、ISO、CAB、DMG | 解壓縮、ZIP/7Z/TAR、多檔打包成一個 ZIP |
| **CAD／字型／資料** | DWG、DXF；TTF、OTF、WOFF2；JSON、YAML、TOML、XML、vCard、iCalendar | PDF／SVG／PNG；字型互轉；資料互轉與 CSV/XLSX |
| **3D 模型** | GLB、glTF、STL、OBJ、3MF、PLY | 互轉、PNG 預覽 |
| **地理資訊** | Shapefile、GeoJSON、KML、KMZ、GPX | 互轉、CSV／XLSX／JSON，投影座標自動轉 WGS 84 |

值得強調的是：**未特別標註的格式裝好即用**，不需要安裝 Office、韓文文書軟體或 LibreOffice。少數格式需要可選引擎（Ghostscript、LibreOffice、Pandoc、calibre、FFmpeg），這些引擎只在真的用到時才下載，不佔用基本安裝。

### 引擎設定

![引擎設定畫面](/assets/images/filee/engine-setup-en.png)

可選引擎的安裝與版本由 Filee 自己管理，需要時才會跳出下載；已安裝的引擎與設定在升級版本時會保留。

## 四、命令列：同一套引擎的 `filee`

圖形介面之外，Filee 提供 `filee` 命令（由安裝程式或 `install.sh` 加入 PATH），使用與應用程式**相同的引擎與預設**：

```bash
filee convert photo.heic --to jpg
filee convert *.png --to webp --quality 80 -o converted
filee watch D:\Inbox --to pdf --move-originals
```

它支援萬用字元、整批資料夾、監視資料夾，並提供 JSON 輸出與結束代碼，方便寫進腳本或排程。全部命令與選項見官網的 [Command Line 頁面](https://filee.sh/cli/) 或 `filee help`。

## 五、2.1.0（2026-10-24）帶來的能力

最新一版把 Filee 從「轉檔器」推向「檔案工具工作台」：

| 新功能 | 說明 |
|---|---|
| **OCR 文字辨識** | 辨識掃描件與圖片中的文字，輸出可搜尋的 PDF，或可直接編輯的文件 |
| **媒體處理** | 壓縮、合併、清除照片／影片／音訊的中繼資料，並可從影片剪出片段 |
| **PDF 編輯** | 編輯 PDF 頁面；為任意 PDF 加上浮水印、頁碼或密碼 |
| **表格與試算表** | PDF 中的表格可轉成 Excel 工作表；大型 Excel 轉 PDF 明顯加速；存 PDF 前可排版分頁、可選 AutoCAD 版本 |
| **替換原檔** | 開啟後結果直接放回原檔位置，原檔送進資源回收筒 |
| **更多格式** | FITS 天文照片、iCalendar、HAR、USM 遊戲影片、刺繡與繪圖機檔案，CAD 每個配置各出一頁 PDF |
| **程式碼簽章** | Windows 版本以 Certum 開源簽章憑證簽署，降低被 Smart App Control 與防毒軟體攔截的機率 |
| **介面與平台** | 新增法語、繁體中文、尼泊爾語、泰語、土耳其語、歐洲葡語與 Material You 主題、視窗縮放；Linux 可直接在程式內更新，並支援 GNOME／Hyprland Wayland 的拖曳手勢（實驗） |

前一個大版 **2.0.0** 則是介面層的轉折點：改用自家 Windows 安裝程式、瀏覽器直接拖曳、圓環翻面、新的裁剪工具（在圖片上按 <kbd>A</kbd> 就地選比例）、Live Photo／Motion Photo 的影片取出，以及西班牙語、日語、俄語、阿拉伯語等介面。

![圓環工具列的深色模式](/assets/images/filee/page-toolbar-dark.png)

## 六、隱私與專案現況

- **完全離線**：Filee 不上傳檔案，也不傳送任何使用資料。這對處理合約、病歷、發票（支援台灣常用的 OFD 電子發票讀取）這類檔案相當關鍵。
- **純本機引擎**：轉換是在自己的電腦上跑，不是把檔案送到雲端。
- **開發狀態活躍**：CHANGELOG 記錄了 22 個版本，2026-10-19 到 10-24 之間連續發佈 1.12.0、2.0.0、2.1.0 三個版本。
- **可擴充**：專案提供 [架構文件](https://github.com/KnifeLemon/Filee/blob/main/docs/ARCHITECTURE.md)、[新增轉換器](https://github.com/KnifeLemon/Filee/blob/main/docs/ADDING-A-CONVERTER.md)、[新增語言](https://github.com/KnifeLemon/Filee/blob/main/docs/ADDING-A-LANGUAGE.md) 等指南，歡迎 PR。
- **免費且持續免費**：以 MIT 授權釋出，靠 GitHub Sponsors、Patreon、Ko-fi、PayPal 等自願贊助維持。

![Star 成長趨勢](/assets/images/filee/star-history.svg)

## 七、適合誰用

- **常常要把同一批檔案轉來轉去的人**：手機 HEIC 照片、掃描 PDF、Office 文件、電子書、字幕、影片，一個圓環解決。
- **在乎隱私、不願意上傳檔案的人**：醫療影像、法務文件、公司內部試算表都能留在本機。
- **需要自動化的人**：`filee watch` 加上結束代碼與 JSON 輸出，可以直接接進排程或 CI 流程。
- **跨格式的少見需求**：DWG/DXF、Shapefile/KML、TTF/WOFF2、HWP、OFD、FITS——這些通常是「找不到工具就放棄」的格式，Filee 直接內建。

如果你只是想找一個裝好就不必再開瀏覽器分頁的轉檔工具，Filee 的入門成本大概是三秒：裝好、按住快捷鍵、把檔案拖進圓環。

專案首頁：[github.com/KnifeLemon/Filee](https://github.com/KnifeLemon/Filee)（MIT 授權，Windows／Linux，macOS 預覽）
