---
name: s3-dispatch
description: "为 S3 Gamepad 固件项目派发多 Agent 任务。当用户说'派发任务''开始 M0-XX''让 USB/Input/QA agent 干活''跑下一个任务''启动多 agent 开发'，或要求按 plan.md 把某项工作交给子 agent 时使用。负责：前置门禁检查、生成任务文件、选择角色 agent、spawn、验收报告、更新看板状态。这是本项目多 Agent 协作的入口技能。"
---

# S3 Gamepad 任务派发流程

你是主 Agent（唯一集成者）。按 `docs/multi-agent-protocol.md` 执行，核心纪律：**一次一个任务、门禁不跳过、报告不齐打回**。

## 第一步：前置检查（派发前必做）

1. 读 `docs/plan.md` 与 `docs/tasks/`，确认当前里程碑和已有任务状态。
2. 里程碑门控：M0-01（板卡确认，见 `docs/board-pinmap-template.md` 状态列与 `docs/hardware-questions.md`）未完成 → **不得派发任何编码任务**，只能派只读分析类任务（如接口契约提案、任务矩阵规划）。
3. 接口门控：`docs/interface-contract.md` 状态为 DRAFT 时，usb-engineer 与 input-engineer 不得并行写实现。
4. 并发门控：同时最多 3 个子 Agent，且任务文件白名单互不重叠。
5. 工作区检查：`git status` 有未提交改动时先提醒用户处理。

## 第二步：生成任务文件

从 `docs/tasks/_TEMPLATE.md` 复制为 `docs/tasks/<任务ID>-<短名>.md`（任务 ID 沿用 plan.md 编号，如 `M0-03-hid-descriptor.md`），填齐：需求 ID、负责人、白名单、DoD、测试方法、禁止事项、回退方案。模板带 ※ 的字段缺一不可。

## 第三步：角色路由

| 任务类型 | subagent |
|---|---|
| USB、HID 描述符、报告打包、枚举、USB 状态机 | `usb-engineer` |
| ADC、摇杆、扳机、按键、消抖、校准、IO 扩展 | `input-engineer` |
| 测试编写、代码审查、契约对齐检查、就绪评估 | `qa-reviewer` |
| 公共接口、架构、CMake、sdkconfig、集成合并 | 主 Agent 自己做，不派发 |

## 第四步：派发

用 Agent 工具 spawn 对应 subagent，prompt 模板：

```
读取任务文件 D:\work\Gamepad\docs\tasks\<文件名>.md 并严格按其中约束执行。
完成后按 docs/multi-agent-protocol.md 第 6 节模板输出任务报告。
你的文件白名单以任务文件为准；遇到门禁或冲突立即停止并在报告中说明。
```

## 第五步：验收与收尾

1. 检查报告 7 字段齐全（需求 ID / 修改文件 / 接口影响 / 测试命令与结果 / 硬件待测项 / 已知风险 / 下一步）；缺项打回补充。
2. 抽查白名单：报告里的修改文件若超出任务白名单 → REJECTED，记录冲突。
3. 更新任务文件状态与 `docs/plan.md` 看板；提醒用户哪些项需要实机验证。
4. 审查通过后由你（主 Agent）在独立分支合并，遵守提交规范 `[<任务ID>] <摘要>`。
5. 向用户汇总：本阶段交付、阻塞项、下一步建议。

## 禁止

- 跳过门禁直接派编码任务；同时派两个会改同一文件的任务。
- 把子 Agent 报告里的 PASS 直接当作实机验证结论。
- 用户尚未说"批准 M0 实施"前派发业务固件编码任务（ kickoff 流程见 `prompts/multiagent-kickoff.txt` 的五项前置交付 A–E）。
