# 🌐 Network Automation Scripts 📡

## 🚀 Purpose 🚀 
Welcome to the **Network Automation Scripts Repository**, your go-to collection for automating network switch management and configurations. These scripts are specifically designed to simplify repetitive tasks, reduce manual errors, and improve efficiency in managing network devices. 🌟

### 💡 Current Focus: **Aruba CX Switches** 💡
The repository currently features scripts for managing **Aruba CX switches** (models 6100, 6200, 8320), with plans to expand support for other brands and devices. If you're a network engineer or enthusiast, this is your toolbox for automation! 🛠️

---

## 🛡️ Features 🛡️ 

### 🔧 **1. Interface Configuration Management**
- **Supported Commands:**
  - Apply or remove AAA security settings on specific interfaces.
  - Retrieve and display active interface configurations.
  - Save configurations directly to the device memory.

- **Use Case:**  
  Simplifies tasks like securing interfaces with AAA or auditing their configurations, providing quick, repeatable, and reliable results.

---

### 📋 **2. Show Running Configurations** 📋
- **Supported Commands:**
  - `show running-config interface <interface>`: Retrieve and display active configurations for specific interfaces.

- **Use Case:**  
  Ideal for troubleshooting or validating configurations on a switch without navigating complex command-line interfaces.

---

### 🔮 **Planned Features** 🔮
We're working on expanding the repository to include:
- **Advanced Configuration Management**: VLAN setups, QoS rules, and more for Aruba CX switches.
- **Multi-Vendor Support**: Scripts for devices from:
  - 🖧 **Cisco**
  - 📡 **Juniper**
  - 📟 **MikroTik**
  - 🔌 **Ubiquiti**
  - And more!

---

## 💻 How to Use 💻

### Prerequisites
- **Python 3.x** installed on your machine.
- Install required libraries:
  ```bash
  pip install paramiko

🌟 Why Use These Scripts? 🌟

✅ Save Time: Automate repetitive tasks with a few simple inputs.
✅ Improve Accuracy: Minimize human errors with standardized commands.
✅ Scale Easily: Configure multiple interfaces in one go, or adapt for new vendors.
✅ Learn and Grow: Use these scripts as a starting point to explore Python-based network automation.

⚠️ Disclaimer ⚠️

These scripts are tested with Aruba CX switches (models 6100, 6200, 8320). They may not work as expected on other brands or models.
Use responsibly and ensure you have appropriate permissions before making changes.
This repository was created with AI (ChatGPT) and extensively tested on supported devices.

🤝 Contributions Welcome!🤝 

Want to enhance these scripts or add support for other brands? Join us! 🌐

How to Contribute
Fork this repository.
Make your changes or add new scripts.
Submit a pull request with your contributions.
