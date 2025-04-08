import subprocess
import glob
import re

def extract_device_info(dev_name):
    try:
        # Get ATTRS from attribute-walk (deeper device hierarchy)
        result_walk = subprocess.run(
            ["udevadm", "info", "--attribute-walk", "--name", dev_name],
            capture_output=True, text=True, check=True
        )

        vendor = re.search(r'ATTRS\{idVendor\}=="([^"]+)"', result_walk.stdout)
        product = re.search(r'ATTRS\{idProduct\}=="([^"]+)"', result_walk.stdout)
        serial = re.search(r'ATTRS\{serial\}=="([^"]+)"', result_walk.stdout)

        # Get environment variables from direct info
        result_info = subprocess.run(
            ["udevadm", "info", "--name", dev_name],
            capture_output=True, text=True, check=True
        )

        # Extract symlinks (DEVLINKS=...)
        symlinks = re.findall(r'E: DEVLINKS=(.+)', result_info.stdout)
        symlink_list = symlinks[0].split() if symlinks else []

        # Extract ID_PATH
        id_path_match = re.search(r'E: ID_PATH=(.+)', result_info.stdout)
        id_path = id_path_match.group(1) if id_path_match else "N/A"

        return {
            "device": dev_name,
            "idVendor": vendor.group(1) if vendor else "N/A",
            "idProduct": product.group(1) if product else "N/A",
            "serial": serial.group(1) if serial else "N/A",
            "idPath": id_path,
            "symlinks": symlink_list
        }

    except subprocess.CalledProcessError:
        print(f"Failed to get info for {dev_name}")
        return None

def main():
    tty_devices = sorted(glob.glob("/dev/ttyUSB*"))

    if not tty_devices:
        print("No /dev/ttyUSB* devices found.")
        return

    for dev in tty_devices:
        info = extract_device_info(dev)
        if info:
            print(f"\nDevice: {info['device']}")
            print(f"  idVendor : {info['idVendor']}")
            print(f"  idProduct: {info['idProduct']}")
            print(f"  serial   : {info['serial']}")
            print(f"  idPath   : {info['idPath']}")
            print(f"  symlinks : {', '.join(info['symlinks']) if info['symlinks'] else 'None'}")

if __name__ == "__main__":
    main()