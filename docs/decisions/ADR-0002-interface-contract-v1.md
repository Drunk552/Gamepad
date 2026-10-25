# ADR-0002 接口契约 v1.0 冻结

日期：2026-10-25 · 状态：ACCEPTED · 发起：主 Agent（规划会话）

## 背景
按 multi-agent-protocol.md §2/§5，USB 与输入模块并行实现前必须冻结接口契约。主 Agent 在 2026-10-25 规划会话提出冻结候选与六个决策点（D1-D6），用户拍板"按建议"全部采纳。

## 决策
- **D1** M0 即冻结全量 13 字节报告，未实现输入恒发中性值——避免 M0→M1 修改描述符导致 Windows/Steam 重新映射与已跑测试作废。
- **D2** Y/Ry 轴向下为正（HID 通用桌面惯例，减少 Steam 映射翻转）。
- **D3** 按钮位序采用 Xbox 序：bit0..bit10 = A,B,X,Y,LB,RB,Select,Start,L3,R3,Home；D-pad 只走 hat。
- **D4** 不使用 Report ID（单报告设备）。
- **D5** LT/RT 映射 HID Usage Z/Rz，各 8bit，独立双幅值。
- **D6** hat 中性 = 0x08 + Null State 标志。
- 同步冻结：快照同步 = portMUX 临界区整结构复制；USB 状态机（BOOT→INIT→USB_WAIT→USB_ACTIVE）归属 gamepad_core，usb_gamepad 仅事件上报；bInterval=4ms、采样 2ms 目标；M0 校准常量（死区 ±5%、消抖 15ms）。

## 影响
- `docs/firmware/interface-contract.md` 状态 DRAFT → ACCEPTED（v1.0）。
- 接口冻结门禁解除：M0-02（最小工程）完成后，M0-03（usb-engineer）与 M0-04（input-engineer）可并行实现。
- M0-03 必须交付与契约 §2/§3/§4 逐字段一致的描述符与序列化 Host 测试。

## 后续
- 任何契约变更：新 ADR + 主 Agent 审批 + 描述符/序列化代码/测试三同步，缺一不可。
- M2 校准体系落地时以新 ADR 升级契约 §9 并引入参数版本号。
