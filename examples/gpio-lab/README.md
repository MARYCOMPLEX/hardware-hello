# GPIO 与任务调度实验

目标 ESP-IDF 5.5.x，ESP32-S3 开发板。默认只输出每秒递增日志，不驱动引脚。

```sh
. ~/esp/esp-idf/export.sh
idf.py set-target esp32s3
idf.py build
idf.py -p PORT flash monitor
```

`PORT` 替换为真实串口。成功时每秒看到 `hello: tick=0`、`tick=1` 等。

实验 LED：断电后，将已核实空闲的输出 GPIO → 470 Ω 电阻 → LED 阳极；LED 阴极 → GND。运行 `idf.py menuconfig`，进入 `Hardware Hello lab`，启用 LED 并填写已核实引脚，重新编译烧录。LED 每秒切换一次状态，完整周期约 2 秒。引脚默认值 2 仅是配置初值，不表示原项目板上的 GPIO2 可用；避开 Flash、PSRAM、USB、启动配置及已占用引脚。

普通 LED 与可寻址 RGB LED 的协议不同；这个实验不驱动 WS2812。软件检查只验证芯片支持输出，电路是否允许由你核对。更换目标芯片时先重新核对板级引脚。当前未在实物上验收，烧录时记录板卡型号、IDF 版本和日志。
