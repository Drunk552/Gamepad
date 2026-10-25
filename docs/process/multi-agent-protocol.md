# 多 Agent 协作协议（S3 Gamepad）

本文件是 `AGENTS.md` 多 Agent 条款的执行细则：任务怎么派发、怎么汇报、怎么合并、怎么算完成。主 Agent（当前会话）与所有子 Agent 都必须遵守。角色定义文件：`.zcode/agents/`（ZCode）、`.codex/agents/`（Codex），二者语义一致。

## 1. 角色与工具映射

| 角色 | ZCode subagent | Codex agent | 文件所有权 | 说明 |
|---|---|---|---|---|
| 主 Agent / 集成者 | 主会话（非 subagent） | 主会话 | `main/**`、`components/gamepad_core/**`、`components/board_bsp/**`、公共头文件、`CMakeLists.txt`、`idf_component.yml`、`sdkconfig.defaults`、`docs/firmware/interface-contract.md` | 唯一可合并主分支；唯一可改公共接口 |
| USB 工程师 | `usb-engineer` | `usb_engineer` | `components/usb_gamepad/**` | HID 描述符、报告打包、USB 状态机 |
| 输入工程师 | `input-engineer` | `input_engineer` | `components/input_analog/**`、`components/input_buttons/**`、`components/calibration/**` | ADC 采样、消抖、校准；`board_bsp` 引脚表仅在主 Agent 审核授权后修改 |
| QA 审查员 | `qa-reviewer` | `qa_reviewer` | 默认只读；授权后写 `tests/**`、`docs/test-evidence/**` | 契约对齐、Host 单测、静态检查、就绪评估 |

并发上限：**同时最多 3 个子 Agent**，且只并行彼此独立（不触碰对方文件）的任务。

## 2. 任务生命周期

```
PROPOSED → ASSIGNED → IN_PROGRESS → IN_REVIEW → MERGED / REJECTED / BLOCKED
```

- 任务以文件为准：`docs/tasks/<任务ID>-<短名>.md`，从 `docs/tasks/_TEMPLATE.md` 生成。任务 ID 沿用 `docs/process/plan.md` 的编号（如 `M0-03`）。
- 只有主 Agent 可以创建/指派任务、合并成果、把状态推进到 MERGED。
- 子 Agent 只处理**一个**任务；完成后输出第 6 节格式的报告并停止，不自行领取下一个任务。
- 里程碑门控照 `docs/process/plan.md`：M0-01（板卡确认）未完成不得派发任何编码任务；接口契约（`docs/firmware/interface-contract.md`）未冻结不得并行 USB 与 Input 实现。

## 3. 分支与提交规范

- 每个任务一个分支：`<任务ID小写>-<短名>`，如 `m0-03-hid-descriptor`，从 `main` 切出。
- 提交信息格式：`[<任务ID>] <一句话摘要>`，例如 `[M0-03] 冻结 HID Report Descriptor 与打包测试`。
- 一次提交只针对一个任务；不把无关改动混进同一提交。
- 合并由主 Agent 完成审查后执行；子 Agent 不得执行 `reset --hard`、`clean -fd`、force-push、跨任务 rebase。
- 冲突（两个任务需要改同一文件）：双方立即停止，由主 Agent 裁决唯一责任人并记录到任务的"冲突"栏。

## 4. 门禁（合并前必查）

1. **编译门禁**：`idf.py build` 通过；工具链不可用 → 整项标 `NOT_RUN` 并写明原因，禁止虚报。
2. **Host 测试门禁**：相关单测（校准/死区/消抖/映射/报告序列化）通过。
3. **引脚门禁**：改动涉及 GPIO 时，`python tools/validate_pinmap.py docs/hardware/board-pinmap.md` 无 ERROR；未核实引脚必须带 `TODO_BOARD_VALIDATION` 标记，合并前 `grep -rn "TODO_BOARD_VALIDATION" components/ main/` 的每一处都有对应未完成任务编号。
4. **契约门禁**：改 HID Descriptor 必须同步改 Report 结构/长度、测试和 `docs/firmware/interface-contract.md` 变更记录；公共类型改动必须先有 ADR。
5. **诚实门禁**：报告里的测试状态只能是 PASS / FAIL / NOT_RUN / BLOCKED；编译通过 ≠ 实机通过。

## 5. 接口冻结与变更流程

1. 冻结前：`docs/firmware/interface-contract.md` 状态为 DRAFT，任何 Agent 可提意见，只有主 Agent 定稿。
2. 冻结后：任何契约变更必须（a）写 ADR 到 `docs/decisions/`，（b）主 Agent 审批，（c）同步更新描述符、序列化代码与测试，三者缺一不可。
3. `gamepad_state_t`、报告字节布局、按钮位映射、hat 编码、USB 状态机、快照同步方式均属契约范围。

## 6. 固定汇报模板（每个任务收尾必交）

```
## 任务报告：<任务ID> <标题>
- 需求 ID / 测试 ID：
- 修改文件：（逐个列出，含新增/删除）
- 接口/API 影响：（无 则写"无"）
- 测试命令与结果：（PASS / FAIL / NOT_RUN + 原因）
- 硬件待测项：（需用户实机执行的步骤清单）
- 已知风险：
- 下一步建议：
```

## 7. 证据与缺陷

- 实测证据存 `docs/test-evidence/<测试ID>/<YYYY-MM-DD>-<描述>.{png,log,md,txt}`；记录字段按 `docs/process/test-matrix.md` 报告模板。
- `docs/process/test-matrix.md` 的状态只能由证据驱动变更；FAIL 建缺陷 `DEF-<序号>`，按 S0–S3 分级（见需求文档 8.2）。
- 用户提供的硬件事实（板卡型号、原理图、摇杆参数等）由主 Agent 记录进 `docs/hardware/hardware-questions.md` 与 `docs/hardware/board-pinmap.md`，来源必须可追溯。

## 8. 环境事实锁定

- ESP-IDF 与 esp_tinyusb 版本在首次编译通过后写入 `docs/decisions/` ADR，并提交 `dependencies.lock`；升级须独立变更单。
- Host 单测框架定为 CTest（纯 CMake，不依赖 ESP-IDF 也能在 PC 跑）；逻辑代码与硬件寄存器访问分离以保证可测。
- 开发期 VID/PID 沿用 esp_tinyusb 示例自带测试标识，量产前必须替换为授权标识（追踪于 `docs/decisions/`）。

## 9. 会话启动检查单（主 Agent 每次开新会话先做）

1. 读 `AGENTS.md`、`docs/process/plan.md`、`docs/tasks/`、`docs/process/test-matrix.md`，确认当前里程碑与未决任务。
2. `git status` / `git log --oneline -10` 确认工作区干净、无未合并分支遗留。
3. 有硬件待办时提醒用户；无新证据不得改任何测试状态。
