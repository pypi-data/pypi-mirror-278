import psutil
import GPUtil
import uptime
import os
import time
from datetime import timedelta
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.box import ROUNDED

console = Console()


def get_cpu_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"{cpu_usage}%"


def get_memory_info():
    memory = psutil.virtual_memory()
    return f"{memory.percent}% (Used: {memory.used / (1024 ** 3):.2f}GB, Total: {memory.total / (1024 ** 3):.2f}GB)"


def get_disk_info():
    disk = psutil.disk_usage('/')
    return f"{disk.percent}% (Used: {disk.used / (1024 ** 3):.2f}GB, Total: {disk.total / (1024 ** 3):.2f}GB)"


def get_uptime():
    system_uptime = timedelta(seconds=int(uptime.uptime()))
    return str(system_uptime)


def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "No GPU found."
    info = []
    for gpu in gpus:
        info.append(f"{gpu.name} - Memory Usage: {gpu.memoryUsed / gpu.memoryTotal *
                    100:.2f}% (Used: {gpu.memoryUsed}MB, Total: {gpu.memoryTotal}MB)")
    return "\n".join(info)


def get_system_info():
    info = {
        "OS": "Windows 11 Home Single Language [64-bit]",
        "Host": "LENOVO 82JU",
        "Kernel": "10.0.22631.0",
        "Motherboard": "LENOVO LNVNB161216",
        "Uptime": get_uptime(),
        "Packages": "27 (choco), 2 (scoop)",
        "Shell": "PowerShell v7.4.2",
        "Resolution": "1536x864",
        "Terminal": "Windows Terminal",
        "CPU": "AMD Ryzen 7 5800H with Radeon Graphics",
        "GPU": get_gpu_info(),
        "Memory": get_memory_info(),
        "Disk (C:)": get_disk_info(),
    }
    return info


def create_table(system_info):
    table = Table(
        title="System Information",
        title_style="bold magenta",
        box=ROUNDED,
        expand=True,
        show_edge=False,
        padding=(0, 1),
    )
    table.add_column("Component", style="cyan", no_wrap=True, justify="right")
    table.add_column("Details", style="white", justify="left")

    for key, value in system_info.items():
        table.add_row(key, value)

    return table


def display_system_info():
    with Live(auto_refresh=False) as live:
        while True:
            system_info = get_system_info()
            table = create_table(system_info)
            live.update(
                Panel(table, border_style="bold yellow", padding=(1, 2)))
            live.refresh()
            time.sleep(5)  # Update every 5 seconds


def main():
    display_system_info()


if __name__ == "__main__":
    main()
