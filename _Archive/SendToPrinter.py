import subprocess
import platform

def print_file(filepath, printer_name):
    os_type = platform.system()

    if os_type == "Windows":
        # Uses PowerShell to print to a named printer
        subprocess.run([
            "powershell", "-Command",
            f'Get-Content "{filepath}" | Out-Printer -Name "{printer_name}"'
        ], check=True)

    elif os_type == "Linux":
        # Uses CUPS lp command
        subprocess.run([
            "lp", "-d", printer_name, filepath
        ], check=True)

    else:
        raise OSError(f"Unsupported OS: {os_type}")

# Usage
print_file(r"C:\temp\Test.txt", "EPSON TM-T88V Receipt")
#EPSON TM-T88V Receipt"