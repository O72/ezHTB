import os
import sys
import socket
import argparse
import subprocess
from multiprocessing import Process


OUTPUT_DIR = "/root/Desktop/test/"
OUTPUT_DIR_NMAP = "/nmap.txt"
APPEND_HOSTS = True

NMAP_BIN_LOC = "/usr/bin/nmap"


def initialize(box_name):
    f = Path(OUTPUT_DIR + box_name)
    try:
        f.mkdir()
    except FileExistsError as skip:
        print("|-| Skipping: directory already exists")

    f = Path(OUTPUT_DIR + box_name + OUTPUT_DIR_NMAP)
    if not os.path.exists(os.path.dirname(f)):
        try:
            os.makedirs(os.path.dirname(f))
        except OSError as skip:
            if skip.errno != errno.EEXIST:
                raise
            print("|-| Skipping:directory already exists")


def configure_hosts(box_name, box_ip_address):
    if APPEND_HOSTS:
        try:
            with open("/etc/hosts", "a") as f:
                f.write("\n" + box_ip_address + "\t" + box_name.lower() + ".htb ")

        except PermissionError as skip:
            print("|-| Insufficient permissions: could not write to /etc/hosts")


def launch_nmap(box_name, box_ip_address, quick, all_):
    try:
        output = OUTPUT_DIR + box_name + OUTPUT_DIR_NMAP

        if quick:
            subprocess.call([NMAP_BIN_LOC, "-Pn", "-sV", "-oN", output, box_ip_address], stdout=subprocess.DEVNULL)
        elif all_:
            subprocess.call([NMAP_BIN_LOC, "-T4", "-A", "-p", "1-65535", "-oN", output, box_ip_address], stdout=subprocess.DEVNULL)
        else:
            subprocess.call([NMAP_BIN_LOC, "-sC", "-sV", "-oN", output, box_ip_address], stdout=subprocess.DEVNULL)
        print("|+| nmap scan complete")
    except Exception as skip:
        print("|-| Failed to initiate nmap")
        print(skip)


def check_port(box_ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    respond = sock.connect_ex((box_ip_address, port))
    if respond == 0:
        return True
    else:
        return False


def main(args):

    print("|+| creating directories")
    initialize(args.box_name)

    print("|+| creating /etc/hosts entry")
    configure_hosts(args.box_name, args.box_ip_address)

    print("|+| starting nmap")
    nmap = Process(target=launch_nmap, args=(args.box_name, args.box_ip_address, args.quick, args.all))

    nmap.start()
    nmap.join()

    print("nmap scan complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ezHTB', usage='ezHTB.py [options] box_name box_ip_address')
    parser.add_argument('box_name', metavar='box_name', type=str,
                        help='box name: used to create the directory structure')
    parser.add_argument('box_ip_address', metavar='box_ip_address', type=str, help='target ip address')
    parser.add_argument('-q', '--quick', action='store_true',
                        help='determine scan parameters: nmap -Pn -sV')
    parser.add_argument('-c', '--all', action='store_true',
                        help='determine scan parameters: nmap -T4 -A -p 1-65535')
    args = parser.parse_args()
    main(args)

