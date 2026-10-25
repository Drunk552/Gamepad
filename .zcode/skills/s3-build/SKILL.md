---
name: s3-build
description: "构建 S3 Gamepad 固件并做诚实验证。当需要跑 idf.py build、编译固件、执行 Host 单元测试（CTest）、检查 TODO_BOARD_VALIDATION 合并门禁、确认 ESP-IDF 环境/版本时使用。用户或子 Agent 任务要求'编译一下''跑测试''过门禁'时也用。环境不可用时明确标 NOT_RUN，绝不虚报。"
---

# S3 Gamepad 构建与验证纪律

目标：产出可信的构建/测试结论。状态只有 PASS / FAIL / NOT_RUN，工具链不可用必须写明原因。

## 1. 定位 ESP-IDF 环境

按顺序探测：
1. `idf.py --version` 是否已在 PATH。
2. 常见安装位置：`%USERPROFILE%\esp\esp-idf\`、`D:\esp\esp-idf\`、VS Code ESP-IDF 扩展的安装目录（`~/.espressif` / `%USERPROFILE%\.espressif` 下找 `idf_cmd_init.bat` 或 `export.sh`）。
3. 找不到 → 输出 NOT_RUN + 安装指引（ESP-IDF 5.x/6.x + VS Code ESP-IDF 扩展或官方离线安装器），不猜测版本。

找到后记录确切版本号。**首次编译成功后**：把 ESP-IDF 与 esp_tinyusb 版本写入 `docs/decisions/` 新 ADR，并确认 `dependencies.lock` 已提交（版本从此锁定）。

## 2. 编译固件

Git Bash 下二选一：
```bash
# 方式 A：bash 导出
source <idf_path>/export.sh && idf.py build
# 方式 B：走 Windows 初始化脚本
cmd //c "<idf_path>\export.bat && idf.py build"
```
工程根：`D:\work\Gamepad`。记录命令、退出码、警告摘要。

## 3. Host 单元测试（不依赖 ESP-IDF）

```bash
cmake -B build-host -S tests && cmake --build build-host && ctest --test-dir build-host --output-on-failure
```
若 `tests/` 尚不存在（固件工程未创建），明确说明并跳过，不算 FAIL。

## 4. 合并门禁检查

```bash
grep -rn "TODO_BOARD_VALIDATION" components/ main/ 2>/dev/null
```
- 无输出 → 门禁通过。
- 有输出 → 每一处必须能对应到未完成任务编号；无法对应的 → 阻断合并并报告。

## 5. 输出格式

```
## 构建验证结果
- 环境：ESP-IDF <版本>（或 NOT_RUN：<原因>）
- idf.py build：PASS/FAIL/NOT_RUN（<错误摘要>）
- Host 测试：<N> 通过 / <M> 失败 / NOT_RUN
- TODO_BOARD_VALIDATION：<数量> 处，均有任务追踪 / 门禁通过
- 结论：可合并 / 需修复 / 环境缺失
```

## 纪律

- 绝不把"编译通过"表述为"实机通过"；实机结论只能来自 `docs/test-evidence/` 的证据。
- 构建失败时保留完整错误输出供分析，不截断关键报错。
- 不为绕过编译错误而修改 sdkconfig 或全局 CMake（那是主 Agent 的权限）。
