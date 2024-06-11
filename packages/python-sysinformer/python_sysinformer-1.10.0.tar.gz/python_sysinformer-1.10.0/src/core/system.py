import os
import datetime
import platform
import subprocess
import time
import re
import distro

from src.utilities.utils import print_bold_kv, print_title


def get_last_boot_time() -> str:
    """Returns the last boot time as a date and time string."""
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(
                ["sysctl", "-n", "kern.boottime"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            if match := re.search(r"sec = (\d+)", result):
                boot_timestamp = int(match[1])
                return datetime.datetime.fromtimestamp(boot_timestamp).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            else:
                raise ValueError("Could not parse kern.boottime output")
        except (subprocess.CalledProcessError, ValueError) as e:
            print(f"An error occurred while getting last boot time: {e}")
            return "Error obtaining last boot time"
    elif platform.system() == "Linux":
        try:
            return subprocess.run(
                ["uptime", "-s"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while getting last boot time: {e}")
            return "Error obtaining last boot time"
    else:
        return "Not supported on this OS"


def get_system_uptime() -> str:
    """Returns the system uptime as a string."""
    if platform.system() == "Linux":
        try:
            uptime_seconds = time.time() - os.stat("/proc/1").st_ctime
            days, rem = divmod(uptime_seconds, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, _ = divmod(rem, 60)
            return f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"
        except Exception as e:
            print(f"An error occurred while getting system uptime on Linux: {e}")
            return "Error in obtaining uptime"
    elif platform.system() == "Darwin":
        try:
            uptime_output = subprocess.run(
                ["uptime"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            return ", ".join(uptime_output.split(",")[:2])
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while getting system uptime: {e}")
            return "Error in obtaining uptime"
    else:
        return "Not supported on this OS"


def get_user_count_unix(path: str) -> int:
    """Counts the number of user directories in the given path for Unix systems."""
    try:
        # Exclude the "Shared" folder from the count
        return len(
            [
                d
                for d in os.listdir(path)
                if os.path.isdir(os.path.join(path, d)) and d != "Shared"
            ]
        )
    except FileNotFoundError:
        return 0


def get_system_info() -> dict:
    """Gets system information depending on the OS."""
    system_info = {
        "os_type": platform.system(),
        "hostname": platform.node(),
        "kernel_info": platform.uname().release,
        "architecture": platform.machine(),
        "dist": "N/A",
        "dist_version": "N/A",
        "uptime": "UNKNOWN",
        "last_boot_date": "UNKNOWN",
        "users_nb": 0,
        "current_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }

    system_info["uptime"] = get_system_uptime()
    system_info["last_boot_date"] = get_last_boot_time()
    if system_info["os_type"] == "Linux":
        system_info["dist"] = distro.name()
        system_info["dist_version"] = (
            platform.freedesktop_os_release().get("VERSION") or distro.version()
        )
        system_info["users_nb"] = get_user_count_unix("/home")

    elif system_info["os_type"] == "Darwin":
        system_info["dist"] = "macOS"
        system_info["dist_version"] = platform.mac_ver()[0]
        system_info["users_nb"] = get_user_count_unix("/Users")

    return system_info


def print_system_info() -> None:
    """Prints various system information."""
    system_info = get_system_info()

    print_title("System Information")
    print_bold_kv("Hostname", system_info["hostname"])
    print_bold_kv(
        "OS",
        f"{system_info['os_type']} {system_info['dist']} {system_info['dist_version']}",
    )
    print_bold_kv("Kernel", system_info["kernel_info"])
    print_bold_kv("Architecture", system_info["architecture"])
    print_bold_kv("Uptime", system_info["uptime"])
    print_bold_kv("Last boot", system_info["last_boot_date"])
    print_bold_kv("Users", system_info["users_nb"])
    print_bold_kv("Server datetime", system_info["current_date"])
