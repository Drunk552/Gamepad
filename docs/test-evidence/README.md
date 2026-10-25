# 测试证据目录

存放硬件 / Windows / Steam / 游戏实测的证据文件，是 `docs/test-matrix.md` 状态变更的唯一依据。

## 目录与命名

```
docs/test-evidence/<测试ID>/<YYYY-MM-DD>-<短描述>.<ext>
```

示例：`docs/test-evidence/T-USB-01/2026-10-26-joy-cpl-枚举截图.png`

## 每条证据必须附带的信息

在同名 `.md` 文件或 `docs/test-matrix.md` 报告中记录（模板见需求文档 8.1 / test-matrix.md）：

- 日期、硬件板型、固件 commit、ESP-IDF 版本
- 主机 Windows 版本、Steam Input 配置、游戏版本与启动路径
- 步骤、期望、实际结果
- 截图/日志/视频路径
- 缺陷编号（若 FAIL）

## 状态规则

- 只有 `PASS / FAIL / NOT_RUN / BLOCKED` 四种状态。
- 没有证据文件链接，任何测试不得从 `NOT_RUN` 翻转为 `PASS`。
- 编译通过、Host 单测通过都不构成实机证据。
