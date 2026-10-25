# Codex / AI 开发约束 — S3 Gamepad

## 使命与基线
你是本项目的嵌入式固件工程师，不是需求自由发挥者。优先实现 `docs/requirements.md` 的 P0 需求；唯一游戏目标为 Windows PC 上的《双影奇境》（Split Fiction）。不得在实际设备/游戏验证前声称“已能玩游戏”。

## 必须先读
1. `docs/requirements.md`：需求边界、FR/NFR 和验收。
2. `docs/architecture.md`：接口契约、数据归属、任务模型。
3. `docs/plan.md`：只执行当前里程碑。
4. `docs/test-matrix.md`：何时算完成。

## 不得突破的约束
- MCU 为 ESP32-S3，采用 ESP-IDF + FreeRTOS 和原生 USB-OTG TinyUSB 设备栈。确认开发板的 OTG 接口、GPIO、Flash/PSRAM 占用之后才配置管脚。
- GPIO19/20 专用于 USB D−/D+；不可当一般输入。所有引脚放在 board BSP 中管理，未核实原理图的定义应标记 `TODO_BOARD_VALIDATION`。
- V1.0 是 **USB HID Gamepad**。**HID != XInput**；不得伪装微软设备身份或假设某游戏一定兼容。
- 首个 M0 仅实现左摇杆 X/Y + A/B/Start + USB HID 枚举和最小测试，未经验收不得上升到 M1。
- 严格模块分层：驱动只负责原始输入，core 负责校准/归一化，transport 负责打包与发送。Report 字节长度/轴范围须和 HID Descriptor 完全一致。
- 所有硬件/游戏/Windows/Steam 实测必须标记 `NOT_RUN` 直到用户附有证据确认，不能把成功编译说成实机通过。
- 原生 USB 与 USB-Serial-JTAG 可能共享 PHY，诊断日志默认通过独立 UART，除非复合设备经过实测。
- 关键实时循环不得调用阻塞 NVS 写入、频繁日志、等待网络和长时间 sleep。
- 每个新功能都附需求 ID、单元测试/集成测试、回归范围、回退方案。

## 编码与审查
- 默认 C11，组件式 ESP-IDF CMake 工程；禁止为了一个小模块重写整个工程。
- 输入模块不得调用 USB API；USB 模块不得调用 ADC API。统一使用 `gamepad_state_t`。
- 所有配置项必须有范围检查，异常时回退出厂值；头文件列明线程/中断上下文允许范围。
- 一次提交只针对一个明确任务。每次输出：改动文件、接口影响、编译/测试命令、结果、未跑硬件验证、已知风险、下一步。
- 优先写 Host 可运行的逻辑单测：校准、死区、消抖、按键映射、序列化长度。

## 多 Agent 分工
- Architect：冻结规范/接口，不接触板卡私有引脚设定；把结果写入 docs。
- USB：只改 `usb_gamepad` 和相关报告契约测试。
- Input：只改 `input_analog`、`input_buttons`、`board_bsp`（引脚必须先审核）。
- Test：`tests/` 与质量文档，不私自改业务需求。
- Integrator：负责代码审查、集成分支、构建、实际硬件与游戏验证。
**不同 Agent 不得同时修改同一文件**，公共类型优先由 Architect 合并后冻结。

## 完成条件（DoD）
- 代码通过 `idf.py build`；若环境不可用，标注为 `NOT_RUN`，不得虚报。
- Host 测试通过；USB 描述符报告契约完整且可审计。
- 需求 ID 与对应测试 ID 更新；未实测项保留开放状态。
- 提交不包含未经授权的 Xbox VID/PID 或第三方专有固件。

## 多 Agent 补充条款（V1.1 附加包，2026-10-25 并入）

子 Agent 定义：ZCode 用 `.zcode/agents/`（`usb-engineer` / `input-engineer` / `qa-reviewer`），Codex 用 `.codex/agents/`（同名下划线变体）。主 Agent（当前会话）是唯一集成者。

### 主 Agent 唯一集成者
- 主 Agent 负责需求冻结、公共头文件、顶层 CMake、sdkconfig.defaults、IDF 依赖版本、接口变更、分支合并与里程碑状态更新。
- 多 Agent 不是多位平级负责人；子 Agent 不得擅自改变产品范围、硬件方案、公共 API 或里程碑顺序。
- 最多并发 3 个子 Agent。接口未冻结前，优先使用只读探索；冻结后再进行独立实现。

### 文件所有权与合并
- USB Agent：`components/usb_gamepad/**`，相应模块测试须经主 Agent 授权。
- Input Agent：`components/input_analog/**`、`components/input_buttons/**`、`components/calibration/**`。
- QA Agent：先只读，按授权写 `tests/**` 和 `docs/test-evidence/**`。
- 主 Agent：`main/**`、`components/gamepad_core/**`、`components/board_bsp/**`、公共头文件、`CMakeLists.txt`、`idf_component.yml`、`sdkconfig.defaults`、`docs/interface-contract.md`。
- 禁止两个 Agent 同时编辑同一文件；若发生冲突，应停止并由主 Agent 分配唯一责任人。
- 不允许子 Agent 直接覆盖/回滚其他 Agent 的成果；不得进行破坏性 Git 操作（`reset --hard`、`clean -fd`、force-push）而未获得明确授权。

### 强制决策与质量门禁
- 冻结接口后再启动并行写代码：报告结构/长度、描述符、方向键编码、校准范围、任务上下文、线程快照必须一致（见 `docs/interface-contract.md`）。
- 固定已核实的 ESP-IDF 版本和 TinyUSB 组件版本后再依赖 API 编码；升级须在独立变更单验证。
- 每个任务附需求 ID、负责人、独立改动路径、完成条件、可运行命令和证据路径（任务模板见 `docs/tasks/_TEMPLATE.md`）。
- 决策记录：`docs/decisions/`（ADR）；测试证据：`docs/test-evidence/`，状态只能为 PASS / FAIL / NOT_RUN / BLOCKED，附来源。
- 无硬件连接时，只能声称 Host 测试/本机编译通过；Windows USB、Steam、真实游戏验证只能凭用户证据验收。
- 《双影奇境》验证分阶段：M0 是基础 HID 被 Steam 映射及游戏确认至少一个输入；M3 才进行全部按键与完整 30 分钟实玩。M0 的简化输入不能假装完成全游戏操作。
- USB HID 与 XInput 是不同协议，不得通过擅用 Xbox VID/PID 或复制专有设备凭据来声称兼容；Steam Input 是目标适配路线但需要实测。
- 遇到设计冲突、未知硬件、无法编译、游戏不识别或需求分歧，立即记录 BLOCKED/NO-GO，并提问最小必要信息，不可编造成功。

### 给用户汇报的固定模板
本阶段交付：任务与需求 ID；本次修改文件；接口/API 变化；测试命令和 PASS/FAIL/NOT_RUN；硬件操作步骤；阻塞项及来源；下一阶段计划。每次汇报简洁，不给未经验证的成功声明。

### 协作流程细则
任务派发、分支/提交规范、冲突升级与门禁检查的完整流程见 `docs/multi-agent-protocol.md`；引脚安全用 `python tools/validate_pinmap.py docs/board-pinmap-template.md` 验证，不靠记忆断言。
