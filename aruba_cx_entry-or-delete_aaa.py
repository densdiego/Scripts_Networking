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
    """Executes a command on the switch using exec_command and returns the full output."""
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(2)  # Allow time for the command to execute
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    if error:
        print(f"Error executing command '{command}': {error.strip()}")
    return output.strip()

def display_interface_configuration(client, iface):
    """Displays the active configuration of a specific interface."""
    command = f"show running-config interface {iface}"
    output = execute_command(client, command)
    
    if not output:
        print(f"No configuration found for interface {iface}.")
    else:
        print(f"\nActive configuration for interface {iface}:\n")
        print(output)

def configure_interface(client, iface, action):
    """Applies or removes security configurations on a specified interface."""
    shell = client.invoke_shell()
    shell.send("configure terminal\n")
    time.sleep(1)

    shell.send(f"interface {iface}\n")
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

        for iface in interfaces:
            print(f"\nConfiguring interface {iface}...\n")
            configure_interface(client, iface, action)
            print(f"\nVerifying configuration for interface {iface}...\n")
            display_interface_configuration(client, iface)

        save_configuration(client)

        another = input("Do you want to configure more interfaces? (yes/no): ")
        if normalize_text(another) != "yes":
            break

    client.close()
    print("Session closed.")

if __name__ == "__main__":
    main()
