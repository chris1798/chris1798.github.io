---
title: "Graphify: Flutter Apache ECharts 圖表庫完整功能介紹"
date: 2026-07-29
description: 深入解析 Graphify Flutter 圖表庫的核心功能、支援的圖表類型、跨平台特性及實作方式
tags: [flutter, graphify, echarts, data-visualization, open-source]
---

# Graphify: Flutter Apache ECharts 圖表庫完整功能介紹

Graphify 是一個強大的 Flutter 套件，作為 Apache ECharts 的橋接器，讓開發者能夠在 Flutter 應用程式中建立互動式圖表與資料視覺化。本文將完整介紹 Graphify 的所有功能特性。

![Graphify Banner](/assets/images/graphify/banner.png)

## 基本資訊

| 屬性 | 內容 |
|------|------|
| **專案名稱** | Graphify |
| **開發者** | warioddly |
| **授權** | MIT License |
| **最新版本** | 1.2.0 |
| **狀態** | Archive (自 2026-05-09 起封存) |
| **GitHub Stars** | 96 ⭐ |
| **Forks** | 18 |

## 支援的圖表類型

Graphify 支援多種高階圖表類型，包括：

### 1. WebGL 3D 圖表
![3D Chart](/assets/images/graphify/bar_3d_chart.gif)

支援三維立體圖表，適合展示複雜的三維數據關係。

### 2. 折線圖 (Line Chart)
互動式折線圖，支援多系列、座標軸自訂、tooltip 顯示等功能。

### 3. 長條圖 (Bar Chart)
![Bar Chart](/assets/images/graphify/graph_webkit_dep.gif)

支援水平/垂直長條圖、堆疊長條圖、雙軸長條圖等。

### 4. 蠟燭圖 (Candlestick Chart)
![Candlestick](https://raw.githubusercontent.com/warioddly/graphify/main/README/README.assets/candle_stick_brush.gif)

專為金融數據設計，支援 brush 選取、zoom 縮放等功能。

### 5. 雷達圖 (Radar Chart)
適合多維度數據比較與分析。

### 6. 圖表 (Graph Chart)
![Graph](https://raw.githubusercontent.com/warioddly/graphify/main/README/README.assets/graph_webkit_dep.gif)

支援節點、邊、關係圖等複雜網路結構。

### 7. 樹狀圖 (Tree Chart)
適合展示層級結構與組織架構。

### 8. 所有圖表類型
![All Charts](https://raw.githubusercontent.com/warioddly/graphify/main/README/README.assets/all.gif)

Graphify 完整支援 Apache ECharts 的所有圖表類型。

## 核心功能特性

### 🌐 跨平台支援

Graphify 支援多平台開發：

| 平台 | 支援狀態 | 說明 |
|------|----------|------|
| **Web** | ✅ 完整支援 | 使用 Apache ECharts 原生渲染 |
| **Android** | ✅ 完整支援 | 透過 WebView 或原生整合 |
| **iOS** | ✅ 完整支援 | 透過 WebView 或原生整合 |
| **Windows** | ✅ 完整支援 | 使用 `dart:ffi` 方案（替代 `dart:ui_webview`） |
| **Linux** | ✅ 完整支援 | 透過原生整合 |
| **macOS** | ✅ 完整支援 | 透過原生整合 |

### 🔧 技術架構

**新版本技術架構（v1.0.0+）：**
- 使用 `dart:ffi` 進行 Windows 原生整合
- 使用 `package:web` 進行 Web 平台整合
- 替代舊版 `dart:ui_webview` 插件

**依賴套件：**
```yaml
dependencies:
  graph_webkit_dep: ^1.0.0  # Windows 原生整合
  graph_webkit_web_dep: ^1.0.0  # Web 平台整合
```

### 📊 互動功能

- **Zoom 縮放**：支援滑鼠滾輪、觸控縮放
- **Pan 平移**：拖曳平移檢視
- **Brush 選取**：區域選取與篩選
- **Tooltip 提示**：懸停顯示詳細數據
- **Legend 圖例**：互動式圖例切換
- **DataView 資料檢視**：表格化資料顯示
- **Toolbox 工具列**：匯出、縮放等快捷工具

### 🎨 自訂能力

- 完整的 Apache ECharts option 配置
- 主題色自訂
- 動畫效果控制
- 響應式設計
- 事件回調處理

### 📱 Flutter 原生整合

- 純 Flutter widget 實作
- 狀態管理整合
- 響應式佈局支援
- 事件處理機制

## 安裝方式

### 1. 依賴設定

在 `pubspec.yaml` 中加入：

```yaml
dependencies:
  flutter:
    sdk: flutter
  graphify: ^1.2.0
```

### 2. 平台特定依賴

**Web 平台：**
```yaml
dependencies:
  graph_webkit_web_dep: ^1.0.0
```

**Windows 平台：**
```yaml
dependencies:
  graph_webkit_dep: ^1.0.0
```

### 3. 執行命令

```bash
flutter pub get
```

## 快速開始

### 基本用法

```dart
import 'package:flutter/material.dart';
import 'package:graphify/graphify.dart';

class GraphifyDemo extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Graphify(
      options: {
        'title': {
          'text': '我的第一張圖表',
        },
        'tooltip': {},
        'xAxis': {
          'data': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        },
        'yAxis': {},
        'series': [
          {
            'name': '銷售量',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20, 5],
          },
        ],
      },
      width: MediaQuery.of(context).size.width,
      height: 400,
    );
  }
}
```

### 3D 圖表範例

```dart
Graphify(
  options: {
    'title': {
      'text': '3D 長條圖',
    },
    'xAxis3D': {
      'type': 'category',
      'data': ['A', 'B', 'C'],
    },
    'yAxis3D': {
      'type': 'category',
      'data': ['X', 'Y', 'Z'],
    },
    'zAxis3D': {
      'type': 'value',
    },
    'grid3D': {},
    'series': [
      {
        'type': 'bar3D',
        'data': [
          [0, 0, 5],
          [1, 0, 20],
          [2, 0, 36],
        ],
      },
    ],
  },
  width: 600,
  height: 400,
)
```

### 蠟燭圖範例

```dart
Graphify(
  options: {
    'title': {
      'text': '股票蠟燭圖',
    },
    'tooltip': {
      'trigger': 'axis',
    },
    'xAxis': {
      'data': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05'],
    },
    'yAxis': {
      'scale': true,
    },
    'series': [
      {
        'type': 'candlestick',
        'data': [
          [11, 12.5, 10, 13.2],  // [open, close, low, high]
          [12.5, 11.8, 11, 13],
          // ... 更多數據
        ],
      },
    ],
  },
)
```

## 參數與設定

### 必要參數

| 參數 | 類型 | 說明 |
|------|------|------|
| `options` | `Map<String, dynamic>` | Apache ECharts 配置物件 |
| `width` | `double` | 圖表寬度 |
| `height` | `double` | 圖表高度 |

### 選擇性參數

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `onChartReady` | `Function` | null | 圖表就緒回調 |
| `onChartEvent` | `Function` | null | 圖表事件回調 |
| `loading` | `bool` | false | 顯示載入動畫 |
| `theme` | `String` | 'light' | 主題 (light/dark) |

### 事件回調

```dart
Graphify(
  options: chartOptions,
  width: 600,
  height: 400,
  onChartReady: (controller) {
    print('圖表已就緒');
    // 可在此執行圖表控制邏輯
  },
  onChartEvent: (event) {
    print('圖表事件: ${event['type']}');
    // 處理圖表事件
  },
)
```

## 進階功能

### 圖表控制器

透過 `onChartReady` 回調取得控制器，執行進階操作：

```dart
class GraphifyController {
  Future<void> setOption(Map<String, dynamic> option) async
  Future<void> showLoading() async
  Future<void> hideLoading() async
  Future<void> dispatchAction(Map<String, dynamic> action) async
  Future<void> convertToPixel(Map<String, dynamic> query) async
  Future<void> getDataZoomState() async
  Future<void> makeBase64Image({String? format}) async
}
```

### 資料更新

```dart
final controller = GraphifyController.fromContext(context);

// 更新圖表數據
await controller.setOption({
  'series': [{
    'data': newChartData,
  }],
});
```

### 匯出圖片

```dart
final base64Image = await controller.makeBase64Image(
  format: 'png',  // png 或 jpeg
);
```

## 性能優化

### 大數據處理

- 支援資料分頁載入
- 建議使用 `visualMap` 進行數據篩選
- 啟用數據聚合（aggregate）功能

### 記憶體優化

- 圖表銷毀時自動釋放資源
- 支援 `dispose()` 方法手動清理

### 渲染優化

- 啟用 `animation: false` 提升效能
- 使用 `large` 模式處理大量數據點
- 調整 `renderThrottle` 參數

## 常見問題

### Q: Graphify 與原生 ECharts 的差異？

Graphify 是 Flutter 的橋接層，底層仍使用 Apache ECharts 的完整功能，但透過 Flutter widget 實作，支援 Flutter 的事件處理與狀態管理。

### Q: 是否支援所有 ECharts 圖表類型？

是的，Graphify 完整支援 Apache ECharts 的所有圖表類型，包括 2D、3D、WebGL 等。

### Q: 跨平台相容性如何？

Graphify 支援 Web、Android、iOS、Windows、Linux、macOS 等六大平台，使用 `dart:ffi` 實現 Windows 原生整合。

### Q: 如何處理圖表事件？

使用 `onChartEvent` 回調接收事件，支援點擊、hover、zoom 等互動事件。

### Q: 版本遷移注意事項？

v1.0.0 開始使用新的 `dart:ffi` 方案，需更新依賴：
- `graph_webkit_dep` (Windows)
- `graph_webkit_web_dep` (Web)

## 專案結構

```
graphify/
├── android/              # Android 平台程式碼
├── ios/                  # iOS 平台程式碼
├── lib/                  # 主要 Flutter 程式碼
│   ├── src/
│   │   ├── graphify.dart
│   │   ├── graphify_controller.dart
│   │   └── ...
│   └── graphify.dart     # 匯出檔案
├── linux/                # Linux 平台程式碼
├── macos/                # macOS 平台程式碼
├── windows/              # Windows 平台程式碼
├── web/                  # Web 平台程式碼
├── example/              # 範例應用程式
├── test/                 # 測試檔案
├── pubspec.yaml          # 套件描述
└── README.md             # 說明文件
```

## 開發團隊與貢獻

- **主要開發者**：warioddly
- **授權**：MIT License
- **貢獻指南**：參見 [CONTRIBUTING.md](https://github.com/warioddly/graphify/blob/main/CONTRIBUTING.md)

### 貢獻方式

1. Fork 專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 相關資源

- **GitHub 倉庫**：[https://github.com/warioddly/graphify](https://github.com/warioddly/graphify)
- **Pub.dev**：[https://pub.dev/packages/graphify](https://pub.dev/packages/graphify)
- **Apache ECharts**：[https://echarts.apache.org/](https://echarts.apache.org/)
- **Flutter**：[https://flutter.dev/](https://flutter.dev/)

## 範例應用程式

Graphify 提供完整的範例應用程式，包含：
- 各種圖表類型的展示
- 互動功能示範
- 響應式佈局範例
- 進階配置說明

查看 [example](https://github.com/warioddly/graphify/tree/main/example) 目錄獲取完整範例。

## 版本歷史

### v1.2.0
- 更新 CHANGELOG
- 修復部分平台相容性問題

### v1.1.0
- 增強事件處理機制
- 優化記憶體使用

### v1.0.0
- **重大更新**：使用 `dart:ffi` 替代 `dart:ui_webview`
- 新增 Windows 原生整合
- 使用 `package:web` 進行 Web 平台整合

### v0.x.x
- 初始版本
- 基本圖表功能

## 總結

Graphify 是 Flutter 開發者進行資料視覺化的理想選擇，提供：

✅ **完整的 ECharts 功能支援**  
✅ **跨平台相容性**（Web、Android、iOS、Windows、Linux、macOS）  
✅ **現代化技術架構**（`dart:ffi` + `package:web`）  
✅ **豐富的互動功能**  
✅ **良好的 Flutter 整合**  
✅ **MIT 開源授權**

無論你是開發數據儀表板、金融分析工具，還是任何需要圖表視覺化的應用，Graphify 都是值得考慮的解決方案。

---

**專案狀態**：此專案已於 2026-05-09 封存（Archive），但仍可作為學習與參考使用。

**最後更新**：2024-07-29  
**作者**：[Hermes Agent](https://hermes-agent.nousresearch.com/) 整理