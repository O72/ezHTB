import os
import sys
import socket
import argparse
import subprocess
from multiprocessing import Process

OUTPUT_DIR = "/root/Desktop/test/"
# OUTPUT_DIR = "/root/Desktop/HackTheBox/"
OUTPUT_NMAP = "/nmap.txt"
APPEND_HOSTS = True
NMAP_BIN_LOC = "/usr/bin/nmap"


def init(box_name):
    """
    This function initialize the directory path for the target box following the /root/Desktop/HackTheBox/{box_name}
    format, and the supported tools for now nmap. Their format will be {tool_name}.txt inside
    the ~/HackTheBox/{box_name}/ directory
    :param box_name: the name of the box
    """
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
            print("|-| Skipping: file already exists")


def etc_hosts(box_name, box_ip_address):
    """
    This function will add the box name with a format of {box_name}.htb and its ip address to the /etc/hosts
    so that it can be accessed via hostname.
    :param box_name: the name of the box
    :param box_ip_address: the ip of the box
    """
    if APPEND_HOSTS:
        try:
            with open("/etc/hosts", "a") as f:
                f.write("\n" + box_ip_address + "\t" + box_name.lower() + ".htb ")

        except PermissionError as skip:
            print("|-| Insufficient permissions: could not write to /etc/hosts")


def launch_nmap(box_name, box_ip_address, quick, all_):
    """
    This function handle nmap it start it and check for which parameter does the user provide and then
    it execute that command. print nmap scan completed when it finish
    :param box_name: the name of the box
    :param box_ip_address: the ip of the box
    :param quick: does a quick nmap scan with -q or --quick
    :param all_: does nmap scan for all the ports with -c or --all
    """
    try:
        output = OUTPUT_DIR + box_name + OUTPUT_DIR_NMAP

        if quick:
            subprocess.call([NMAP_BIN_LOC, "-Pn", "-sV", "-oN", output, box_ip_address], stdout=subprocess.DEVNULL)
        elif all_:
            subprocess.call([NMAP_BIN_LOC, "-T4", "-A", "-p", "1-65535", "-oN", output, box_ip_address],
                            stdout=subprocess.DEVNULL)
        else:
            subprocess.call([NMAP_BIN_LOC, "-sC", "-sV", "-oN", output, box_ip_address], stdout=subprocess.DEVNULL)
        print("|+| nmap scan complete")
    except Exception as skip:
        print("|-| Failed to initiate nmap")
        print(skip)


def check_port(box_ip_address, port):
    """
    This function check if the box has http/80 or https/443 up and return the result.
    :param box_ip_address: the ip of the box
    :param port: to check for port 80 and 443
    :return: true if there is a site on that port, false otherwise.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    respond = sock.connect_ex((box_ip_address, port))
    if respond == 0:
        return True
    else:
        return False


def main(args):
    """
    The main function which takes the input from the user and then run the correct nmap scan regarding
    to the input.
    :param args: the argument from the user.
    """
    print("|+| creating directories")
    init(args.box_name)

    print("|+| creating /etc/hosts entry")
    etc_hosts(args.box_name, args.box_ip_address)

    print("|+| starting nmap")
    nmap = Process(target=launch_nmap, args=(args.box_name, args.box_ip_address, args.quick, args.all))

    nmap.start()
    nmap.join()

    print("nmap scan complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ezHTB', usage='ezHTB.py [options] box_name box_ip_address')
    parser.add_argument('box_name', metavar='box_name', type=str,
                        help='box name: used to create the directory structure')
    parser.add_argument('box_ip_address', metavar='box_ip_address', type=str, help='box_ip_address: target ip address')
    parser.add_argument('-q', '--quick', action='store_true',
                        help='determine scan parameters: nmap -Pn -sV')
    parser.add_argument('-c', '--all', action='store_true',
                        help='determine scan parameters: nmap -T4 -A -p 1-65535')
    args = parser.parse_args()
    main(args)
