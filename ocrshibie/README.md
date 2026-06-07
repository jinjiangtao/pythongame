# OCR 图片文字识别工具

一个功能丰富的图片文字识别桌面应用程序。

## 功能特性

- **多种识别方式**: 截图识别、本地图片识别、批量识别
- **图片预处理**: 灰度化、二值化、去噪、自动旋转、亮度/对比度调节
- **语言支持**: 中文、英文、中英文混合
- **历史记录**: 保存识别历史，可随时查看
- **导出功能**: 支持导出为 TXT 或 DOCX 格式
- **自动复制**: 识别完成后自动复制到剪贴板

## 环境要求

1. Python 3.8+
2. Tesseract OCR 引擎

### 安装 Tesseract

**Windows**:
- 下载地址: https://github.com/UB-Mannheim/tesseract/wiki
- 安装时确保勾选中文语言包（chi_sim）
- 默认安装路径: `C:\Program Files\Tesseract-OCR`

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python main.py
```

## 文件结构

```
ocrshibie/
├── main.py              # 程序入口
├── app.py               # 主窗口界面
├── screenshot.py        # 截图功能
├── ocr_engine.py        # OCR识别引擎
├── image_processor.py   # 图片预处理
├── batch_processor.py   # 批量识别处理
├── history_manager.py   # 历史记录管理
├── settings.py          # 配置常量
├── utils.py             # 辅助函数
├── requirements.txt     # 依赖列表
└── README.md            # 说明文档
```

## 使用说明

1. **截图识别**: 点击"截图识别"按钮，选择区域后自动识别
2. **打开图片**: 点击"打开图片"选择本地图片进行识别
3. **批量识别**: 选择文件夹，自动识别所有图片并保存为 TXT
4. **预处理**: 在"预处理"标签页中可以对图片进行各种处理以提高识别率
5. **历史记录**: 在"历史"标签页查看以前的识别记录

## 打包成 EXE

可以使用 PyInstaller 打包成单个可执行文件:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "OCR工具" main.py
```

打包时需要确保 Tesseract 也随程序一起分发，或者要求用户自行安装。
