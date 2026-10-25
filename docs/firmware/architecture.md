# 架构与接口契约

## 主要数据链
`ADC1 [LX,LY,RX,RY,LT,RT]` → `input_analog` → `calibration/filter` → `gamepad_core` → `usb_gamepad` → `Windows/Steam/Input`。
`15 digital switches` → `input_buttons`（直连或 MCP23017） → `debounce` → `gamepad_core`。
`settings_store/NVS` → 默认与校准参数。

## 共享接口（冻结前必审核）
```c
typedef struct {
    int16_t lx, ly, rx, ry;
    uint8_t lt, rt;
    uint16_t buttons;
    uint8_t hat;       /* 0..7; 8 neutral */
    uint32_t sample_ms;
} gamepad_state_t;
```
`GamepadState` 的线程一致性由 core 保证，transport 只消费不可变快照。轴原始 ADC 的滤波参数从配置读入，不以原始 raw 值代替 GamepadState。

## USB 约束
- 标准 HID Gamepad，不保证兼容游戏的 XInput 输入入口。
- TinyUSB 端点忙时丢弃过期帧或等待下轮，不能无限积压。
- USB state: `BOOT > INIT > USB_WAIT > USB_ACTIVE`，断开退回 USB_WAIT，清空可能卡住的按键状态。
- 每次 Descriptor 变更同时修 Report 结构/长度、测试与 Windows 映射记录。

## 资源候选（待实际板卡原理图确认）
- GPIO1..6：ADC1 六路；GPIO8/9：MCP23017 I2C；GPIO13：INT 可选；GPIO10/11：后续电机控制预留；GPIO12：LED 可选。
- GPIO19=D−，GPIO20=D+；GPIO0/45/46 等启动/strap 不随意复用。不同开发板可能占用其他引脚，最终由 `board_pinmap.h` 冻结。
- 开发版选择独立 UART 日志；USB OTG 端口只做 USB HID。

## 数据与测试分离
`components/input_analog` 不 include USB 头文件；`components/usb_gamepad` 不 include ADC 头文件。校准、映射、Report 打包逻辑应可 Host 单测。
