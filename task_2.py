import json
import time
from typing import Tuple

from datasketch import HyperLogLog

LOG_FILE = "lms-stage-access.log"


def load_ip_addresses(filename: str) -> list:
    ip_addresses = []
    with open(filename, "r") as file:
        for line in file:
            try:
                log_entry = json.loads(line.strip())
                ip = log_entry.get("remote_addr")
                if ip:
                    ip_addresses.append(ip)
            except json.JSONDecodeError:
                continue
    print(f"Завантажено {len(ip_addresses)} IP-адрес з файлу.")
    return ip_addresses


def exact_count(ip_list: list) -> Tuple[int, float]:
    start = time.time()
    unique_ips = set(ip_list)
    duration = time.time() - start
    return len(unique_ips), duration


def hll_count(ip_list: list, p: int = 14) -> Tuple[int, float]:
    # p = 14 -> стандартна точність (помилка ~1.04 / sqrt(2^p) ≈ 1%)
    hll = HyperLogLog(p)
    start = time.time()
    for ip in ip_list:
        hll.update(ip.encode("utf8"))
    duration = time.time() - start
    return int(hll.count()), duration


def print_results_table(exact_result, hll_result):
    from tabulate import tabulate

    headers = ["", "Точний підрахунок", "HyperLogLog (datasketch)"]
    table = [
        ["Унікальні елементи", exact_result[0], hll_result[0]],
        ["Час виконання (сек.)", round(exact_result[1], 4), round(hll_result[1], 4)],
    ]
    print("Результати порівняння:\n")
    print(tabulate(table, headers=headers, tablefmt="grid"))


def main():
    ip_list = load_ip_addresses(LOG_FILE)
    exact_result = exact_count(ip_list)
    hll_result = hll_count(ip_list)
    print_results_table(exact_result, hll_result)


if __name__ == "__main__":
    main()
