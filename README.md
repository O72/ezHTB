# ezHTB
ezHTB is a reconnaissance tool for HackTheBox that utilizes nmap, gobuster, nikto, and enum4linux
with different options and features to make your recon faster. 

- ezHTB can
    - Discover hosts and services on a computer network.
    - Brute-force directories and files in web sites.
    - Scan web-servers for dangerous files, vulnerability, outdated server software and other problems.
    - Enumerate information from Windows and Samba systems for file share permissions.
    - Create a reverse shell of your choice in a fast way, the choices being (php, bash, powershell, nc).

## Prerequisites

```bash
# Install python3.
sudo apt-get install python3.6
# Install nmap.
sudo apt-get install nmap
# Install gobuster.
sudo apt-get install gobuster
# Install nikto.
sudo apt-get install nikto
# Install enum4linux.
sudo apt-get install enum4linux
```
## Installation
```bash
git clone https://github.com/O72/ezHTB.git
cd ezHTB
python3 ezHTB.py 
```
## Usage

```bash
python3 ezHTB.py -h
usage: ezHTB.py [options]

optional arguments:
  -h, --help            show this help message and exit

Flag options:

  -H HOSTNAME, --hostname HOSTNAME
                        hostname: used to create the directory structure
  -i IP, --ip IP        ip address: host/target ip address
  -p PORT, --port PORT  port: host/target port
  -R REVERSE [REVERSE ...], --reverse REVERSE [REVERSE ...]
                        reverse type: creating a reverse shell based on the
                        choice of the user
  -G GOBUSTER, --gobuster GOBUSTER
                        gobuster: run gobuster with several argument. see
                        examples to find which argument is best for you.
  -n NMAP, --nmap NMAP  nmap: run nmap scan with several argument. see
                        examples to find which argument is best for you.
  -E, --enum4linux      enum4linux: run enum4linux with -a which will do
                        everything.
  -N, --nikto           nikto: run nikto with -s to force ssl or without.
  -a, --append          Append the ip address and hostname on /etc/hosts
  -o OUT, --out OUT     output file name. ex, -o example.txt
  -x, --https           force https
  -s, --ssl             force ssl
```

## Examples
```bash
# All the output are redirected to ~/exHTB/ezHTB_Results

# It will run nmap with the given ip address and a special type that will check for all ports 
# to find open ports then it will do a deep scan into those open ports. 
# (optional types "quick, default, maximum, special") 
python3 ezHTB.py -n special -i 10.10.10.X

# It will run gobuster with the given ip address and a common directory type that is found in ~/ezHTB/Files
# (optional types "common, quick, medium", optional args "-p" to choose a specific port 'defualt to 80/443 only', "-x" to force https)
python3 ezHTB.py -G common -i 10.0.10.X 

# It will run enum4linux with -a flag which will do everything with the given ip address.
python3 ezHTB.py -E -i 10.10.10.X

# It will run nikto with the given ip address. 
# (optional arg "-s" to force 443)
python3 ezHTB.py -N -i 10.10.10.X

# It will create php reverse shell with the given ip address and port. 
# (optional types "php, bash, powershell, nc", optional arg "-o" to specify output file name)
python3 ezHTB.py -R php -i 10.10.X.X -p 8080
```

## License
[MIT](https://github.com/O72/ezHTB/blob/master/LICENSE)