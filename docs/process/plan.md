# 阶段规划 / 里程碑看板

> 任务执行方式：按 `multi-agent-protocol.md` 派发，任务文件从 `../tasks/_TEMPLATE.md` 生成，状态流转见协议第 2 节。看板状态只能由主 Agent 依据任务 MERGED / 实测证据更新。

| 阶段 | 工作 | 退出判据 | 状态 |
|---|---|---|---|
| M0 | USB HID 最小 Demo，1 摇杆 + A/B/Start，Windows/Steam/《双影奇境》真实测试 | 目标游戏认得设备并接受关键输入 | NOT_STARTED |
| M1 | 6 路模拟、15 数字键、MCP23017 或直连 | 所有输入数据正确 | NOT_STARTED |
| M2 | 分层、滤波、校准、NVS、USB 状态机 | 编译/单测/板测及需求对齐 | NOT_STARTED |
| M3 | 游戏覆盖、20 次重连、2h 稳定性 | P0 回归测试通过 | NOT_STARTED |
| M4 | 原理图、PCB、样板打样 | 板上 P0 回归且电气评审通过 | NOT_STARTED |
| M5 | 外壳、装配和人体工程学 | 可持续舒适游玩 | NOT_STARTED |
| M6 | BLE/2.4G、震动、电池（非 P0） | 独立验收 | NOT_STARTED |

## M0 Task 分解
1. M0-01：识别实际 S3 板卡与 USB-OTG 端口；输出可用引脚表及来源。**绝不能猜**。
2. M0-02：创建 `idf.py build` 成功的 ESP-IDF 最小工程；固定依赖。
3. M0-03：实现 HID Report Descriptor + 打包（LX/LY/AB），对值域与长度做 Host 测试。
4. M0-04：集成 ADC / 两键读取与基本消抖、USB 状态机；编译。
5. M0-05：用户在 Windows `joy.cpl` 记录证据。
6. M0-06：用户在 Steam Input 记录映射，再在《双影奇境》游戏实测。
7. M0-07：根据结果判定 GO / NO-GO；失败时开新任务而非开始画板。

## 合并策略
Architect 首先交付接口规范；USB / Input / Test 不同目录并行；Integrator 在独立分支逐个审查合并，不能把多 Agent 输出一次性无审查覆盖主分支。
