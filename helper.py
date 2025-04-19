from netmiko import ConnectHandler
import argparse


def run_network_command(
    device_type: str, ip: str, username: str, password: str, command: str
) -> str:
    """
    Executes a command on a remote network device using Netmiko.
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run command on network device via SSH"
    )
    parser.add_argument(
        "--device_type", required=True, help="Device type (e.g., cisco_ios)"
    )
    parser.add_argument("--ip", required=True, help="IP address of the device")
    parser.add_argument("--username", required=True, help="SSH username")
    parser.add_argument("--password", required=True, help="SSH password")
    parser.add_argument("--command", required=True, help="Command to run")

    args = parser.parse_args()

    result = run_network_command(
        args.device_type, args.ip, args.username, args.password, args.command
    )

    print(result)
