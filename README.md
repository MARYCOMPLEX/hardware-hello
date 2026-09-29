# Hardware Hello

面向软件工程师与硬件初学者的 ESP32 多功能调试器中文教材，共 24 章。

**[在线阅读完整教材](https://marycomplex.github.io/hardware-hello/)**

从电压、电流、元件和 C 语言开始，逐步学习 ESP-IDF、总线时序、协议、显示、调试、原理图、供电、PCB、传感器误差和综合实验。包含计算示例、接线方法、故障定位与带答案的自测。原项目源码事实与教学示例分别标注；尚未核验完整原板 EDA/BOM，不把推测写成板级事实。

## 阅读与实验

- `book.md`：完整书稿，也是站点唯一内容来源。
- `examples/gpio-lab/`：完整 ESP-IDF GPIO 入门工程，默认只打印日志。
- `examples/protocol_lab.py`：无硬件、无依赖的流式协议实验及自动测试。
- `docs/source-map.md`：原项目对应关系与核查边界。

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python examples/protocol_lab.py
python build_book.py
python -m http.server 4173
```

浏览器访问 `http://localhost:4173`。章节与小节都有独立锚点，侧边目录可展开小节。推送 main 后 GitHub Actions 自动测试协议示例、重建教材并部署 Pages。

GPIO 实验需要 ESP-IDF 5.5.x 和对应开发板；操作步骤见其 README。软件协议实验已测试，GPIO/原板电路未做实物验收。

## 来源

- [原固件](https://github.com/MARYCOMPLEX/Multi-Function-ESP32-Debugger)
- [硬件作者主页](https://oshwhub.com/djsdjsdjs5)

仓库仅存放本书、相关学习代码和站点构建文件。
