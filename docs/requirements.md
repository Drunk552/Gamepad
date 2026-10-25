# 产品需求基线（S3 Gamepad V1.0）

## 目标
开发 ESP32-S3 USB 有线双摇杆游戏手柄，优先在 Windows Steam 版《双影奇境》（Split Fiction）实测。EA 官方确认 PC 本地合作支持两只控制器，或一只控制器+键鼠。Windows 能枚举 ≠ Steam 能映射 ≠ 游戏支持，三个关卡必须分别验收。

## P0 输入清单
- 模拟：左 X/Y、右 X/Y 共 4 轴，LT/RT 共 2 轴；6 路模拟输入，每路独立校准。
- 数字：ABXY4、D-pad4、LB/RB2、L3/R3 2、Start/Select/Home3，共 15 键。
- 协议：原生 USB HID Gamepad；使用合法/授权测试标识，不伪装微软品牌。
- 数据：`int16_t lx,ly,rx,ry`（中心0），`uint8_t lt,rt`（0..255），`uint16_t buttons`、`uint8_t hat`（0..7/8=neutral）。

## P0 功能需求
| ID | 要求 | 验收 |
|---|---|---|
| FR-001 | Windows 识别 USB HID Gamepad | T-USB-01 |
| FR-002 | 4 轴摇杆准确、独立、可校准 | T-ADC-01 |
| FR-003 | LT/RT 模拟行程独立、单调 | T-ADC-02 |
| FR-004 | 15 数字键短按/长按正确 | T-KEY-01 |
| FR-005 | 消抖、死区、限幅、滤波 | T-FLT-01 |
| FR-006 | 统一完整状态快照和 report 契约 | T-FW-01 |
| FR-007 | 20 次重连不死机、不卡键 | T-USB-02 |
| FR-008 | Steam 映射并通过目标游戏实玩 | T-GAME-01 |
| FR-009 | UART/诊断可追踪输入与 USB 状态 | T-DIAG-01 |

## 首版参考性能指标（验收目标，不是现有能力）
- ADC/按键采样目标 500 Hz；USB 报告目标 250 Hz；可按测量调整。
- 输入变化到 HID 报告构建的 99 分位目标不超过 20ms，使用仪器或时间戳实测。
- 连续游戏至少 30min；持续工作 2h；20 次重连；摇杆放手 10 秒不漂移出死区。

## M0 否决条件
若无法在 Windows → Steam Input →《双影奇境》逐项通过最低操作测试，停止 PCB / 外壳投入，先调整协议或兼容路径。

## 非首版范围
BLE、2.4G 无线、锂电充电、震动、RGB、PC 配置工具和跨平台主机兼容均列 P1/P2，不得偷偷加入 M0。
