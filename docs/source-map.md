# 来源与实践映射

| 本书实践 | 原项目目录/页面 | 学到什么 |
|---|---|---|
| C6 主机 | `C6_Screen` | ESP32-C6、LVGL、LinkIt Host、ESP-NOW |
| 逻辑分析仪 | `S3_LogicAnalyser` | SPI 采集、UART/I²C 监听、SWD 接收 |
| CMSIS-DAP | `S3_otg_cmsisdap` | USB OTG、CherryUSB、无线 DAP |
| 热成像 | `S3_Thermal` | MLX90640、I²C、帧协议 |
| 环境传感器 | `S3_Environment_Sensor` | I²C 传感器、数据聚合 |
| 陀螺仪 | `C3_Gyro` | ESP32-C3、SPI 传感器 |

## 核查边界

本书核查的原固件提交为 `e086e5e3c0039c5dcce43b96778e52a4c3b8ccd7`。GPIO 表表示该源码的配置，实物连线仍须匹配 PCB 版本。

硬件作者主页展示五个项目：ESP 加 PICO 简易开发版、环境传感器模块、屏幕模块、简易热成像模块、简易陀螺仪模块。已获取的网页资料不足以核验完整 EDA 工程、BOM、Gerber 和 RP2040 采样固件；不能据网页附件栏为空就断言 EDA 编辑器内不存在资料。

第 16—24 章中的示范电路、预算与 HH1 协议是教学设计，不能直接当作原板生产文件。书中明确区分源码事实、教学假设与待实测结论。
