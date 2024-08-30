import requests
import socks
import socket
from requests.exceptions import ProxyError, ConnectTimeout
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# File containing the list of proxies
proxies_file = 'proxies.txt'

# Target URL
target_url = 'https://www.google.com'

# File to store successfully accessed proxies
output_file = 'successful_proxies.txt'


def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies


def check_proxy(proxy, proxy_type):
    try:
        if proxy_type in ['http', 'https']:
            response = requests.get(target_url, proxies={proxy_type: f"{proxy_type}://{proxy}"}, timeout=5)
            response.raise_for_status()
            print(f"{proxy_type.upper()} proxy {proxy} is working.")
            return f"{proxy_type}://{proxy}"
        else:
            socks.set_default_proxy(socks.SOCKS4 if proxy_type == 'socks4' else socks.SOCKS5, proxy.split(':')[0],
                                    int(proxy.split(':')[1]))
            socket.socket = socks.socksocket
            response = requests.get(target_url, timeout=5)
            response.raise_for_status()
            print(f"{proxy_type.upper()} proxy {proxy} is working.")
            return f"{proxy_type}://{proxy}"
    except (ProxyError, ConnectTimeout, requests.exceptions.RequestException) as e:
        print(f"{proxy_type.upper()} proxy {proxy} failed: {e}")
        return None


def check_all_proxies(proxies):
    successful_proxies = []
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        for proxy in proxies:
            for protocol in ['http', 'https', 'socks4', 'socks5']:
                futures.append(executor.submit(check_proxy, proxy, protocol))

        for future in as_completed(futures):
            result = future.result()
            if result:
                successful_proxies.append(result)

    return successful_proxies


# Load proxies from the file
proxies = load_proxies(proxies_file)

# Check all proxies
successful_proxies = check_all_proxies(proxies)

# Write successfully accessed proxies to the output file
with open(output_file, 'w') as file:
    for proxy in successful_proxies:
        file.write(proxy + '\n\t')

print(f"Successfully accessed proxies have been written to {output_file}.")
