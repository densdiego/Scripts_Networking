import paramiko
import getpass
import time
import unicodedata

def normalize_text(text):
    """Removes accents and converts text to lowercase."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.lower()

def connect_to_switch(ip, username, password):
    """Establishes an SSH connection to the switch."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password)
        return client
    except Exception as e:
        print(f"Error connecting to the switch: {e}")
        return None

def execute_command(client, command):
    """Executes a command on the switch and returns the full output."""
    shell = client.invoke_shell()
    shell.send(command + "\n")
    time.sleep(2)  # Wait for the command to process
    output = ""
    while shell.recv_ready():
        output += shell.recv(65535).decode('utf-8')
        time.sleep(0.5)
    return output.strip()

def filter_configuration(output, interface):
    """Filters the output to show only the configuration of the selected interface."""
    configurations = output.splitlines()
    start = False
    interface_config = []

    for line in configurations:
        if f"interface {interface}" in line:
            start = True
        if start:
            interface_config.append(line)
            if line.strip() == "exit":  # Stop capturing at 'exit'
                break

    return "\n".join(interface_config)

def display_interface_configuration(client, interface):
    """Displays the active configuration of a specific interface."""
    command = f"show running-config interface {interface}"
    output = execute_command(client, command)
    filtered_config = filter_configuration(output, interface)
    print(f"\nActive configuration for interface {interface}:\n")
    print(filtered_config)

def configure_interface(client, interface, action):
    """Applies or removes security configurations on a specified interface."""
    shell = client.invoke_shell()
    shell.send("configure terminal\n")
    time.sleep(1)

    shell.send(f"interface {interface}\n")
    time.sleep(1)

    if action == "add":
        commands = [
            "aaa authentication port-access client-limit 2",
            "aaa authentication port-access dot1x authenticator",
            "eapol-timeout 30",
            "max-eapol-requests 1",
            "max-retries 1",
            "reauth",
            "enable",
            "aaa authentication port-access mac-auth",
            "cached-reauth",
            "cached-reauth-period 86400",
            "quiet-period 30",
            "enable"
        ]
    elif action == "remove":
        commands = [
            "no aaa authentication port-access client-limit 2",
            "no aaa authentication port-access dot1x authenticator",
            "no aaa authentication port-access mac-auth"
        ]
    else:
        print("Invalid action. Choose 'add' or 'remove'.")
        shell.send("exit\n")
        time.sleep(1)
        return

    # Execute commands in the interface context
    for cmd in commands:
        shell.send(cmd + "\n")
        time.sleep(1)

    # Exit interface context and configuration mode
    shell.send("exit\n")
    time.sleep(1)
    shell.send("exit\n")
    time.sleep(1)

def parse_interfaces(input_string):
    """Parses interfaces entered as a range or comma-separated list."""
    interfaces = []
    for item in input_string.split(","):
        if "-" in item:
            start, end = item.split("-")
            base_start, num_start = start.rsplit("/", 1)
            base_end, num_end = end.rsplit("/", 1)
            if base_start == base_end:
                for i in range(int(num_start), int(num_end) + 1):
                    interfaces.append(f"{base_start}/{i}")
            else:
                print(f"Invalid range: {item}")
        else:
            interfaces.append(item.strip())
    return interfaces

def save_configuration(client):
    """Saves the configuration to memory."""
    output = execute_command(client, "write memory")
    print("Configuration saved successfully.")
    return output

def main():
    print("=== Aruba Switch Configuration ===")
    ip = input("Enter the switch IP address: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    client = connect_to_switch(ip, username, password)
    if client is None:
        return

    while True:
        input_string = input("Enter the interfaces to configure (e.g., 1/1/1-1/1/4 or 1/1/1,1/1/3,1/1/5): ")
        interfaces = parse_interfaces(input_string)

        action = input("Do you want to add or remove security? (add/remove): ").lower()
        if action not in ["add", "remove"]:
            print("Invalid action. Please try again.")
            continue

        for interface in interfaces:
            print(f"\nConfiguring interface {interface}...\n")
            configure_interface(client, interface, action)
            display_interface_configuration(client, interface)

        save_configuration(client)

        another = input("Do you want to configure more interfaces? (yes/no): ")
        if normalize_text(another) != "yes":
            break

    client.close()
    print("Session closed.")

if __name__ == "__main__":
    main()
