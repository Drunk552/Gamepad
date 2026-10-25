# S3 Gamepad · ESP32-S3 USB HID 双摇杆手柄

目标：ESP32-S3 USB HID 双摇杆手柄，优先适配 PC《双影奇域》（Split Fiction）。
本仓库当前是**工程约束、任务拆解和验收文档 + 多 Agent 协作配置**，固件代码在 M0 批准后创建（届时新增 `main/`、`components/`、`tests/`）。

## 目录结构

```
├── AGENTS.md                      # AI 开发约束（V1.0 基线 + V1.1 多 Agent 附加条款）
├── README.md
├── docs/                          # 文档地图见 docs/README.md
│   ├── product/                   #   需求基线 requirements.md + PRD 母本 docx
│   ├── hardware/                  #   硬件待确认问题 + 引脚确认表 board-pinmap.md
│   ├── firmware/                  #   架构 architecture.md + 接口契约 interface-contract.md
│   ├── process/                   #   里程碑 plan.md + 协作协议 + 测试矩阵
│   ├── prompts/                   #   AI 启动提示词存档
│   ├── tasks/                     #   任务文件（工作产物，从 _TEMPLATE.md 生成）
│   ├── decisions/                 #   ADR 决策记录
│   └── test-evidence/             #   实测证据归档
├── tools/validate_pinmap.py       # ESP32-S3 引脚安全静态验证
├── .zcode/                        # ZCode：agents/（3 角色）+ skills/（4 工作流）
├── .codex/                        # Codex 同名角色配置（与 .zcode 语义一致）
└── _archive/                      # 原始启动包/补充包存档（git 忽略）
```

## 多 Agent 协作

| 角色 | ZCode subagent | 职责 |
|---|---|---|
| 主 Agent | 主会话 | 接口冻结、集成、合并、里程碑门控（唯一集成者） |
| USB 工程师 | `usb-engineer` | `components/usb_gamepad/**` |
| 输入工程师 | `input-engineer` | `components/input_analog/**`、`input_buttons/**`、`calibration/**` |
| QA 审查员 | `qa-reviewer` | 只读审查；授权后写 `tests/**` |

工作流 skill：`s3-dispatch`（任务派发）、`s3-build`（构建与门禁）、`s3-pinmap`（引脚验证）、`s3-evidence`（证据记录）。细则见 `docs/process/multi-agent-protocol.md`。

## 立即开始

1. **新开 ZCode 会话**：投喂 `docs/prompts/zcode-kickoff.txt`（主 Agent 会先交五项规划，不会直接写代码）。
2. **回答 `docs/hardware/hardware-questions.md`**：开发板型号、USB-OTG 口、摇杆/扳机元件等（M0-01，一切编码的前置）。
3. 提供 pinout 后用 `s3-pinmap` 技能填 `docs/hardware/board-pinmap.md` 并冻结引脚。
4. 主 Agent 产出接口契约终稿（`docs/firmware/interface-contract.md`）交用户批准。
5. 用户发出"批准 M0 实施"后，用 `s3-dispatch` 按 `docs/process/plan.md` 逐任务派发。
6. 实测证据随时用 `s3-evidence` 记录；M0 GO/NO-GO 由游戏实测决定，通过后才进入 M1/PCB。

## 红线（详见 AGENTS.md）

- USB HID ≠ XInput；禁止伪装微软 VID/PID；开发期用 esp_tinyusb 示例测试标识。
- GPIO19/20 专用 USB；引脚必须过 `validate_pinmap.py` + 原理图核对，未确认标 `TODO_BOARD_VALIDATION`。
- 所有实机测试默认 `NOT_RUN`，只能凭证据翻转；编译通过 ≠ 实机通过。

## 官方参考

- ESP-IDF USB Device Stack: https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32s3/api-reference/peripherals/usb_device.html
- ESP-IDF TinyUSB HID 示例: https://github.com/espressif/esp-idf/tree/master/examples/peripherals/usb/device/tusb_hid
- Steam Input 支持的设备: https://partner.steamgames.com/doc/features/steam_controller/device
- 《双影奇域》好友通行证: https://www.ea.com/zh-hans/games/split-fiction/split-fiction/features/friends-pass-pc
