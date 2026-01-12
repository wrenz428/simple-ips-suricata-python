import json
import subprocess
import time

LOG_FILE = "/var/log/suricata/eve.json"
blocked_ips = set()

def block_ip(ip):
    if ip not in blocked_ips:
        print(f"[+] Blocking IP: {ip}")
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        blocked_ips.add(ip)

with open(LOG_FILE, "r") as f:
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(1)
            continue

        event = json.loads(line)

        if event.get("event_type") == "alert":
            src_ip = event.get("src_ip")
            alert_msg = event["alert"]["signature"]
            print(f"[!] Alert detected: {alert_msg} from {src_ip}")
            block_ip(src_ip)
