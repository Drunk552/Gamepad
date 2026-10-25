# 开发板引脚确认表（候选 → 最终，逐步冻结）

> 未确认原理图前 **禁止** 把候选 GPIO 写死为最终 GPIO。ESP32-S3 的具体开发板可能复用 USB、Flash/PSRAM、UART、LED、Strapping 等引脚。
> 本表每次修改后必须跑 `python tools/validate_pinmap.py docs/hardware/board-pinmap.md`（S3 通用规则静态检查，替代不了原理图核对）。
> 已知问题：候选 RX=GPIO3 是 strapping 引脚（JTAG 源选择），若沿用需评估摇杆电路的上电电平，建议改用 GPIO7/GPIO10。

- 开发板厂商/型号：国产 DevKitC-1 兼容板（厂商丝印不可读，板名丝印仅 "ESP32-S3"）；排针丝印与 Espressif ESP32-S3-DevKitC-1 布局一致。来源：实物照片 `docs/hardware/photos/`（用户 2026-10-25 提供）
- ESP32-S3 模组型号 / Flash / PSRAM：屏蔽罩丝印 "S3-N16R8"（16MB Flash / 8MB PSRAM）。R8 为 Octal PSRAM → **GPIO33-37 模组内部占用，虽引出排针亦不可用**
- 官方原理图或 Pinout 来源：无原理图；以排针丝印照片 + ESP32-S3 技术规格书为准
- USB 数据端口：两个 USB-C。丝印 **"USB"**（旁有 **USB-OTG** 丝印）= 原生 USB-OTG，D−=GPIO19，D+=GPIO20；丝印 **"COM"** = USB-UART 桥接口（桥接芯片丝印不可读），用于下载/日志
- UART 调试口：COM 口（经桥接芯片走 UART0，芯片侧 GPIO43/44）。USB HID 占用 OTG 口时日志走 COM 口，两者物理独立，满足 AGENTS 约束（首次枚举实测最终确认）
- 摇杆元件：采购中（用户 2026-10-25 确认：1 个 XY 双电位器摇杆模块 + 3 个轻触按键 A/B/Start）
- 板载 RGB LED：丝印 "RGB"，控制引脚未读出（DevKitC-1 布局常见 GPIO48，**未核实，本项目不使用**）
- 板载按键：RST + BOOT（BOOT=GPIO0，strapping，已被板占用）
- GPIO 候选：ADC1 GPIO1..7（RX 由 GPIO3 改为 GPIO7，见下）；I2C GPIO8/9；MCP INT GPIO13；外部 LED GPIO12
- GPIO0 / 45 / 46 等启动限制：GPIO0=BOOT 键占用；GPIO45/46 strapping 不用；GPIO35/36/37 Octal PSRAM 占用不可用
- 脚位实际可用性与冲突：排针引出确认可用 GPIO1-21、38-48（照片丝印）；GPIO19/20 引出但被 OTG 占用
- 批准日期/审核人：2026-10-25 / 主 Agent（候选级确认；"最终脚位"列待电气实测后冻结）

| 功能 | 候选脚位 | 最终脚位 | 证明 / 原理图页 | 状态 |
|---|---|---|---|---|
| LX | GPIO1 | TBD | 排针丝印照片（引出确认）+ 技术规格书（ADC1_CH0） | NOT_VERIFIED |
| LY | GPIO2 | TBD | 同上（ADC1_CH1） | NOT_VERIFIED |
| RX | GPIO7 | TBD | 同上（ADC1_CH6）；原候选 GPIO3 因 strapping 弃用 | NOT_VERIFIED |
| RY | GPIO4 | TBD | 同上（ADC1_CH3） | NOT_VERIFIED |
| LT | GPIO5 | TBD | 同上（ADC1_CH4） | NOT_VERIFIED |
| RT | GPIO6 | TBD | 同上（ADC1_CH5） | NOT_VERIFIED |
| I2C_SDA | GPIO8 | TBD | 排针丝印照片（引出确认） | NOT_VERIFIED |
| I2C_SCL | GPIO9 | TBD | 同上 | NOT_VERIFIED |
| USB_D− | GPIO19 | GPIO19 | 技术规格书（USB D− 专用）+ 板丝印 "USB-OTG"（2026-10-25 照片）；电气连通待 T-USB-01 实测 | NOT_VERIFIED |
| USB_D+ | GPIO20 | GPIO20 | 同上（USB D+ 专用） | NOT_VERIFIED |
