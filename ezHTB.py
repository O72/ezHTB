#!/usr/bin/env python3
__author__ = "Omar Aljaloud (O72)"
__license__ = "MIT"
__version__ = "0.1"
__email__ = "oaa3024@rit.edu"
__status__ = "Under Development"

import os
import sys
import socket
import argparse
import subprocess
import shutil
import random
import re
from multiprocessing import Process
from pathlib import Path

# Tools output structure
ezHTB = "/ezHTB_Results"
OUTPUT_DIR = Path(os.path.join(os.getcwd() + ezHTB))  # ~/ezHTB
OUTPUT_NMAP = "/nmap.txt"
OUTPUT_GOBUSTER = "/gobuster.txt"
OUTPUT_NIKTO = "/nikto.txt"
OUTPUT_ENUM4LINUX = "/enum4linux.txt"

# Reverse shells for reverse() function
OUTPUT_PHP = "/php_reverse_shell.php"
OUTPUT_BASH = "/bash_reverse_shell.sh"
OUTPUT_POWERSHELL = "/powershell_reverse_shell.ps1"
OUTPUT_NC = "/nc_reverse_shell.txt"

# Gobuster wordlists
DIR_COMMON = "Files/common_dir.txt"
DIR_SMALL = "/usr/share/dirbuster/wordlists/directory-list-2.3-small.txt"
DIR_MEDIUM = "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt"

# Append to /etc/hosts
APPEND_HOSTS = True

# Tools binaries
NMAP_BIN_LOC = "/usr/bin/nmap"
GOBUSTER_BIN_LOC = "/usr/bin/gobuster"
NIKTO_BIN_LOC = "/usr/bin/nikto"
ENUM4LINUX_BIN_LOC = "/usr/bin/enum4linux"


def init(args):
    """
    This function initialize the directories path for the each tool that is being used.
    :param args: which args did the user choose
    """
    if args.hostname is not None:
        f = Path(os.path.join(os.getcwd() + ezHTB + args.hostname))
        try:
            f.mkdir()
        except FileExistsError as skip:
            print(f"|-| Skipping: {f} directory already exists")

    if args.hostname is None:
        try:
            OUTPUT_DIR.mkdir()
        except FileExistsError as skip:
            print(f"|-| Skipping: {OUTPUT_DIR} directory already exists")

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
        f = os.path.join(os.getcwd() + ezHTB + output_type)
        if not os.path.exists(os.path.dirname(f)):
            try:
                os.makedirs(os.path.dirname(f))
            except OSError as skip:
                if skip.errno != errno.EEXIST:
                    raise
                print(f"|-| Skipping: {output_type} file already exists")
    elif box_name is not None:
        f = os.path.join(os.getcwd() + ezHTB + box_name + output_type)
        if not os.path.exists(os.path.dirname(f)):
            try:
                os.makedirs(os.path.dirname(f))
            except OSError as skip:
                if skip.errno != errno.EEXIST:
                    raise
                print(f"|-| Skipping: {output_type} file already exists")


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
                    f.write("\n" + ip_address + "\t" + hostname.lower() + ".htb ")
                    print(f"|*| The ip address {ip_address} and the hostname {hostname.lower}.htb "
                          f"has been added to /etc/hosts ")
        except PermissionError as skip:
            print("|-| Insufficient permissions: could not write to /etc/hosts")


def reverse(args):
    """
    This function created to get reverse shell of different kinds as fast as possible. Given a kind of reverse shell
    of the user needs between php, bash, powershell, nc, and the ip and port to replace in the reverse shell. It can
    either print or redirect it to a file using the -o flag
    :param args: reverse shell type, port, ip
    """
    php = "php" in args.reverse
    bash = "bash" in args.reverse
    powershell = "powershell" in args.reverse
    nc = "nc" in args.reverse

    if args.reverse is None or args.port is None or args.ip is None:
        print("|-| Incomplete reverse shell parameters")
        exit(1)
    if php and args.port is not None and args.ip is not None:
        if args.out is not None:
            type_path = os.path.join(os.getcwd() + ezHTB + f"/{args.out}")
            dir_path = Path(os.path.join(os.getcwd() + f"/Files{OUTPUT_PHP}"))
            new_path = Path(type_path)
            text = dir_path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            new_path.write_text(text)
            print(f"|+| php reverse shell has been created in {type_path}")
        else:
            php_path = os.path.join(os.getcwd() + ezHTB + f"{OUTPUT_PHP}")
            dir_path = Path(os.path.join(os.getcwd() + f"/Files{OUTPUT_PHP}"))
            new_path = Path(php_path)
            text = dir_path.read_text()
            text = text.replace("127.0.0.1", f"{args.ip}")
            text = text.replace("1234", f"{args.port}")
            new_path.write_text(text)
            print(f"|+| php reverse shell has been created in {php_path}")
    if bash and args.port is not None and args.ip is not None:
        reverse_handle(args.ip, args.port, args.out, OUTPUT_BASH, "bash")

    if powershell and args.port is not None and args.ip is not None:
        reverse_handle(args.ip, args.port, args.out, OUTPUT_POWERSHELL, "powershell")

    if nc and args.port is not None and args.ip is not None:
        reverse_handle(args.ip, args.port, args.out, OUTPUT_NC, "nc")

    if args.reverse is not None and not php and not bash and not powershell and not nc:
        print("|-| Invalid reverse shell type")

    exit(0)

def reverse_handle(ip, port, out_flag, output_type, reverse_type):
    """
    This function handle the condition of whether the user chose -o which will redirect the result to a file.
    :param ip: the ip address for the reverse shell to call back to
    :param port: the port for the reverse shell to call back to
    :param out_flag: whether the user chose to output the result
    :param output_type: the path of reverse shell
    :param reverse_type: the type of reverse shell
    """
    if out_flag is not None:
        type_path = os.path.join(os.getcwd() + ezHTB + f"/{out_flag}")
        dir_path = Path(os.path.join(os.getcwd() + f"/Files{output_type}"))
        new_path = Path(type_path)
        text = dir_path.read_text()
        text = text.replace("127.0.0.1", f"{ip}")
        text = text.replace("1234", f"{port}")
        new_path.write_text(text)
        print(f"|+| {reverse_type} reverse shell has been created in {type_path}")
    else:
        dir_path = Path(os.path.join(os.getcwd() + f"/Files{output_type}"))
        text = dir_path.read_text()
        text = text.replace("127.0.0.1", f"{ip}")
        text = text.replace("1234", f"{port}")
        print(text)


def start_nmap(hostname, ip_address, nmap_type):
    """
    This function handle nmap it start it and check for which parameter does the user provide and then
    it execute that command. print nmap scan completed when it finish
    :param hostname: the name of the target
    :param ip_address: the ip of the target
    :param nmap_type: what type of scan does the user wants
    """
    try:
        if hostname is not None:
            output = os.path.join(os.getcwd() + ezHTB + box_name + OUTPUT_NMAP)
            nmap_handle(ip_address, nmap_type, output)
            print("|*| Nmap scan completed")
        elif hostname is None:
            output = os.path.join(os.getcwd() + ezHTB + OUTPUT_NMAP)
            nmap_handle(ip_address, nmap_type, output)
            print("|*| Nmap scan completed")

    except Exception as skip:
        print("|-| Failed to initiate nmap")
        print(skip)

def nmap_handle(ip_address, nmap_type, output):
    """
    This function handles nmap to run with a given nmap scan type. special is recommended!!
    :param ip_address: ip address of the target
    :param nmap_type: the chosen nmap scan type
    :param output: the result path
    :return:
    """
    if nmap_type == "special":
        tmp_file = "/tmp/" + ip_address + str(random.randrange(1000, 9999))
        subprocess.call([NMAP_BIN_LOC, "-Pn", "-p-", "-min-rate", "1000", "-oG", tmp_file, ip_address],
                        stdout=subprocess.DEVNULL)
        list_open_ports = nmap_handle_special(tmp_file)
        if len(list_open_ports) >= 1:
            open_ports_string = re.sub("[^a-zA-Z0-9 \n,\.]", "", str(list_open_ports))
            print(f"|+| Nmap: Open ports {open_ports_string}")
            print(f"|+| Nmap: Starting deep scan on ports {open_ports_string}")
            subprocess.call([NMAP_BIN_LOC, "-p", open_ports_string, "-Pn", "-sC", "-sV", "-oN", output,
                             ip_address], stdout=subprocess.DEVNULL)
    elif nmap_type == "quick":
        subprocess.call([NMAP_BIN_LOC, "-Pn", "-oN", output, ip_address],
                        stdout=subprocess.DEVNULL)
    elif nmap_type == "default":
        subprocess.call([NMAP_BIN_LOC, "-Pn", "-sC", "-sV", "-oN", output,
                         ip_address], stdout=subprocess.DEVNULL)
    elif nmap_type == "maximum":
        subprocess.call([NMAP_BIN_LOC, "-Pn", "-T4", "-A", "-p", "1-65535", "-oN", output, ip_address],
                        stdout=subprocess.DEVNULL)

def nmap_handle_special(tmp_file):
    """
    This function returns the open ports from nmap scan output file
    :param tmp_file: the file to grep open ports from
    :return: a list of open ports
    """
    for line in open(tmp_file):
        if "Ports" in line:
            line = line.split("Ports")[1].strip(" ").split(",")
            ports = [port.split("/")[0] for port in line]
            ports = [re.sub("[^a-zA-Z0-9 \n\.]", "", port) for port in ports]
            return ports


def start_gobuster(args):
    """
    This function runs gobuster with a wordlist chosen based on the parameter that the user provides.
    :param args: ip address, wordlist, https ?
    """

    try:
        if args.hostname is not None:
            output = os.path.join(os.getcwd() + ezHTB + box_name + OUTPUT_GOBUSTER)
            gobuster_helper(args.ip, args.gobuster, args.https, output, args.port)
            print("|*| Gobuster scan completed")
        elif args.hostname is None:
            output = os.path.join(os.getcwd() + ezHTB + OUTPUT_GOBUSTER)
            gobuster_helper(args.ip, args.gobuster, args.https, output, args.port)
            print("|*| Gobuster scan completed")
    except Exception as skip:
        print("|-| Failed to initiate gobuster")
        print(skip)

def gobuster_helper(ip_address, wordlist, https, output, port):
    """
    This is a helper function to run gobuster with a chosen wordlist from the user and with http or https
    :param ip_address: ip address of the target
    :param wordlist: the chosen wordlist
    :param https: will run https if true, will run http is false
    :param output: the result path
    :param port: the target port
    """
    url = "http://"
    if https:
        url = "https://"

    if wordlist == "common" and port is None:
        wordlist = DIR_COMMON
        gobuster_no_port(ip_address, url, wordlist, https, output)
    elif wordlist == "quick" and port is None:
        wordlist = DIR_SMALL
        gobuster_no_port(ip_address, url, wordlist, https, output)
    elif wordlist == "medium" and port is None:
        wordlist = DIR_MEDIUM
        gobuster_no_port(ip_address, url, wordlist, https, output)
    elif wordlist == "common" and port is not None:
        wordlist = DIR_COMMON
        gobuster_port(ip_address, port, url, wordlist, https, output)
    elif wordlist == "quick" and port is not None:
        wordlist = DIR_SMALL
        gobuster_port(ip_address, port, url, wordlist, https, output)
    elif wordlist == "medium" and port is not None:
        wordlist = DIR_MEDIUM
        gobuster_port(ip_address, port, url, wordlist, https, output)

def gobuster_no_port(ip_address, url, wordlist, https, output):
    """
    This function is to check for port 80 and 443 if it is open if it is so then it will do gobuster on that specific
    port with the choose of the user wordlist.
    :param ip_address: the ip of the target
    :param url: http or https
    :param wordlist: the chosen of the user wordlist
    :param https: true if -x if set false otherwise
    :param output: output path
    """
    try:
        if check_port(ip_address, 80) and not https or check_port(ip_address, 443) and https:
            subprocess.call([GOBUSTER_BIN_LOC, "dir", "-w", wordlist, "-z", "-q", "-k", "-x", ".php, .html",
                             "-o", output, "-u", url + ip_address], stdout=subprocess.DEVNULL)
        else:
            print("|-| Failed to start Gobuster: ports closed")
    except OSError:
        print("|-| Failed to initiate gobuster")

def gobuster_port(ip_address, port, url, wordlist, https, output):
    """
    This function is to check for any given port if it is open if it is so then it will do gobuster on that specific
    port with the choose of the user wordlist.
    :param ip_address: the ip of the target
    :param port: the port of the web target
    :param url: http or https
    :param wordlist: the chosen of the user wordlist
    :param https: true if -x if set false otherwise
    :param output: output path
    """
    try:
        if check_port(ip_address, port) and not https or check_port(ip_address, port) and https:
            subprocess.call([GOBUSTER_BIN_LOC, "dir", "-w", wordlist, "-z", "-q", "-k", "-x", ".php, .html",
                             "-o", output, "-u", url + ip_address + ":" + port], stdout=subprocess.DEVNULL)
        else:
            print("|-| Failed to start Gobuster: ports closed")
    except OSError:
        print("|-| Failed to initiate gobuster")

def start_nikto(ip_address, ssl):
    """
    This function is to scan a target web with nikto to look if the web has some vulnerability.
    :param ip_address: ip address of the target
    :param ssl: force ssl so that it starts 443 faster
    """
    try:
        output = os.path.join(os.getcwd() + ezHTB + OUTPUT_NIKTO)
        if ssl:
            subprocess.call([NIKTO_BIN_LOC, "-h", ip_address, "-s", "-o", output], stdout=subprocess.DEVNULL)
            print("|*| Nikto scan completed")
        elif not ssl:
            subprocess.call([NIKTO_BIN_LOC, "-h", ip_address, "-o", output], stdout=subprocess.DEVNULL)
            print("|*| Nikto scan completed")
    except OSError:
        print("|-| Failed to initiate Nikto")


def start_enum4linux(ip_address):
    """
    This function is to enumerating information from Windows or Unix through Samba systems.
    :param ip_address: ip address of the target
    """
    try:
        output_path = os.path.join(os.getcwd() + ezHTB + OUTPUT_NIKTO)
        output = open(output_path, "w")
        subprocess.call([ENUM4LINUX_BIN_LOC, "-a", ip_address], stdout=output)
        print("|*| Enum4linux scan completed")
    except OSError:
        print("|-| Failed to initiate Enum4linux")


def check_port(ip_address, port):
    """
    This function check if the target has http/80 or https/443 up or any port and return the result.
    :param ip_address: the ip of the target
    :param port: to check for port 80 and 443 or any other port
    :return: true if there is a site on that port, false otherwise.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    respond = sock.connect_ex((ip_address, int(port)))
    if respond == 0:
        return True
    else:
        return False


def arg_parser():
    """
    This function gets the inputs from the user to use them in the tools
    :return: the Namespace of the input arguments.
    """
    parser = argparse.ArgumentParser(prog='ezHTB.py', usage='%(prog)s [options]')
    options = parser.add_argument_group('Flag options', '')
    options.add_argument('-H', '--hostname', nargs=1,
                         help='box name: used to create the directory structure and an entry in /etc/hosts')
    options.add_argument('-i', '--ip', action='store', help='box ip address: target ip address')
    options.add_argument('-p', '--port', action='store', help='box port: host port')
    options.add_argument('-R', '--reverse', nargs='+',
                         help='creating a reverse shell based on the choose of the user')
    options.add_argument('-G', '--gobuster', action='store',
                         help='..')
    options.add_argument('-n', '--nmap', action='store',
                         help='nmap scan with one argument. see examples to find which argument you want')
    options.add_argument('-E', '--enum4linux', action='store_true',
                         help='..')
    options.add_argument('-N', '--nikto', action='store_true',
                         help='..')
    options.add_argument('-o', '--out', action='store', help='output file name. ex, -o example.txt')
    options.add_argument('-x', '--https', action='store_true', help='force https')
    options.add_argument('-s', '--ssl', action='store_true', help='force ssl')
    options.add_argument('-a', '--append', action='store_true', help='append the ip address and hostname on /etc/hosts')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args


def main():
    """
    The main function which takes the input from the user and then run the correct nmap scan regarding
    to the input.
    """
    NMAP_STARTED = False
    GOBUSTER_STARTED = False
    NIKTO_STARTED = False
    ENUM4LINUX_STARTED = False

    args = arg_parser()
    print(args)

    print("|+| Creating directories")
    init(args)

    if args.reverse is not None:
        print("|+| Creating a reverse shell")
        reverse(args)

    if args.append is not None:
        print("|+| Creating /etc/hosts entry")
        etc_hosts(args.hostname, args.ip)

    if args.nmap is not None:
        print("|+| Starting nmap")
        nmap = Process(target=start_nmap, args=(args.hostname, args.ip, args.nmap))
        nmap.start()
        NMAP_STARTED = True

    if args.gobuster is not None:
        print("|+| Starting gobuster")
        gobuster = Process(target=start_gobuster, args=(args,))
        gobuster.start()
        GOBUSTER_STARTED = True

    if args.nikto:
        print("|+| Starting nikto")
        nikto = Process(target=start_nikto, args=(args.ip, args.ssl))
        nikto.start()
        NIKTO_STARTED = True

    if args.enum4linux:
        print("|+| Starting enum4linux")
        enum4linux = Process(target=start_enum4linux, args=(args.ip,))
        enum4linux.start()
        ENUM4LINUX_STARTED = True

    if NMAP_STARTED:
        nmap.join()
    if GOBUSTER_STARTED:
        gobuster.join()
    if NIKTO_STARTED:
        nikto.join()
    if ENUM4LINUX_STARTED:
        enum4linux.join()

    print("|*| All scans completed.")


if __name__ == "__main__":
    main()

