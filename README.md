# ezHTB
Reconnaissance tool using Python for HackTheBox that runs nmap and gobuster for you to make your life easier.

## Prerequisites

### For Kali Linux
*  Install python3.
```bash
sudo apt-get install python3.6
```
* Install nmap.
```bash
sudo apt-get install nmap
```
* Install gobuster.
```bash
sudo apt-get install gobuster
```

## Usage

```python3
λ O72 Desktop → python3 ezHTB.py -h
usage: ezHTB.py [options] box_name box_ip_address

positional arguments:
  box_name        box name: used to create the directory structure
  box_ip_address  box_ip_address: target ip address
  {}              Default run: nmap -sC -sV -oN | gobuster http/https
                  common_dir.txt wordlists

optional arguments:
  -h, --help      show this help message and exit
  -q, --quick     determine scan parameters: nmap -Pn -sV | gobuster
                  http/https small wordlists
  -m, --maximum   determine scan parameters: nmap -T4 -A -p 1-65535 | gobuster
                  http/https medium wordlists
  -x, --https     force https

```


## License
[MIT](https://github.com/O72/ezHTB/blob/master/LICENSE)