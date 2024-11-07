from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
import psutil
import time
import random
import platform
from datetime import datetime, timedelta

console = Console()

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    uptime = timedelta(seconds=int(time.time() - psutil.boot_time()))
    
    # Informações sobre o processo que mais consome CPU
    processes = [(p.info["cpu_percent"], p.info["name"]) for p in psutil.process_iter(['name', 'cpu_percent'])]
    top_process = max(processes, key=lambda p: p[0]) if processes else ("N/A", "N/A")
    
    # Informação da bateria (se disponível)
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "N/A"
    battery_plugged = battery.power_plugged if battery else "N/A"
    
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory.percent,
        "memory_used": memory.used / (1024 ** 2),
        "memory_total": memory.total / (1024 ** 2),
        "disk_usage": disk.percent,
        "disk_used": disk.used / (1024 ** 2),
        "disk_total": disk.total / (1024 ** 2),
        "network_sent": net.bytes_sent / (1024 ** 2),
        "network_recv": net.bytes_recv / (1024 ** 2),
        "uptime": str(uptime),
        "top_process": top_process,
        "battery_percent": battery_percent,
        "battery_plugged": battery_plugged,
    }

def render_panel():
    info = get_system_info()

    # ASCII Art Title
    console.print("[bold green]Dark Net System Monitor[/bold green]", style="green on black")
    console.print("=" * 50, style="green")

    # Barra de Progresso Personalizada
    progress_cpu = Progress(
        TextColumn("[bold red]CPU:"),
        BarColumn(bar_width=20, style="red"),
        TextColumn("[bold red]{task.percentage:.0f}%")
    )

    progress_memory = Progress(
        TextColumn("[bold blue]Memória:"),
        BarColumn(bar_width=20, style="blue"),
        TextColumn("[bold blue]{task.percentage:.0f}%")
    )

    progress_disk = Progress(
        TextColumn("[bold green]Disco:"),
        BarColumn(bar_width=20, style="green"),
        TextColumn("[bold green]{task.percentage:.0f}%")
    )

    # Adiciona as Tarefas de Monitoramento
    progress_cpu.add_task("CPU", total=100, completed=info["cpu_usage"])
    progress_memory.add_task("Memória", total=100, completed=info["memory_usage"])
    progress_disk.add_task("Disco", total=100, completed=info["disk_usage"])

    # Tabela com Infos Extras
    table = Table(border_style="bright_green")
    table.add_column("Descrição", justify="left", style="bold cyan")
    table.add_column("Valor", justify="right", style="yellow")

    table.add_row("CPU Uso", f"{info['cpu_usage']}%")
    table.add_row("Memória Usada", f"{info['memory_used']:.2f} MB / {info['memory_total']:.2f} MB")
    table.add_row("Disco Usado", f"{info['disk_used']:.2f} MB / {info['disk_total']:.2f} MB")
    table.add_row("Rede Enviada", f"{info['network_sent']:.2f} MB")
    table.add_row("Rede Recebida", f"{info['network_recv']:.2f} MB")
    table.add_row("Tempo de Atividade", f"{info['uptime']}")
    table.add_row("Processo Mais Ativo", f"{info['top_process'][1]} ({info['top_process'][0]:.2f}%)")
    table.add_row("Bateria", f"{info['battery_percent']}% {'(Plugada)' if info['battery_plugged'] else '(Desplugada)'}")

    # Exibe as Barras de Progresso e a Tabela
    console.clear()
    console.print(progress_cpu)
    console.print(progress_memory)
    console.print(progress_disk)
    console.print(table)

    # Simulação de Logs de Tráfego de Rede
    console.print("\n[bold green]Real-time Network Activity:[/bold green]", style="green")
    for _ in range(5):  # Exibe 5 logs de exemplo
        source_ip = f"192.168.1.{random.randint(1, 255)}"
        dest_ip = f"10.0.0.{random.randint(1, 255)}"
        data_amount = random.randint(1, 1000)
        log_line = f"[{time.strftime('%H:%M:%S')}] [green]{source_ip}[/green] -> [yellow]{dest_ip}[/yellow] : {data_amount} KB transferred"
        console.print(log_line)

while True:
    render_panel()
    time.sleep(1)

