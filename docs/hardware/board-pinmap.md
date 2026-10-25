# 开发板引脚确认表（候选 → 最终，逐步冻结）

> 未确认原理图前 **禁止** 把候选 GPIO 写死为最终 GPIO。ESP32-S3 的具体开发板可能复用 USB、Flash/PSRAM、UART、LED、Strapping 等引脚。
> 本表每次修改后必须跑 `python tools/validate_pinmap.py docs/hardware/board-pinmap.md`（S3 通用规则静态检查，替代不了原理图核对）。
> 已知问题：候选 RX=GPIO3 是 strapping 引脚（JTAG 源选择），若沿用需评估摇杆电路的上电电平，建议改用 GPIO7/GPIO10。

- 开发板厂商/型号：TODO
- ESP32-S3 模组型号 / Flash / PSRAM：TODO
- 官方原理图或 Pinout 来源：TODO
- USB 数据端口：TODO（确认 D−=GPIO19，D+=GPIO20；USB 走原生 OTG）
- UART 调试口：TODO
- GPIO 候选：ADC1 GPIO1..6；I2C GPIO8/9；MCP INT GPIO13；LED GPIO12。
- GPIO0 / 45 / 46 等启动限制：TODO
- 脚位实际可用性与冲突：TODO
- 批准日期/审核人：TODO

| 功能 | 候选脚位 | 最终脚位 | 证明 / 原理图页 | 状态 |
|---|---|---|---|---|
| LX | GPIO1 | TBD | TBD | NOT_VERIFIED |
| LY | GPIO2 | TBD | TBD | NOT_VERIFIED |
| RX | GPIO3 | TBD | TBD | NOT_VERIFIED |
| RY | GPIO4 | TBD | TBD | NOT_VERIFIED |
| LT | GPIO5 | TBD | TBD | NOT_VERIFIED |
| RT | GPIO6 | TBD | TBD | NOT_VERIFIED |
| I2C_SDA | GPIO8 | TBD | TBD | NOT_VERIFIED |
| I2C_SCL | GPIO9 | TBD | TBD | NOT_VERIFIED |
| USB_D− | GPIO19 | GPIO19 | TBD | NOT_VERIFIED |
| USB_D+ | GPIO20 | GPIO20 | TBD | NOT_VERIFIED |
