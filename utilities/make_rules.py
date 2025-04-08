#!/usr/bin/env python3

import argparse
import subprocess
import re
import sys
from pathlib import Path

def extract_device_info(dev_path):
    try:
        result = subprocess.run(
            ["udevadm", "info", "--attribute-walk", "--name", dev_path],
            capture_output=True, text=True, check=True
        )

        vendor = re.search(r'ATTRS\{idVendor\}=="([^"]+)"', result.stdout)
        product = re.search(r'ATTRS\{idProduct\}=="([^"]+)"', result.stdout)
        serial = re.search(r'ATTRS\{serial\}=="([^"]+)"', result.stdout)

        if not (vendor and product and serial):
            print(f"[ERROR] Could not extract full device info from {dev_path}")
            sys.exit(1)

        return vendor.group(1), product.group(1), serial.group(1)

    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to run udevadm or invalid device path: {dev_path}")
        sys.exit(1)

def generate_rule(name, vendor, product, serial):
    return (
        f'SUBSYSTEM=="tty", ACTION=="add", '
        f'ATTRS{{idVendor}}=="{vendor}", ATTRS{{idProduct}}=="{product}", '
        f'ATTRS{{serial}}=="{serial}", SYMLINK+="{name}", MODE="0666"\n'
    )

def main():
    parser = argparse.ArgumentParser(description="Generate a combined udev rules file for USB serial devices")
    parser.add_argument("-p", "--path", action="append", required=True, help="Device path, e.g. /dev/ttyUSB1")
    parser.add_argument("-s", "--simlink", action="append", required=True, help="Symlink name, e.g. MY_DEVICE")
    parser.add_argument("-o", "--output", default="dummy", help="Output rules filename (without .rules), default: dummy")

    args = parser.parse_args()

    if len(args.path) != len(args.simlink):
        print("[ERROR] The number of -p/--path and -s/--simlink arguments must match.")
        sys.exit(1)

    output_file = Path(f"{args.output}.rules")
    all_rules = []

    for dev_path, link_name in zip(args.path, args.simlink):
        vendor, product, serial = extract_device_info(dev_path)
        rule = generate_rule(link_name, vendor, product, serial)
        all_rules.append(rule)
        print(f"✅ Added rule for {dev_path} -> {link_name}")

    with open(output_file, "w") as f:
        f.writelines(all_rules)

    print(f"\n📄 Rules written to: {output_file}")
    print("📌 To activate, move the file to /etc/udev/rules.d/ and reload udev:")
    print(f"   sudo mv {output_file} /etc/udev/rules.d/")
    print("   sudo udevadm control --reload-rules && sudo udevadm trigger")

if __name__ == "__main__":
    main()