import requests
from bs4 import BeautifulSoup
import os
import time
import argparse
import shutil

# ANSI escape code variables for console coloring
ANSI_RESET = "\u001b[0m"
ANSI_GREEN = "\u001b[32m"
ANSI_RED = "\u001b[31m"
ANSI_CYAN = "\u001b[36m"
ANSI_YELLOW = "\u001b[33m"

def spider_site(url, output_directory, pause_time, visited_urls):
    # Check if http or https is in the URL, and add it if it's not there
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    # Check if the URL has already been visited
    if url in visited_urls:
        return

    # Add the URL to the visited URLs set
    visited_urls.add(url)

    # Get the HTML content of the URL
    try:
        print(f"{ANSI_CYAN}Requesting content for {url}...{ANSI_RESET}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        html = response.content
        print(f"{ANSI_GREEN}Successfully retrieved content for {url}{ANSI_RESET}")
    except requests.RequestException as e:
        print(f"{ANSI_RED}Error getting content for {url}: {e}{ANSI_RESET}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the text on the page
    text = soup.get_text()

    # Remove any blank lines
    text = os.linesep.join([s for s in text.splitlines() if s.strip()])

    # Get the filename for the URL, and add "(reader)" if the text is the article or reader view
    filename = url.replace('://', ' - ').replace('/', ' - ')
    if soup.find_all(class_='article') or soup.find_all(class_='reader'):
        filename = f"(reader) {filename}"
    filename = f"url - {filename}.txt"

    # Save the text to the file in the output directory
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    try:
        with open(os.path.join(output_directory, filename), 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"{ANSI_CYAN}Scanned and saved {url} to {os.path.join(output_directory, filename)}{ANSI_RESET}")
    except Exception as e:
        print(f"{ANSI_RED}Error saving file for {url}: {e}{ANSI_RESET}")

    # Find all links on the page
    links = soup.find_all('a')

    # Iterate through the links
    for link in links:
        # Get the href attribute of the link
        href = link.get('href')

        # Check if the href is a valid URL on the same domain
        if href.startswith('http') and url.split('/')[2] in href:
            # Recursively spider the site with a pause
            time.sleep(pause_time)
            spider_site(href, output_directory, pause_time, visited_urls)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recursively spider an array of domains, extract all text, and save to a file in an output directory.')
    parser.add_argument('-d', '--domains', nargs='+', help='Array of domains to spider', required=True)
    parser.add_argument('-o', '--output', help='Output directory to save text files to', default='output')
    parser.add_argument('-p', '--pause', type=int, default=1, help='Time to pause between spidering each page (in seconds)')
    parser.add_argument('-c', '--clean', action='store_true', help='Remove existing files in the output directory')
    args = parser.parse_args()

    # Remove existing files in the output directory if the clean flag is set
    if args.clean and os.path.exists(args.output):
        shutil.rmtree(args.output)

    # Iterate through the domains
    for domain in args.domains:
        visited_urls = set()  # Set to store visited URLs for each domain
        print(f"{ANSI_YELLOW}Spidering site: {domain}{ANSI_RESET}")
        # Spider the site
        spider_site(f"https://{domain}", args.output, args.pause, visited_urls)
