# Aruba CX SSH Automation Script

## Purpose
This script is specifically designed to manage and audit **Aruba CX switches** via SSH. It allows network administrators to retrieve important information such as interface status, system details, connected clients, and the current running configuration. The script is tailored exclusively for **Aruba CX devices** and is not intended for use with other equipment.

## Features
- Securely connects to Aruba CX switches using SSH.
- Executes the following commands in sequence:
  - `show interface brief`: Displays a summary of the switch's interfaces.
  - `show system`: Provides system-level information about the device.
  - `show port-access clients`: Lists connected clients.
  - `show running-config`: Outputs the current running configuration of the device.
- Outputs both command results and potential errors for troubleshooting.

## Requirements
- **Python 3.x**
- **Paramiko** library for SSH communication (`pip install paramiko`).

## How to Use
1. Clone or download the script from this repository.
2. Run the script with Python:
   ```bash
   python script_name.py
