import platform
import re
import subprocess

from typing import Literal, Optional
from tabulate import tabulate
import psutil

from src.utilities.utils import print_title


def calculate_memory_usage(
    total: int, free: int, buffers: int, cached: int
) -> tuple[int, int, float]:
    """
    Calculate the total, free, and used percentage for memory or swap.

    Parameters:
        total (int): Total memory or swap.
        free (int): Free memory or swap.
        buffers (int): Buffered memory (only applicable for memory, not swap).
        cached (int): Cached memory (only applicable for memory, not swap).

    Returns:
        tuple: Total, free, and used percentage.
    """
    total //= 1024
    free = (free + buffers + cached) // 1024
    used_percentage = ((total - free) / total) * 100 if total != 0 else 0

    return total, free, used_percentage


def format_memory_value(value_in_mb: float) -> str:
    """Formats memory values to display in MB or GB as appropriate."""
    if value_in_mb > 1000:
        return f"{value_in_mb / 1024:.2f}GB"
    else:
        return f"{value_in_mb}MB"


def get_memory_info() -> (
    tuple[str, str, float | Literal[0], float | Literal[0], str, str, float | Literal[0], float | Literal[0]]
):
    """Get memory information"""
    if platform.system() == "Darwin":
        return get_memory_info_macos()
    elif platform.system() == "Linux":
        try:
            mem_info = {
                i.split()[0].rstrip(":"): int(i.split()[1])
                for i in open("/proc/meminfo", encoding="UTF-8").readlines()
            }
        except (FileNotFoundError, PermissionError):
            # print(f"Error reading file '/proc/meminfo': {exception}")
            return ("0MB", "0MB", 0, 0, "0MB", "0MB", 0, 0)

        keys = ["MemTotal", "MemFree", "Buffers", "Cached", "SwapTotal", "SwapFree"]
        if any(key not in mem_info for key in keys):
            print("Not all keys found in '/proc/meminfo'")
            return ("0MB", "0MB", 0, 0, "0MB", "0MB", 0, 0)

        total_memory, mem_free, mem_used_percentage_calc = calculate_memory_usage(
            mem_info["MemTotal"],
            mem_info["MemFree"],
            mem_info["Buffers"],
            mem_info["Cached"],
        )

        memory_usage = psutil.virtual_memory().percent
        swap_usage = psutil.swap_memory().percent
        swap_total, swap_free, swap_used_percentage_calc = calculate_memory_usage(
            mem_info["SwapTotal"], mem_info["SwapFree"], 0, 0
        )

        return (
            format_memory_value(total_memory),
            format_memory_value(mem_free),
            memory_usage,
            mem_used_percentage_calc,
            format_memory_value(swap_total),
            format_memory_value(swap_free),
            swap_usage,
            swap_used_percentage_calc,
        )
    else:
        return ("0MB", "0MB", 0, 0, "0MB", "0MB", 0, 0)


def get_total_memory_of_all_processes() -> float:
    """
    Get the total memory usage of all processes on macOS.

    Returns:
        int: Total memory usage of all processes in MB.
    """
    # Get process info
    ps = (
        subprocess.Popen(["ps", "-caxm", "-orss,comm"], stdout=subprocess.PIPE)
        .communicate()[0]
        .decode()
    )

    # Iterate processes
    process_lines = ps.split("\n")
    sep = re.compile(r"[\s]+")
    ps_total = 0  # kB
    for row in range(1, len(process_lines)):
        row_text = process_lines[row].strip()
        row_elements = sep.split(row_text)
        try:
            rss = float(row_elements[0]) * 1024
        except (ValueError, IndexError):
            rss = 0  # ignore...
        ps_total += rss
    return ps_total / 1024 / 1024 or 0


def get_memory_info_macos() -> (
    tuple[str, str, float | Literal[0], float | Literal[0], str, str, float | Literal[0], float | Literal[0]]
):
    """Get memory information on macOS"""
    try:
        sysctl_output = subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode()
    except (subprocess.CalledProcessError, PermissionError):
        return ("0MB", "0MB", 0, 0, "0MB", "0MB", 0, 0)

    total_memory = int(sysctl_output.strip()) // (1024 * 1024)  # Convert bytes to MB

    mem_usage_process = get_total_memory_of_all_processes()
    mem_free = round(total_memory - mem_usage_process)
    memory_usage = psutil.virtual_memory().percent
    mem_used_percentage_calc = (
        ((total_memory - mem_free) / total_memory) * 100 if total_memory != 0 else 0
    )

    swap_output = subprocess.check_output(["sysctl", "-n", "vm.swapusage"]).decode()
    swap_stats = {
        k: float(v.replace("M", ""))
        for k, v in re.findall(r"(\w+) = (\d+\.?\d*)M", swap_output)
    }
    swap_total = swap_stats.get("total", 0)  # Already in MB
    swap_free = swap_stats.get("free", 0)  # Already in MB
    swap_usage = psutil.swap_memory().percent
    swap_used_percentage_calc = (
        ((swap_total - swap_free) / swap_total) * 100 if swap_total != 0 else 0
    )

    return (
        format_memory_value(total_memory),
        format_memory_value(mem_free),
        memory_usage,
        mem_used_percentage_calc,
        format_memory_value(swap_total),
        format_memory_value(swap_free),
        swap_usage,
        swap_used_percentage_calc,
    )


def show_warning_msg() -> Optional[str]:
    """
    Print the macOS warning message
    """
    if platform.system() == "Darwin":
        return "\033[1mWARNING\033[0m: calc memory usage derived from process info; sys usage from psutil"
    return "\033[1mWARNING\033[0m: memory usage derived from '/proc/meminfo' and psutil"


def print_memory_info() -> None:
    """
    Print the memory information table
    """
    # Memory
    (
        mem_total,
        mem_free,
        memory_usage,
        mem_used_percentage_calc,
        swap_total,
        swap_free,
        swap_usage,
        swap_used_percentage_calc,
    ) = get_memory_info()

    table = [
        ["Memory", f"{mem_free}", f"{mem_total}", f"{mem_used_percentage_calc:.2f}%", f"{memory_usage:.2f}%"],
        ["Swap", f"{swap_free}", f"{swap_total}", f"{swap_used_percentage_calc:.2f}%", f"{swap_usage:.2f}%"],
    ]

    headers = ["Type", "Free", "Total", "Calc Usage", "Sys Usage"]

    print_title("Memory Information")
    print(show_warning_msg())
    print(tabulate(table, headers, tablefmt="simple_grid"))
