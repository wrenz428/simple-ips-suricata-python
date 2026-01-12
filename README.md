# simple-ips-suricata-python
Basic Intrusion Prevention System using Suricata and Python on Kali Linux

This project demonstrates a simple Intrusion Prevention System (IPS) implemented on Kali Linux using Suricata and Python. The purpose of the project is to detect repeated SSH connection attempts and automatically block the attacker using firewall rules.

Before starting, the Kali Linux system should be updated to the latest version to avoid compatibility issues. This can be done by running the following command:

sudo apt update && sudo apt upgrade -y

Suricata must be installed on the system. To install Suricata, run:

sudo apt install suricata -y

After installation, verify that Suricata is installed correctly by running:

suricata --version

Python 3 is required for the automation script. Python 3 is preinstalled on Kali Linux by default.

The virtual machine network must be configured correctly. The Kali Linux virtual machine should be set to use a Host‑Only Adapter in VirtualBox. Promiscuous mode should be set to Allow All and the cable connected option should be enabled. This allows the Kali machine and the Windows host machine to communicate on the same network.

The IP address of the Kali IPS machine must be identified. Run the following command on Kali Linux:

ip a

Note the IP address assigned to the active interface. This IP address will be used as the scan target during testing.

Network connectivity should be tested from the Windows host machine. Open Command Prompt on Windows and run:

ping <KALI_IP_ADDRESS>

If the ping is successful, the network is configured correctly.

Suricata uses rule files to detect malicious activity. Custom rules are stored in the directory /etc/suricata/rules/. Ensure that a file named local.rules exists in this directory. If it does not exist, create it.

Edit the Suricata configuration file using:

sudo nano /etc/suricata/suricata.yaml

Ensure that the default rule path is set to /etc/suricata/rules and that local.rules is included in the rule files section. This allows Suricata to load the custom rules.

The SSH service must be running on the Kali IPS machine to generate traffic on port 22. Start and enable the SSH service using:

sudo systemctl start ssh
sudo systemctl enable ssh

Verify that the service is running by using:

sudo systemctl status ssh

Extract the project files and navigate to the project directory using:

cd IPS_Project

The project directory contains the Python script ips.py and a shell script run_suricata.sh.

Before running the shell script, it must be made executable. Run the following command from inside the IPS_Project directory:

chmod +x run_suricata.sh

Suricata can now be started using the script or directly from the terminal. To start Suricata manually, run:

sudo suricata -i eth0

Ensure that the interface name matches the interface associated with the Kali IP address.

To monitor Suricata alerts in real time, open a new terminal and run:

sudo tail -f /var/log/suricata/fast.log

The Python script is responsible for monitoring Suricata alerts and blocking attacker IP addresses using iptables. The script must be run with root privileges because firewall rules require administrative access. From the IPS_Project directory, run:

sudo python3 ips.py

To test the IPS, a safe simulated brute‑force attack can be performed from the Windows host machine using Nmap or Zenmap. Run the following command, replacing the IP address with the Kali IPS machine’s IP:

nmap -p 22 --min-rate 20 --max-retries 10 <KALI_IP_ADDRESS>

This command sends repeated SSH connection attempts without attempting real password authentication.

If the system is working correctly, Suricata will log an alert in fast.log indicating a possible SSH brute‑force attempt. The Python script will detect the alert and apply an iptables rule to block the attacker’s IP address.

Firewall rules can be verified by running the following command on Kali Linux:

sudo iptables -L -n

A DROP rule for the attacker’s IP address should be visible. After the IP is blocked, Nmap scans from the attacker machine will show port 22 as filtered.

If needed, firewall rules can be cleared using:

sudo iptables -F

This completes the setup and demonstration of the Intrusion Prevention System.
