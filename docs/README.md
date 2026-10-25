# S3 Gamepad 文档地图

所有项目文档都在 `docs/` 下，按关注点分组。新会话/新角色从这里开始。

## 目录总览

| 分组 | 文件 | 内容 | 主要使用者 |
|---|---|---|---|
| **product/** 产品与需求 | `requirements.md` | P0 需求基线（FR/NFR、输入清单、M0 否决条件）——**执行基线** | 所有 Agent |
| | `PRD-S3-Gamepad-V1.0.docx` | 完整版产品/设计母本（背景、BOM、算法参数、风险台账） | 人员参考 |
| **hardware/** 硬件事实 | `hardware-questions.md` | 必须由用户确认的 9 项硬件事实——**M0-01 前置** | 用户 + 主 Agent |
| | `board-pinmap.md` | 引脚确认表（候选→最终→冻结），配套 `tools/validate_pinmap.py` | 主 Agent + input-engineer |
| **firmware/** 固件设计 | `architecture.md` | 数据链、分层、任务模型、USB 状态机 | 所有 Agent |
| | `interface-contract.md` | 接口契约冻结文档（`gamepad_state_t`、报告布局、按钮位）——当前 DRAFT v0.1 | 主 Agent 冻结；usb/input 遵守 |
| **process/** 流程与验收 | `plan.md` | 里程碑看板 M0~M6 + M0 任务分解 | 主 Agent 派发依据 |
| | `multi-agent-protocol.md` | 协作协议：任务生命周期、门禁、分支/提交规范、汇报模板 | 所有 Agent |
| | `test-matrix.md` | 测试矩阵（10 项，证据驱动，默认 NOT_RUN） | qa-reviewer + 用户实测 |
| **prompts/** AI 启动词 | `zcode-kickoff.txt`（ZCode 新会话用，**推荐**）/ `multiagent-kickoff.txt`（Codex 版）/ `codex-m0.txt`（单 Agent 版） | AI 会话启动提示词 | 用户投喂新会话 |
| **tasks/** 工作产物 | `_TEMPLATE.md` + 任务文件 | 每任务一文件（从模板生成） | 主 Agent 创建，子 Agent 执行 |
| **decisions/** 工作产物 | `README.md` + ADR-* | 架构/技术决策记录 | 主 Agent 维护 |
| **test-evidence/** 工作产物 | `<测试ID>/<日期>-<描述>` | 实测证据归档，test-matrix 状态翻转的唯一依据 | 用户产出，qa-reviewer 核对 |

## 推荐阅读顺序

- **主 Agent（每次新会话）**：本文件 → `AGENTS.md` → `process/plan.md` + `tasks/` 现状 → `process/test-matrix.md` → `git log --oneline -10`。
- **usb-engineer / input-engineer**：任务文件 → `AGENTS.md` → `firmware/interface-contract.md`（DRAFT 则只做只读分析）→ `multi-agent-protocol.md` 汇报格式。
- **qa-reviewer**：任务文件 → `firmware/interface-contract.md` → `process/test-matrix.md` → `test-evidence/`。
- **用户（你）**：`product/requirements.md`（要做什么）→ `hardware/hardware-questions.md`（要回答什么）→ 实测后把证据交给主 Agent。

## 文档规则

1. **状态词统一**：文档/契约用 DRAFT / ACCEPTED / SUPERSEDED；测试用 PASS / FAIL / NOT_RUN / BLOCKED；引脚用 NOT_VERIFIED / VERIFIED；任务用 PROPOSED / ASSIGNED / IN_PROGRESS / IN_REVIEW / MERGED / REJECTED / BLOCKED。
2. **单一事实源**：需求以 `product/requirements.md` 为执行基线（docx 为母本参考）；引脚以 `hardware/board-pinmap.md` 为准（代码中的 `board_pinmap.h` 由它生成/核对）；接口以 `firmware/interface-contract.md` 为准。
3. **变更走流程**：需求/接口变更必须先写 `decisions/` ADR；测试状态只能被 `test-evidence/` 里的证据改变。
4. **新文档落位**：产品类进 `product/`，硬件类进 `hardware/`，固件设计进 `firmware/`，流程/规范进 `process/`；不确定就问主 Agent，不要在 `docs/` 根目录新建散文件。
