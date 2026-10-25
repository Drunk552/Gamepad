# 决策记录（ADR）

架构与技术决策按时间顺序编号记录，文件名 `ADR-<序号>-<短名>.md`。每条记录：背景、决策、理由、影响、状态（PROPOSED / ACCEPTED / SUPERSEDED）。

接口层面的变更（`gamepad_state_t`、报告布局、按钮位、USB 状态机）除写 ADR 外，还必须同步 `docs/interface-contract.md` 的变更记录表。

| ADR | 主题 | 状态 |
|---|---|---|
| [ADR-0001](ADR-0001-project-baseline.md) | 项目基线决策：HID 路径、多 Agent 结构、测试与构建约定 | ACCEPTED |
