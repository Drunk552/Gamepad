# ADR-0001 项目基线决策

日期：2026-10-25 · 状态：ACCEPTED · 发起：主 Agent（依据 V1.0 需求文档与 V1.1 多 Agent 附加包）

## 背景
项目启动时需要把分散在启动包/补充包/需求 docx 中的关键决策固化为可引用的基线，供多 Agent 协作与后续变更追溯。

## 决策

1. **适配路径**：优先路径 A（ESP32-S3 → 原生 USB HID Gamepad → Steam Input →《双影奇境》）；路径 B（PC 端桥接虚拟 XInput）仅在 A 实测不满足时立项评估。禁止伪装微软 VID/PID。
2. **多 Agent 结构**：主 Agent 唯一集成者 + 三个子 Agent（usb-engineer / input-engineer / qa-reviewer），并发上限 3，文件所有权按 `AGENTS.md` 附加条款；执行细则见 `docs/process/multi-agent-protocol.md`。ZCode 定义在 `.zcode/agents/`，Codex 定义在 `.codex/agents/`，二者同步维护。
3. **Host 单测框架**：CTest（纯 CMake）。逻辑模块（校准/死区/消抖/映射/序列化）与硬件访问分离，保证 PC 可跑。
4. **引脚安全**：所有引脚分配必须通过 `tools/validate_pinmap.py` 静态校验 + 板卡原理图人工核对，双重确认后才可去掉 `TODO_BOARD_VALIDATION` 标记。
5. **开发期 VID/PID**：沿用 esp_tinyusb 官方示例自带的测试标识；量产（或对外发布固件）前必须替换为授权 VID，违反即阻断合并。
6. **工程根目录**：`D:\work\Gamepad`（纯 ASCII 路径，避免 ESP-IDF Windows 工具链对非 ASCII 路径的兼容问题）。原启动包/补充包目录仅作参考存档，不参与构建。

## 影响
- 子 Agent 在接口契约（`docs/firmware/interface-contract.md`）冻结前不得并行实现 USB 与输入模块。
- ESP-IDF / esp_tinyusb 版本锁定后（首次编译通过时）将新增一条 ADR 记录具体版本号。

## 待定项（不阻塞本 ADR）
- 代码许可证（MIT / Apache-2.0 / 私有）—— 由用户决定。
- ESP-IDF 具体版本号 —— 等本机安装并首次编译通过后锁定。
