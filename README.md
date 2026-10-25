# S3 Gamepad · ESP32-S3 USB HID 双摇杆手柄

目标：ESP32-S3 USB HID 双摇杆手柄，优先适配 PC《双影奇境》（Split Fiction）。
本仓库当前是**工程约束、任务拆解和验收文档 + 多 Agent 协作配置**，固件代码在 M0 批准后创建。

## 目录结构

```
├── AGENTS.md                  # AI 开发约束（V1.0 基线 + V1.1 多 Agent 附加条款）
├── docs/
│   ├── requirements.md        # P0 需求（FR/NFR）
│   ├── architecture.md        # 架构与接口契约
│   ├── plan.md                # 里程碑看板 M0~M6
│   ├── board-pinmap-template.md  # 引脚确认表（用 tools/validate_pinmap.py 验证）
│   ├── interface-contract.md  # 接口契约冻结文档（当前 DRAFT v0.1）
│   ├── hardware-questions.md  # 必须由用户确认的硬件事实清单
│   ├── multi-agent-protocol.md# 多 Agent 协作协议（派发/汇报/门禁/合并）
│   ├── test-matrix.md         # 测试矩阵（证据驱动，默认 NOT_RUN）
│   ├── tasks/                 # 任务文件（从 _TEMPLATE.md 生成）
│   ├── decisions/             # ADR 决策记录
│   └── test-evidence/         # 实测证据归档
├── prompts/                   # codex-m0.txt / multiagent-kickoff.txt
├── tools/validate_pinmap.py   # ESP32-S3 引脚安全静态验证
├── .zcode/                    # ZCode 配置：agents/（3 角色）+ skills/（4 工作流）
├── .codex/                    # Codex 配置（同名角色，与 .zcode 语义一致）
└── ESP32-S3_游戏手柄_项目规划与开发需求_V1.0(1).docx  # 完整版需求母本
```

> 原始的 V1.0 启动包与 V1.1 多 Agent 补充包目录仅作存档（已被 git 忽略），内容已并入根目录。

## 多 Agent 协作

| 角色 | ZCode subagent | 职责 |
|---|---|---|
| 主 Agent | 主会话 | 接口冻结、集成、合并、里程碑门控（唯一集成者） |
| USB 工程师 | `usb-engineer` | `components/usb_gamepad/**` |
| 输入工程师 | `input-engineer` | `components/input_analog/**`、`input_buttons/**`、`calibration/**` |
| QA 审查员 | `qa-reviewer` | 只读审查；授权后写 `tests/**` |

工作流 skill：`s3-dispatch`（任务派发）、`s3-build`（构建与门禁）、`s3-pinmap`（引脚验证）、`s3-evidence`（证据记录）。细则见 `docs/multi-agent-protocol.md`。

## 立即开始

1. **回答 `docs/hardware-questions.md`**：开发板型号、USB-OTG 口、摇杆/扳机元件等（M0-01，一切编码的前置）。
2. 提供 pinout 后用 `s3-pinmap` 技能填 `docs/board-pinmap-template.md` 并冻结引脚。
3. 主 Agent 产出接口契约终稿（`docs/interface-contract.md`）交用户批准。
4. 用户发出"批准 M0 实施"后，用 `s3-dispatch` 按 `docs/plan.md` 逐任务派发。
5. 实测证据随时用 `s3-evidence` 记录；M0 GO/NO-GO 由游戏实测决定，通过后才进入 M1/PCB。

## 红线（详见 AGENTS.md）

- USB HID ≠ XInput；禁止伪装微软 VID/PID；开发期用 esp_tinyusb 示例测试标识。
- GPIO19/20 专用 USB；引脚必须过 `validate_pinmap.py` + 原理图核对，未确认标 `TODO_BOARD_VALIDATION`。
- 所有实机测试默认 `NOT_RUN`，只能凭证据翻转；编译通过 ≠ 实机通过。

## 官方参考

- ESP-IDF USB Device Stack: https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32s3/api-reference/peripherals/usb_device.html
- ESP-IDF TinyUSB HID 示例: https://github.com/espressif/esp-idf/tree/master/examples/peripherals/usb/device/tusb_hid
- Steam Input 支持的设备: https://partner.steamgames.com/doc/features/steam_controller/device
- 《双影奇域》好友通行证: https://www.ea.com/zh-hans/games/split-fiction/split-fiction/features/friends-pass-pc
