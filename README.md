# Web Spider 

This is a Python script that allows you to recursively spider an array of domains, extract all text from the webpages, and save them to text files in an output directory. The script uses the `requests` library to retrieve web content and the `BeautifulSoup` library to parse HTML.

## Prerequisites

To run this script, you need to have the following installed:

- Python 3
- The `requests` library
- The `beautifulsoup4` library

You can install the required libraries using pip:

```shell
pip install requests beautifulsoup4
```

## Usage

To use the web spider script, follow these steps:

1. Clone or download the script to your local machine.
2. Open a terminal or command prompt and navigate to the directory where the script is located.
3. Run the script using the following command:

   ```shell
   python spider.py -d domain1 domain2 ... -o output_directory [-p pause_time] [-c]
   ```

   Replace `domain1 domain2 ...` with the domains you want to spider, separated by spaces. For example:

   ```shell
   python spider.py -d example.com example.org -o output
   ```

   The `-o` option specifies the output directory where the text files will be saved. If the directory doesn't exist, it will be created.

   The optional `-p` option allows you to specify the time to pause between spidering each page in seconds. The default value is 1 second.

   The optional `-c` flag indicates whether to remove existing files in the output directory before spidering. Use this flag if you want to start with a clean output directory.

4. The script will start spidering the specified domains, retrieving the web content, and saving the extracted text to individual text files in the output directory. The files will be named based on the URL of each page.

## Example

Here's an example of how to use the script:

```shell
python spider.py -d example.com example.org -o output -p 2 -c
```

This command will spider the domains `example.com` and `example.org`, pause for 2 seconds between each page request, and remove existing files in the `output` directory before spidering.

## Notes

- The script retrieves the web content using the HTTP or HTTPS protocol. If a domain is specified without the protocol (e.g., `example.com` instead of `https://example.com`), it will automatically prepend `https://` to the URL.
- The script checks if a URL has already been visited to avoid duplicating requests.
- The extracted text is saved to individual text files in the specified output directory. Blank lines are removed from the text content.
- The script recursively spiders the site by following links on each page, limited to the same domain.
- Console output is color-coded for easier visibility of successful and error messages.

Feel free to customize and modify the script according to your specific requirements. Happy spidering!
