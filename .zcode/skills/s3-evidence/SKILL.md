---
name: s3-evidence
description: "记录 S3 Gamepad 的硬件/Windows/Steam/游戏实测证据并更新测试矩阵。当用户提供 joy.cpl 截图、Steam Input 配置结果、《双影奇境》实测反馈、串口日志、拔插/稳定性测试结果等任何实机证据时使用。test-matrix 的 NOT_RUN 只能靠证据翻成 PASS/FAIL——编译通过不算。也用于判断 M0 GO/NO-GO。"
---

# S3 Gamepad 测试证据记录流程

## 1. 收取证据

证据形式：截图 / 日志文件 / 照片 / 视频 / 用户的口头描述（口头描述可记 PARTIAL，截图补齐后才算完整）。

保存到：`docs/test-evidence/<测试ID>/<YYYY-MM-DD>-<短描述>.<扩展名>`

## 2. 完整记录字段

每条证据（同名 .md 或 test-matrix 报告区）必须含：
日期、硬件板型、固件 commit、ESP-IDF 版本、Windows 版本、Steam Input 配置、游戏版本与启动路径、步骤、期望、实际结果、证据文件路径、缺陷编号（FAIL 时）。

字段不全时：能补的向用户要（例如"joy.cpl 截图里设备名是什么"），不能补的在记录里标 `PARTIAL`。

## 3. 更新测试矩阵

`docs/process/test-matrix.md` 对应行的 当前状态：
- `NOT_RUN` → `PASS`：仅当证据完整且通过条件满足。
- `NOT_RUN` / `PASS` → `FAIL`：证据显示不满足通过条件；同时建缺陷 `DEF-<序号>`（下一个可用编号），按需求文档 8.2 定级 S0–S3。
- 需要用户操作但暂缺证据 → 保持 `NOT_RUN`，把待办步骤列给用户。

## 4. M0 GO / NO-GO 判定

M0 相关项：T-USB-01（joy.cpl 枚举）→ Steam Input 映射确认 → T-GAME-01（游戏实测）。三者是递进关卡，前两项通过不能替代游戏实测。

判定输出：
- **GO**：游戏接受关键输入（移动/镜头/确认中至少一项稳定可控）→ 提示可进入 M1，同时列出未闭环项。
- **NO-GO**：按失败类别归因（枚举失败 / 报告错误 / Steam 未识别 / 游戏未识别 / 映射丢失），停止 PCB 投入，给出下一步修复任务建议（写进 docs/tasks/ 提案）。

## 禁止

- 无证据文件把 NOT_RUN 改成 PASS；把编译/Host 测试结果写成实机结果。
- 替用户"脑补"实验结果；用户描述含糊时先问清。
- 跳过 Steam Input 直接拿游戏结果当映射验证。
