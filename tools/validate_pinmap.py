#!/usr/bin/env python3
"""ESP32-S3 Gamepad 引脚分配静态验证器。

用法:
    python tools/validate_pinmap.py docs/hardware/board-pinmap.md
    python tools/validate_pinmap.py docs/hardware/board-pinmap.md --json

解析 board-pinmap Markdown 表格（功能 | 候选脚位 | 最终脚位 | 证明 | 状态），
按 ESP32-S3 硬件规则检查每个候选/最终引脚。规则不依赖记忆断言，全部可追溯到
Espressif《ESP32-S3 系列芯片技术规格书》的引脚定义。

退出码: 0=通过(可含 INFO)  1=存在 ERROR  2=仅 WARN
"""
import argparse
import json
import re
import sys
from pathlib import Path

# ---- ESP32-S3 硬件规则表 ----
USB_PINS = {19: "USB D-", 20: "USB D+"}
STRAPPING = {
    0: "Boot 模式选择 strapping，上电瞬间不得被外电路拉到意外电平",
    3: "JTAG 信号源选择 strapping，上电电平决定 JTAG 走 USB 还是引脚；外接电路需评估上电时的电平",
    45: "VDD_SPI 电压 strapping（3.3V/1.8V），外接可能改变 flash 供电电压",
    46: "Boot 模式与 ROM 日志 strapping",
}
FLASH_PINS = set(range(26, 33))  # GPIO26-32: SPI flash，模组内部已占用
OCTAL_PSRAM_PINS = set(range(33, 38))  # GPIO33-37: Octal PSRAM 模组(如 N8R8)占用
UART0_PINS = {43: "UART0 TXD", 44: "UART0 RXD"}
JTAG_PINS = {39: "MTCK", 40: "MTDO", 41: "MTDI", 42: "MTMS"}
ADC1_PINS = set(range(1, 11))   # GPIO1-10 = ADC1_CH0-CH9
ADC2_PINS = set(range(11, 21))  # GPIO11-20 = ADC2_CH0-CH9（与 WiFi 冲突）
VALID_GPIO = set(range(0, 22)) | set(range(26, 49))  # GPIO22-25 在 S3 上不存在
ANALOG_NAMES = {"LX", "LY", "RX", "RY", "LT", "RT"}
GPIO_RE = re.compile(r"GPIO\s*(\d+)", re.IGNORECASE)


def parse_table(md_path: Path):
    """返回 [(功能, 候选, 最终, 状态), ...]，只解析含 GPIO 的数据行。"""
    rows = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not (s.startswith("|") and GPIO_RE.search(s)):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3:
            continue
        func, cand, final = cells[0], cells[1], cells[2]
        status = cells[4] if len(cells) >= 5 else ""
        if func in ("功能", "Function") or set(func) <= set("-: "):
            continue  # 表头 / 分隔线
        rows.append((func, cand, final, status))
    return rows


def check_pin(func: str, pin: int, col: str):
    """对单个 功能->引脚 分配做规则检查，返回 issue 列表。"""
    issues = []
    where = f"{func} -> GPIO{pin} ({col})"

    if pin not in VALID_GPIO:
        issues.append(("ERROR", where, "ESP32-S3 无此引脚（GPIO22-25 不存在，有效范围 0-21 与 26-48）"))
        return issues

    is_usb_func = "USB" in func.upper() or "D-" in func or "D+" in func
    is_analog = func in ANALOG_NAMES or "摇杆" in func or "扳机" in func

    if pin in USB_PINS and not is_usb_func:
        issues.append(("ERROR", where, f"GPIO{pin} 为 {USB_PINS[pin]} 专用，不可挪作一般 IO"))
    if pin in FLASH_PINS:
        issues.append(("ERROR", where, f"GPIO{pin} 属 SPI flash 占用（GPIO26-32），模组内部已连接"))
    if pin in OCTAL_PSRAM_PINS:
        issues.append(("WARN", where, f"GPIO{pin} 在 Octal PSRAM 模组（如 N8R8）上被占用；需确认模组型号后才能使用"))
    if pin in STRAPPING and not is_usb_func:
        issues.append(("WARN", where, f"strapping 引脚：{STRAPPING[pin]}"))
    if pin in UART0_PINS:
        issues.append(("WARN", where, f"GPIO{pin} 是 {UART0_PINS[pin]} 默认脚；本项目计划用独立 UART 日志，占用前需确认"))
    if pin in JTAG_PINS:
        issues.append(("INFO", where, f"GPIO{pin} 为 {JTAG_PINS[pin]}（JTAG），若不用外部 JTAG 可作普通 IO"))
    if is_analog:
        if pin not in ADC1_PINS and pin not in ADC2_PINS:
            issues.append(("ERROR", where, "模拟输入必须分配在 ADC 引脚（ADC1: GPIO1-10，ADC2: GPIO11-20）"))
        elif pin in ADC2_PINS:
            issues.append(("WARN", where, "ADC2 在 WiFi 开启时不可用；本项目虽无 WiFi，仍应优先 ADC1"))
    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pinmap", help="board-pinmap Markdown 文件路径")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = ap.parse_args()

    md = Path(args.pinmap)
    if not md.is_file():
        print(f"[ERROR] 找不到文件: {md}")
        return 1

    rows = parse_table(md)
    if not rows:
        print("[ERROR] 未解析到任何引脚行，请检查表格格式")
        return 1

    all_issues, seen = [], {}
    for func, cand, final, status in rows:
        for col, cell in (("候选", cand), ("最终", final)):
            m = GPIO_RE.search(cell)
            if not m:  # TBD / TODO 等未定
                continue
            pin = int(m.group(1))
            key = (pin, col)
            if key in seen and seen[key] != func:
                all_issues.append(("ERROR", f"{func} 与 {seen[key]} 同时占用 GPIO{pin}（{col}列）", "引脚重复分配"))
            seen.setdefault(key, func)
            all_issues.extend(check_pin(func, pin, col))

    errors = [i for i in all_issues if i[0] == "ERROR"]
    warns = [i for i in all_issues if i[0] == "WARN"]
    infos = [i for i in all_issues if i[0] == "INFO"]

    if args.json:
        print(json.dumps({"errors": errors, "warnings": warns, "infos": infos,
                          "rows_parsed": len(rows)}, ensure_ascii=False, indent=2))
    else:
        for level, where, msg in all_issues:
            print(f"[{level}] {where}: {msg}")
        print(f"\n解析 {len(rows)} 个功能行；ERROR={len(errors)} WARN={len(warns)} INFO={len(infos)}")
        if not all_issues:
            print("未发现引脚规则违规（注意：本脚本只覆盖 S3 通用规则，具体开发板复用仍需原理图核对）。")

    return 1 if errors else (2 if warns else 0)


if __name__ == "__main__":
    sys.exit(main())
