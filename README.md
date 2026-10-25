# S3 Gamepad · ESP32-S3 USB HID 双摇杆手柄固件

ESP32-S3（N16R8，DevKitC-1 兼容板）原生 USB HID 双摇杆手柄固件工程，目标平台 Windows + Steam《双影奇境》（Split Fiction）。

> 状态：规划与接口契约已冻结（2026-10-25），固件代码按里程碑 M0 起逐步创建；本仓库随实施进度发布源码。

## 硬件与协议

- MCU：ESP32-S3（16MB Flash / 8MB PSRAM），原生 USB-OTG（GPIO19/20）跑 TinyUSB HID Gamepad
- 输入：4 摇杆轴（LX/LY/RX/RY）+ 2 模拟扳机（LT/RT）+ 15 数字键（D-pad 经 hat 传输）
- 协议：标准 USB HID Gamepad。HID ≠ XInput，不伪装微软 VID/PID；开发期使用 esp_tinyusb 示例测试标识，量产前替换为授权标识

## 目录结构（随 M0 实施逐步创建）

```
├── main/                 # 应用入口、任务模型（M0-02 起）
├── components/           # gamepad_core / usb_gamepad / input_analog / input_buttons / calibration / board_bsp
├── tests/                # Host 单元测试（CTest，可在 PC 运行）
├── tools/                # validate_pinmap.py：ESP32-S3 引脚安全静态检查
├── CMakeLists.txt        # 顶层 ESP-IDF 工程（M0-02 起）
└── sdkconfig.defaults    # 目标板配置（M0-02 起）
```

## 构建

- 工具链：ESP-IDF + FreeRTOS + esp_tinyusb（具体版本在首次编译通过后锁定）
- 固件：`idf.py build`
- Host 测试：CTest——校准、死区、消抖、按键映射、HID 报告序列化等逻辑测试不依赖硬件，可在 PC 直接运行

## 测试与验收原则

- 所有实机测试（Windows 枚举 / Steam 映射 / 游戏实测）默认 NOT_RUN，只能凭证据翻转；编译通过 ≠ 实机通过。
- Windows 能枚举 ≠ Steam 能映射 ≠ 游戏支持，三关分别验收。

## 说明

完整项目文档（需求基线、架构设计、接口契约、引脚确认表、任务分解与测试证据）在开发机本地维护，不随本仓库发布。

## 官方参考

- ESP-IDF USB Device Stack: https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32s3/api-reference/peripherals/usb_device.html
- ESP-IDF TinyUSB HID 示例: https://github.com/espressif/esp-idf/tree/master/examples/peripherals/usb/device/tusb_hid
- Steam Input 支持的设备: https://partner.steamgames.com/doc/features/steam_controller/device
- 《双影奇境》好友通行证: https://www.ea.com/zh-hans/games/split-fiction/split-fiction/features/friends-pass-pc
