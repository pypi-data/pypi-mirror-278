from collections import defaultdict
import socket
from typing import DefaultDict, Dict, List, NamedTuple
import requests
import time
from statistics import mean
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init


# Initialize colorama
init(autoreset=True)

# Define the hostnames
hostnames = ["www.revenuecat.com", "app.revenuecat.com", "api.revenuecat.com"]


# Function to resolve DNS and get all IPs
def resolve_dns(hostname: str) -> List[str]:
    try:
        return socket.gethostbyname_ex(hostname)[2]
    except socket.gaierror:
        return []


class TestResult(NamedTuple):
    hostname: str
    ip: str
    failures: int
    min_latency: float
    max_latency: float
    avg_latency: float


# Function to issue HTTP requests and measure latencies
def measure_latency(ip: str, hostname: str) -> TestResult:
    url = f"http://{ip}/favicon-32x32.png"
    headers = {"Host": hostname}
    latencies: List[float] = []
    failures = 0

    for _ in range(10):
        start_time = time.time()
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if hostname == "api.revenuecat.com" and response.status_code == 404:
                pass
            else:
                response.raise_for_status()
        except (requests.RequestException, requests.Timeout) as e:
            print(f"{error('ERROR')}: Failed to connect to {hostname} at {ip}: {e}")
            failures += 1
        latency = time.time() - start_time
        latencies.append(latency)

    return TestResult(
        hostname=hostname,
        ip=ip,
        failures=failures,
        min_latency=min(latencies, default=0),
        max_latency=max(latencies, default=0),
        avg_latency=mean(latencies) if latencies else 0,
    )


# Function to print results with colors
def print_results(hostname: str, results: List[TestResult]):
    print(f"\nResults for {color(hostname, Fore.CYAN)}:")
    for result in results:
        if result.failures == 0:
            res = ok("OK")
        else:
            res = error(f"FAILURES [{result.failures}/10]")

        print(f"  - {color(result.ip, Fore.YELLOW)}: {res}")
        print(
            f"    Latencies (min/max/avg): {result.avg_latency*1000:.1f}ms / {result.max_latency*1000:.1f}ms / {result.avg_latency*1000:.1f}ms"
        )


def color(msg: str, color: Fore) -> str:
    return f"{color}{msg}{Style.RESET_ALL}"


def error(msg: str):
    return color(msg, Fore.RED)


def ok(msg: str):
    return color(msg, Fore.GREEN)


def find_client_ip() -> str:
    try:
        return requests.get("http://ifconfig.me/ip").text.strip()
    except requests.RequestException as e:
        print(f"{error('ERROR')}: Failed to get client IP: {e}")
        return "Unknown"


# Main logic
def main():
    print("Finding client Public IP...")
    ip = find_client_ip()
    print(f"Client Public IP: {color(ip, Fore.YELLOW)}")

    print("")
    print("Resolving hostnames...")
    hostname_ips: Dict[str, List[str]] = {}
    for hostname in hostnames:
        ips = resolve_dns(hostname)
        if not ips:
            print(f"* {color(Fore.CYAN, hostname)}: {error('Failed to resolve')}")
            continue
        print(f"* {color(Fore.CYAN, hostname)}: {ok('Resolved ok')}")
        for ip in ips:
            print(f"  - {ip}")
        hostname_ips[hostname] = ips

    print("")
    print("Connectivity check...")
    with ThreadPoolExecutor() as executor:
        futures: List[Future[TestResult]] = []
        for hostname, ips in hostname_ips.items():
            for ip in ips:
                futures.append(executor.submit(measure_latency, ip, hostname))

        results: DefaultDict[str, List[TestResult]] = defaultdict(list)
        for future in as_completed(futures):
            try:
                result = future.result()
                results[result.hostname].append(result)
            except Exception as e:
                print(f"{error('ERROR')}: Error ocurred: {e}")

        for hostname, res in results.items():
            print_results(hostname, res)


if __name__ == "__main__":
    main()
