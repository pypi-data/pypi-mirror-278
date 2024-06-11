import os
import time
import argparse
import requests
import subprocess
from validlink import check_url_validity
from .utils import install_pip, install_requests, install_tor
from .banner import print_banner

green = "\033[92m"
red = "\033[91m"
white = "\033[97m"
reset = "\033[0m"
cyan = "\033[36m"

def is_tor_installed():
    try:
        subprocess.check_output('which tor', shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def initialize_environment():
    install_pip()
    install_requests()
    install_tor()
    os.system("service tor start")

def ma_ip():
    url = 'https://api.ipify.org'
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException:
        print(f'{white}[{red}!{white}] {red}Issue connecting to Tor network. Please check your Tor installation and connection.{reset}')
        return None

def change_ip():
    os.system("service tor reload")
    return ma_ip()

def change_ip_repeatedly(interval, count):
    if count == 0:
        while True:
            time.sleep(interval)
            new_ip = change_ip()
            if new_ip:
                print(f'{white}[{green}+{white}]{green} Your IP has been changed to {white}:{green} {new_ip}')
    else:
        for _ in range(count):
            time.sleep(interval)
            new_ip = change_ip()
            if new_ip:
                print(f'{white}[{green}+{white}]{green} Your IP has been changed to {white}:{green} {new_ip}')

def auto_fix():
    install_pip()
    install_requests()
    install_tor()
    os.system("pip3 install --upgrade autoip")

def main():
    parser = argparse.ArgumentParser(description="AutoIP - Automate IP address changes using Tor")
    parser.add_argument('--interval', type=int, default=60, help='Time in seconds between IP changes')
    parser.add_argument('--count', type=int, default=10, help='Number of times to change the IP. If 0, change IP indefinitely')
    parser.add_argument('--ip', action='store_true', help='Display the current IP address and exit')
    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix issues (install/upgrade packages)')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    args = parser.parse_args()

    if not is_tor_installed():
        print(f"{white}[{red}!{white}] {red}Tor is not installed. Please install Tor and try again.{reset}")
        return

    if args.auto_fix:
        auto_fix()
        print(f"{white}[{green}+{white}]{green} Auto-fix complete.{reset}")
        return

    if args.ip:
        initialize_environment()
        ip = ma_ip()
        if ip:
            print(f'{white} [{green}+{white}] {white}Current IP {white}:{green} {ip}')
    else:
        print_banner()
        initialize_environment()
        change_ip_repeatedly(args.interval, args.count)

if __name__ == "__main__":
    url = "https://www.example.com"
    is_valid = check_url_validity(url)
    if is_valid:
        main()
    else:
        print(f"{white}[{red}!{white}] {red}Please connect to the internet.{reset}")
