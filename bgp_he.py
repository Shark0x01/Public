#!/usr/bin/python3
import requests
import urllib3
import argparse
from bs4 import BeautifulSoup

# Diable anonying warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(target):
    url = f"https://bgp.he.net/search"
    headers = {
        'Host': 'bgp.he.net',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://bgp.he.net/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Te': 'trailers',
        'Connection': 'close',
    }

    params = {
        'search[search]': target,
        'commit': 'Search',
    }

    #proxies = {'https':'http://127.0.0.1:8080'}

    response = requests.get(url, headers=headers, params=params,verify=False)
    soup = BeautifulSoup(response.text,"html.parser")
    table = soup.find('table')

    if table: 
        # the Header (the first line)
        header_columns = table.find('tr').find_all(['th'])
        header_row_data = [col.get_text(strip=True) for col in header_columns]
        
        # Data rows
        table_data = [header_row_data]

        for row in table.find_all('tr')[1:]: 
            columns = row.find_all(['td', 'th'])
            row_data = [col.get_text(strip=True) for col in columns]
            table_data.append(row_data)

        # Find the maximum width of each column
        column_widths = [max(len(str(row[i])) for row in table_data) for i in range(len(header_row_data))]

        # Print the entire table
        for row_data in table_data:
            formatted_row = '\t\t'.join(str(data).ljust(width) for data, width in zip(row_data, column_widths))
            print(formatted_row)
    else:
        print("No results found.")

parser = argparse.ArgumentParser(
                    prog='BGP_HE',
                    description='Simple Cli Parser for bgp.he.net')
parser.add_argument('-org','--organization', type=str, required=True, help="the target org eg: Github")

args = parser.parse_args()
main(target=args.organization)