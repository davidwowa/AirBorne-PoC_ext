# 2-poc-s-1-repository
poc for CVE-2025-24252 &amp; CVE-2025-24132

CVE-2025-24252: Heap overflow in AirPlayReceiver over mDNS (Bonjour). Triggerable via malformed TXT records.

CVE-2025-24132: Out-of-bounds write in AirPlayScreen component via crafted AirPlay pairing/init message.

**CVE-2025-24252**

Install scapy and avahi on Kali

sudo apt update

sudo apt install python3-scapy avahi-daemon -y

sudo systemctl start avahi-daemon

git clone https://github.com/ekomsSavior/2-PoCs-1-repository.git




