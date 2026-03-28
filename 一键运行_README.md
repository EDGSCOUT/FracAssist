# 🚀 股骨颈骨折辅助诊断系统 - 一键运行

## 📌 快速开始

### 方法1：Web版本（推荐）

```bash
# 1. 克隆项目
git clone git@github.com:EDGSCOUT/FracAssist.git
cd FracAssist

# 2. 安装依赖
pip install -r requirements.txt

# 3. 一键启动
python app.py
```

### 方法2：桌面版本

```bash
# 1. 克隆项目
git clone git@github.com:EDGSCOUT/FracAssist.git
cd FracAssist

# 2. 安装依赖
pip install -r requirements.txt

# 3. 一键启动
python fracture_assistant.py
```

## 🌐 访问地址

启动后访问：
- **Web版本**: http://localhost:8080
- **桌面版本**: 自动打开GUI窗口

## 📋 使用步骤

### Web版本

1. **打开浏览器** → 访问 http://localhost:8080
2. **上传图像** → 拖拽或选择医学影像文件
3. **标注关键点** → 在图像上点击标注：
   - 第1点：骨折近端点（红色）
   - 第2点：骨折远端点（蓝色）
4. **点击【计算分析】** → 系统自动计算并显示：
   - 骨折线角度
   - 三枚螺钉位置（彩色显示）
   - 螺钉规格（长度、直径）
   - Pauwels分型
   - 详细临床建议
5. **保存报告** → 导出分析报告

### 桌面版本

1. **启动程序** → 运行 `python fracture_assistant.py`
2. **打开图像** → 点击【打开图像】按钮
3. **标注关键点** → 在图像上点击两个点
4. **计算分析** → 点击【计算分析】按钮
5. **查看结果** → 右侧显示分析结果
6. **保存图像** → 点击【保存结果图像】

## 📦 系统要求

- Python 3.7+
- 依赖包（自动安装）：
  - Flask
  - NumPy
  - OpenCV
  - Pillow
  - Werkzeug

## 🎯 功能特性

### ✨ 核心功能
- ✅ 医学影像导入（支持多种格式）
- ✅ 交互式关键点标注
- ✅ 精确角度计算
- ✅ **三枚螺钉自动定位**
- ✅ **螺钉规格智能计算**
- ✅ Pauwels分型评估
- ✅ 详细临床建议

### 🔬 专业算法
- Pauwels分型系统（I/II/III型）
- 螺钉长度：70-100mm（动态计算）
- 螺钉直径：6.5mm或7.3mm
- 进针角度：基于骨折线自动计算
- 三枚螺钉：主钉、辅助钉、支撑钉

### 🏥 临床建议
- 骨折类型评估
- 固定方案建议
- 手术技术要点
- 术后注意事项
- 并发症预防

## 📊 输出结果

### 分析结果包含：

1. **基本信息**
   - 骨折线角度
   - 骨折线斜率
   - 两点距离

2. **螺钉配置**
   - 螺钉1（红色）：长度、直径、角度
   - 螺钉2（蓝色）：长度、直径、角度
   - 螺钉3（绿色）：长度、直径、角度

3. **临床建议**
   - Pauwels分型
   - 固定方案
   - 手术技术要点
   - 术后康复计划

## ⚠️ 注意事项

### 医学免责声明
- ⚠️ 本系统仅供辅助诊断参考
- ⚠️ 实际手术方案需专业医生制定
- ⚠️ 建议结合三维影像评估
- ⚠️ 建议结合健侧对比

### 使用限制
- 仅支持二维图像分析
- 需要人工标注关键点
- 不适用于复杂粉碎性骨折

## 🔧 常见问题

### Q: 如何停止Web服务器？
```bash
# 在终端按 Ctrl+C
# 或使用命令
pkill -f "python app.py"
```

### Q: 端口被占用怎么办？
编辑 `app.py` 文件，修改最后一行的端口号：
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # 改为其他端口
```

### Q: 支持哪些图像格式？
- JPG/JPEG
- PNG
- TIFF/TIF
- BMP
- GIF

### Q: 图像大小有限制吗？
- 最大支持：16MB
- 建议分辨率：800x600 或更高

## 📚 更多文档

- **更新说明_v2.md** - v2.0版本详细更新
- **README.md** - 完整技术文档
- **使用指南.md** - 详细使用说明
- **项目总结.md** - 项目总结

## 🌟 项目信息

- **项目名称**: FracAssist (Femoral Neck Fracture Analysis System)
- **版本**: v2.0
- **GitHub**: https://github.com/EDGSCOUT/FracAssist
- **分支**: initial_success

## 💡 快速测试

使用示例图像测试：
```bash
# 示例图像已包含在项目中
# 直接在Web界面上传 demo.jpg 或使用自己的医学影像
```

## 🎉 开始使用

```bash
# 3步启动，立即使用！
git clone git@github.com:EDGSCOUT/FracAssist.git && cd FracAssist
pip install -r requirements.txt
python app.py
```

然后打开浏览器访问：**http://localhost:8080**

---

**现在就开始使用吧！** 🚀