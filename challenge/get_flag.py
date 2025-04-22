import subprocess
import os
import sys
import requests
import json

FLAG_PATH = "/challenge/flag.txt"
EXPECTED_VERSION = "v2.1.0"
PRIME_TEST = 101
PRIME_EXPECTED = True
SUMDIGITS_INPUT = 1234
SUMDIGITS_EXPECTED = 10

def check_container():
    try:
        names = subprocess.check_output(
            "docker ps --format '{{.Names}}'", shell=True
        ).decode().split()
        return "chal-app" in names
    except Exception as e:
        print(f"No running 'chal-app' container: {e}")
        return False

def get_json(url):
    r = requests.get(url, timeout=2)
    r.raise_for_status()
    return r.json()

def post_json(url, payload):
    r = requests.post(url, json=payload, timeout=2)
    r.raise_for_status()
    return r.json()

def main():
    if os.geteuid() != 0:
        print("Flag can only be revealed by root.")
        sys.exit(1)
    if not check_container():
        print("Container 'chal-app' is not running.")
        sys.exit(1)
    try:
        j = get_json("http://localhost:5000/healthz")
        assert j["status"] == "ok", "Healthz endpoint failed."
        j = get_json("http://localhost:5000/version")
        assert j["version"] == EXPECTED_VERSION, "Version endpoint failed"
        j = get_json(f"http://localhost:5000/prime/{PRIME_TEST}")
        assert j["prime"] == PRIME_EXPECTED, "Prime check failed"
        j = post_json("http://localhost:5000/sumdigits", {"number":SUMDIGITS_INPUT})
        assert j["sum"] == SUMDIGITS_EXPECTED, "Sumdigits endpoint failed"
    except Exception as e:
        print(f"One or more checks failed: {e}")
        sys.exit(1)
    with open(FLAG_PATH) as f:
        print(f.read().strip())

if __name__ == "__main__":
    main()