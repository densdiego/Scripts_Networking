import paramiko
import getpass

def ssh_to_aruba_cx(ip, username, password):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the device
        print(f"Connecting to {ip}...")
        ssh.connect(ip, username=username, password=password)
        print("Connection established.\n")

        # Commands to execute in order
        commands = [
            "show interface brief",
            "show system",
            "show port-access clients",
            "show running-config"
        ]

        for command in commands:
            print(f"\nExecuting: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            
            # Read and display the output
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if output:
                print(f"Output:\n{output}")
            if error:
                print(f"Error:\n{error}")

        # Close the connection
        ssh.close()
        print("\nSession closed.")

    except Exception as e:
        print(f"Error connecting or executing the command: {e}")

if __name__ == "__main__":
    print("Program to manage Aruba CX switches")
    ip = input("Enter the IP of the device you want to connect to: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    ssh_to_aruba_cx(ip, username, password)

