# 帧解析练习

原项目 LinkIt 的实际帧结构以对应源码为准，不假设所有帧都有序号或 CRC。

本书第 6 章使用独立的 HH1 教学协议，完整实现见 `protocol_lab.py`，运行：

```sh
python3 examples/protocol_lab.py
```

学习顺序：观察半帧与粘包 → 验证长度边界 → 注入错误 CRC → 验证坏帧后恢复 → 为真实串口集成增加超时。切勿直接将 HH1 帧发给原 LinkIt 设备并期待兼容。
