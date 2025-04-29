#AIRBORNE 2-PoCs-1-repository
poc for CVE-2025-24252 &amp; CVE-2025-24132

**CVE-2025-24132 – AirPlay Pairing Exploit PoC**

This bug is in the AirPlayScreen component and can trigger a heap overflow by sending malformed handshake/init packets over TCP to port 7000 on the target device.**


**CVE-2025-24252: Heap overflow in AirPlayReceiver**

over mDNS (Bonjour). Triggerable via malformed TXT records.

-Install scapy and avahi on Kali

sudo apt update

sudo apt install python3-scapy avahi-daemon -y

sudo systemctl start avahi-daemon

git clone https://github.com/ekomsSavior/2-PoCs-1-repository.git




