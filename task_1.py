import hashlib
import math
import sys


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        results = []
        for i in range(self.num_hashes):
            hash_result = int(hashlib.md5((item + str(i)).encode()).hexdigest(), 16)
            results.append(hash_result % self.size)
        return results

    def add(self, item: str):
        if not isinstance(item, str) or not item.strip():
            return
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1

    def __contains__(self, item: str):
        if not isinstance(item, str) or not item.strip():
            return False
        return all(self.bit_array[hash_value] for hash_value in self._hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list):
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "некоректний пароль"
        elif password in bloom_filter:
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    return results


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = [
        "password123",
        "newpassword",
        "admin123",
        "guest",
        "",
        None,
    ]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
