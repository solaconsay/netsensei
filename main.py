# server.py
from mcp.server.fastmcp import FastMCP
import subprocess
import platform
import shlex
from netmiko import ConnectHandler

# Create an MCP server
mcp = FastMCP("NetSensei")


@mcp.tool()
def ping_ip(ip_address) -> str:
    """
    Pings the specified IP address once and returns the result as a string.

    Args:
        ip_address (str): The target IP address to ping.

    Returns:
        str: The full output from the ping command (success or error).
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip_address]

    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True
        )
        return output  # Successful ping, returning the full result
    except subprocess.CalledProcessError as e:
        return e.output  # Failed ping, return the error output


@mcp.tool()
def traceroute_ip(ip_address) -> str:
    """
    Performs a traceroute to the specified IP address and returns the result.
    """
    if platform.system().lower() == "windows":
        command = ["tracert", ip_address]
    else:
        command = ["traceroute", ip_address]

    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True
        )
        return output
    except subprocess.CalledProcessError as e:
        return e.output


@mcp.tool()
def nmap_scan(target: str, custom_args: str = "") -> str:
    """
    Performs a flexible Nmap scan with optional custom arguments.

    Args:
        target (str): IP or subnet to scan.
        custom_args (str): Optional Nmap arguments (e.g., '-T4').

    Returns:
        dict: Parsed scan result.
    """
    args = custom_args.strip() or "-T4"
    command = ["nmap"] + shlex.split(args) + [target]

    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True
        )
        return output  # Return the scan results as a string
    except subprocess.CalledProcessError as e:
        return e.output  # Capture any errors from nmap


@mcp.tool()
def list_interfaces() -> str:
    """
    Lists all available network interfaces using tshark.

    Returns:
        str: A list of interfaces with their indexes and descriptions.
    """
    try:
        command = ["tshark", "-D"]
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True
        )
        return output

    except subprocess.CalledProcessError as e:
        return f"Error listing interfaces: {e.output.strip()}"

    except FileNotFoundError:
        return "Error: tshark not found. Make sure it is installed and added to your system PATH."


@mcp.tool()
def packet_sniffer(
    interface: int = 7, packet_count: int = 10, filter_expr: str = ""
) -> str:
    """
    Uses tshark to sniff packets on a specific network interface using display filters only.

    Args:
        interface (int): The interface number to use for sniffing.
        packet_count (int): Number of packets to capture.
        filter_expr (str): A display filter (e.g., 'dns', 'http', 'icmp'). This is optional only. The default is "".

    Returns:
        str: Captured packet output.
    """
    try:
        command = ["tshark", "-i", str(interface), "-c", str(packet_count)]

        if filter_expr:
            command += ["-Y", filter_expr]

        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True
        )

        return output

    except subprocess.CalledProcessError as e:
        return f"Sniffer error: {e.output.strip()}"

    except FileNotFoundError:
        return "Error: tshark not found. Make sure it is installed and added to your system PATH."


@mcp.tool()
def use_ssh(
    device_type: str, ip: str, username: str, password: str, command: str
) -> str:
    """
    Executes a command on a remote network device using Netmiko.

    Args:
        device_type (str): Type of the device (e.g., 'cisco_ios', 'juniper', 'linux', etc.).
        ip (str): IP address of the network device.
        username (str): SSH username.
        password (str): SSH password.
        command (str): The command to run on the device.

    Returns:
        str: Command output or an error message.
    """
    try:
        device = {
            "device_type": device_type,
            "ip": ip,
            "username": username,
            "password": password,
        }

        connection = ConnectHandler(**device)
        output = connection.send_command(command)
        connection.disconnect()
        return output

    except Exception as e:
        return f"[!] Failed to run command: {str(e)}"
