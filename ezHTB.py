import os
import sys
import socket
import argparse
import subprocess
import shutil
from multiprocessing import Process
from pathlib import Path

# Tools output structure
OUTPUT_DIR = "/ezHTB/"
OUTPUT_NMAP = "/nmap.txt"
OUTPUT_GOBUSTER = "/gobuster.txt"
OUTPUT_NIKTO = "/nikto.txt"
OUTPUT_ENUM4LINUX = "/enum4linux.txt"

# Reverse shells for reverse() function
OUTPUT_PHP = "/php-reverse-shell.php"
OUTPUT_BASH = "/bash_reverse_shell.sh"
OUTPUT_POWERSHELL = "/powershell_reverse_shell.ps1"
OUTPUT_NC = "/nc_reverse_shell.txt"

# Gobuster wordlists
DIR_COMMON = "/root/Desktop/HackTheBox/common_dir.txt"
DIR_SMALL = "/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt"
DIR_MEDIUM = "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt"

# Append to /etc/hosts
APPEND_HOSTS = True

# Tools binaries
NMAP_BIN_LOC = "/usr/bin/nmap"
GOBUSTER_BIN_LOC = "/usr/bin/gobuster"
NIKTO_BIN_LOC = "/usr/bin/nikto"


def init(args):
    """
    This function initialize the directories path for the each tool that is being used.
    :param args: which args did the user choose
    """
    if args.hostname is not None:
        f = Path(os.path.join(os.getcwd()) + OUTPUT_DIR + args.hostname)
        try:
            f.mkdir()
        except FileExistsError as skip:
            print("|-| Skipping: directory already exists")

    if args.hostname is None:
        f = Path(os.path.join(os.getcwd()) + OUTPUT_DIR)
        try:
            f.mkdir()
        except FileExistsError as skip:
            print("|-| Skipping: directory already exists")

    if args.nmap is not None:
        init_handle(args.hostname, OUTPUT_NMAP)

    if args.gobuster is not None:
        init_handle(args.hostname, OUTPUT_GOBUSTER)

    if args.nikto:
        init_handle(args.hostname, OUTPUT_NIKTO)

    if args.enum4linux:
        init_handle(args.hostname, OUTPUT_ENUM4LINUX)


def init_handle(box_name, output_type):
    """
    This function handles the creating of each tool structure files. If there is a hostname the structure file will be
    ~/ezHTB/{hostname}/{tool_name.txt}, if not it will be like ~/ezHTB/{tool_name.txt}.
    :param box_name: whether the user choose a box name or not
    :param output_type: the tool output format
    """
    if box_name is None:
        f = Path(os.path.join(os.getcwd()) + OUTPUT_DIR + output_type)
        if not os.path.exists(os.path.dirname(f)):
            try:
                os.makedirs(os.path.dirname(f))
            except OSError as skip:
                if skip.errno != errno.EEXIST:
                    raise
                print("|-| Skipping: file already exists")
    elif box_name is not None:
        f = Path(os.path.join(os.getcwd()) + OUTPUT_DIR + box_name + output_type)
        if not os.path.exists(os.path.dirname(f)):
            try:
                os.makedirs(os.path.dirname(f))
            except OSError as skip:
                if skip.errno != errno.EEXIST:
                    raise
                print("|-| Skipping: file already exists")

def etc_hosts(hostname, ip_address):
    """
    This function will add the box name with a format of {box_name}.htb and its ip address to the /etc/hosts
    so that it can be accessed via hostname.
    :param hostname: the name of the target hostname
    :param ip_address: the ip of the target
    """
    IN_THERE = False
    if APPEND_HOSTS:
        try:
            with open("/etc/hosts", "r") as f:
                for line in f:
                    line = line.split()
                    if line:
                        if line[0] == ip_address:
                            IN_THERE = True
                            break
            with open("/etc/hosts", "a") as f:
                if IN_THERE:
                    print("|-| The ip address is already in the /etc/hosts ")
                else:
                    f.write("\n" + box_ip_address + "\t" + box_name.lower() + ".htb ")
        except PermissionError as skip:
            print("|-| Insufficient permissions: could not write to /etc/hosts")


def reverse(args):

    php = "php" in args.reverse
    bash = "bash" in args.reverse
    powershell = "powershell" in args.reverse
    nc = "nc" in args.reverse

    if args.reverse is None or args.port is None or args.ip is None:
        print("incomplete reverse shell parameters")
        exit(1)
    if php and args.port is not None and args.ip is not None:
        if args.out is not None:
            php_path = os.path.join(os.getcwd() + f"/{args.out}")
            dir_path = os.path.join(os.getcwd() + f"/Files{OUTPUT_PHP}")
            path = Path(dir_path)
            new_path = Path(php_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            new_path.write_text(text)
        else:
            php_path = os.path.join(os.getcwd() + f"{OUTPUT_PHP}")
            dir_path = os.path.join(os.getcwd() + f"{OUTPUT_PHP}")
            path = Path(dir_path)
            new_path = Path(php_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            new_path.write_text(text)
    if bash and args.port is not None and args.ip is not None:
        if args.out is not None:
            php_path = os.path.join(os.getcwd() + f"/{args.out}")
            dir_path = os.path.join(os.getcwd() + f"{OUTPUT_BASH}")
            path = Path(dir_path)
            new_path = Path(php_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            new_path.write_text(text)
        else:
            dir_path = os.path.join(os.getcwd() + f"/Files{OUTPUT_BASH}")
            path = Path(dir_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            print(text)
    if powershell and args.port is not None and args.ip is not None:
        if args.out is not None:
            php_path = os.path.join(os.getcwd() + f"/{args.out}")
            dir_path = os.path.join(os.getcwd() + f"/Files{OUTPUT_POWERSHELL}")
            path = Path(dir_path)
            new_path = Path(php_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            new_path.write_text(text)
        else:
            dir_path = os.path.join(os.getcwd() + f"/Files{OUTPUT_POWERSHELL}")
            path = Path(dir_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            print(text)
    if nc and args.port is not None and args.ip is not None:
        if args.out is not None:
            php_path = os.path.join(os.getcwd() + f"/{args.out}")
            dir_path = os.path.join(os.getcwd() + f"/Files{OUTPUT_NC}")
            path = Path(dir_path)
            new_path = Path(php_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            new_path.write_text(text)
        else:
            dir_path = os.path.join(os.getcwd() + f"/Files{OUTPUT_NC}")
            path = Path(dir_path)
            text = path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            print(text)
    if args.reverse is not None and not php and not bash and not powershell and not nc:
        print("invalid reverse shell type")

    exit(1)


def start_nmap(box_name, box_ip_address, quick, maximum):
    """
    This function handle nmap it start it and check for which parameter does the user provide and then
    it execute that command. print nmap scan completed when it finish
    :param box_name: the name of the box
    :param box_ip_address: the ip of the box
    :param quick: does a quick nmap scan with -q or --quick
    :param maximum: does nmap scan for all the ports with -c or --all
    """
    try:
        output = OUTPUT_DIR + box_name + OUTPUT_NMAP

        if quick:
            subprocess.call([NMAP_BIN_LOC, "-Pn", "-sV", "-oN", output, box_ip_address], stdout=subprocess.DEVNULL)
        elif maximum:
            subprocess.call([NMAP_BIN_LOC, "-T4", "-A", "-p", "1-65535", "-oN", output, box_ip_address],
                            stdout=subprocess.DEVNULL)
        else:
            subprocess.call([NMAP_BIN_LOC, "-sC", "-sV", "-oN", output, box_ip_address], stdout=subprocess.DEVNULL)
        print("|+| Nmap scan complete")
    except Exception as skip:
        print("|-| Failed to initiate nmap")
        print(skip)


def start_gobuster(box_name, box_ip_address, wordlist, force_https):
    """
    This function runs gobuster with a wordlist chosen based on the parameter that the user provides.
    :param box_name: the name of the box
    :param box_ip_address: the ip address of the box
    :param wordlist: the word list for gobuster to use
    :param force_https: boolean true if the user wants https, false otherwise
    :return:
    """
    url = "http://"
    if force_https:
        url = "https://"

    try:
        output = OUTPUT_DIR + box_name + OUTPUT_GOBUSTER
        subprocess.call([GOBUSTER_BIN_LOC, "dir", "-w", wordlist, "-z", "-q", "-x", ".php", "-o", output, "-u", url
                         + box_ip_address], stdout=subprocess.DEVNULL)
        print("|+| Gobuster scan complete")
    except Exception as skip:
        print("|-| Failed to initiate gobuster")
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


def arg_parser():

    parser = argparse.ArgumentParser(prog='ezHTB.py', usage='%(prog)s [options]')
    options = parser.add_argument_group('options', '')
    options.add_argument('-H', '--hostname', nargs=1,
                         help='box name: used to create the directory structure and an entry in /etc/hosts')
    options.add_argument('-i', '--ip', action='store', help='box ip address: target ip address')
    options.add_argument('-p', '--port', action='store', help='box port: host port')
    options.add_argument('-R', '--reverse', nargs='+',
                         help='creating a reverse shell based on the choose of the user')
    options.add_argument('-G', '--gobuster', action='store',
                         help='..')
    options.add_argument('-n', '--nmap', action='store',
                         help='..')
    options.add_argument('-E', '--enum4linux', action='store_true',
                         help='..')
    options.add_argument('-N', '--nikto', action='store_true',
                         help='..')
    options.add_argument('-o', '--out', action='store', help='Output file name')
    options.add_argument('-x', '--https', action='store_true', help='force https')
    args = parser.parse_args()
    return args


def main():
    """
    The main function which takes the input from the user and then run the correct nmap scan regarding
    to the input.
    """

    args = arg_parser()
    print(args)

    if args.reverse is not None:
        reverse(args)

    print("|+| Creating directories")
    init(args)

    if args.hostname is not None:
        print("|+| Creating /etc/hosts entry")
        etc_hosts(args.hostname, args.ip)

    if args.nmap is not None:
        print("|+| Starting nmap")
        nmap = Process(target=start_nmap, args=(args.hostname, args.ip, args.nmap))
        nmap.start()


    print("|+| Starting gobuster")
    if args.quick:
        if check_port(args.box_ip_address, 80) and not args.https or \
                check_port(args.box_ip_address, 443) and args.https:
            gobuster = Process(target=start_gobuster,
                               args=(args.box_name, args.box_ip_address, DIR_SMALL, args.https))
            gobuster.start()
        else:
            print("|-| Failed to start Gobuster: ports closed")
    elif args.maximum:
        if check_port(args.box_ip_address, 80) and not args.https or \
                check_port(args.box_ip_address, 443) and args.https:
            gobuster = Process(target=start_gobuster,
                               args=(args.box_name, args.box_ip_address, DIR_MEDIUM, args.https))
            gobuster.start()
        else:
            print("|-| Failed to start Gobuster: ports closed")
    else:
        if check_port(args.box_ip_address, 80) and not args.https \
                or check_port(args.box_ip_address, 443) and args.https:
            gobuster = Process(target=start_gobuster,
                               args=(args.box_name, args.box_ip_address, DIR_COMMON, args.https))
            gobuster.start()
        else:
            print("|-| Failed to start Gobuster: ports closed")

    nmap.join()
    gobuster.join()

    print("|*| All scans complete.")


if __name__ == "__main__":
    main()

