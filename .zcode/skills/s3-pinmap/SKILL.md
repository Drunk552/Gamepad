---
name: s3-pinmap
description: "验证 S3 Gamepad 的 GPIO 引脚分配安全性并推进引脚冻结流程。当用户要填/改 board-pinmap 引脚表、讨论某个 GPIO 能不能用、提供了开发板型号或原理图、或任务涉及引脚分配时使用。核心原则：引脚安全靠脚本验证不靠记忆断言，开发板事实未确认前禁止把候选引脚写成最终引脚。"
---

# S3 Gamepad 引脚验证与冻结流程

## 1. 前提：开发板事实

引脚表冻结的前提是 `docs/hardware-questions.md` 第 1–3 项已确认：开发板准确型号、模组（N8/N16、PSRAM 容量）、官方原理图或 pinout 来源、USB-C 是原生 OTG 口还是 UART 下载口。

用户没提供时：向用户索要（型号/购买链接/原理图都行），**绝不能猜**。可以先用官方开发板资料做"预填分析"，但状态列必须保持 NOT_VERIFIED。

## 2. 运行验证脚本

```bash
python tools/validate_pinmap.py docs/board-pinmap-template.md
```

脚本覆盖的 ESP32-S3 规则（退出码 0=通过，1=ERROR，2=仅 WARN）：

| 规则 | 引脚 | 后果 |
|---|---|---|
| USB D−/D+ 专用 | 19 / 20 | 挪作他用设备无法枚举 |
| strapping | 0 / 3 / 45 / 46 | 上电电平被外电路影响 → 启动行为异常 |
| SPI flash 占用 | 26–32 | 模组内部已接，外接会冲突 |
| Octal PSRAM 占用 | 33–37 | N8R8 等模组不可用，需确认模组型号 |
| UART0 默认脚 | 43 / 44 | 项目计划独立 UART 日志，占用需确认 |
| ADC1 / ADC2 | 1–10 / 11–20 | 模拟输入必须在 ADC 脚；ADC2 与 WiFi 冲突，优先 ADC1 |
| 不存在的引脚 | 22–25 | S3 芯片无这些 GPIO |
| 重复分配 | 任意 | 两功能占同一脚 |

**已知问题**：候选表把 RX（右摇杆 X）放在 GPIO3 —— strapping 引脚。不是绝对不能用，但要评估摇杆电路在复位瞬间的电平；稳妥做法是换到 GPIO7/10 等空闲 ADC1 脚。

## 3. 解读与修复

- 每个 ERROR 必须解决（换引脚或改方案）后才能进入下一步。
- WARN 要么消除、要么在表格"证明/原理图页"列写明评估依据。
- 脚本只覆盖 S3 通用规则；**具体开发板的复用**（板载 LED、外设、USB-JTAG 跳线等）仍需对照该板原理图人工核对。

## 4. 填写与冻结

1. 把确认后的引脚写入"最终脚位"列，"证明 / 原理图页"列填来源（链接/页码），状态列 NOT_VERIFIED → VERIFIED。
2. 全部 VERIFIED 后：由主 Agent 复核，在 `docs/decisions/` 记 ADR（板卡型号 + 引脚冻结版本），此后 `board_pinmap.h` 才能去掉对应的 `TODO_BOARD_VALIDATION`。
3. 换板卡 = 重新走整个流程。

## 禁止

- 没有原理图来源就把状态改成 VERIFIED。
- 把候选脚位直接当最终脚位使用。
- 在实时代码里散落 GPIO 数字——引脚只允许出现在 `board_bsp` 中。
