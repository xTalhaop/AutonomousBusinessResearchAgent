# agent_2.py
import json
import requests
from bs4 import BeautifulSoup

def scrape_urls_agent(json_urls_input: str) -> str:
    """
    Takes a JSON string array of URLs, scrapes the visible text content
    from each website, and combines it into a single raw text dataset.
    """
    print("\n[Agent 2] Activating... Scraping raw data from verified links.")

    try:
        # Parse the JSON string from Agent 1 back into a Python list
        urls = json.loads(json_urls_input)
    except Exception as e:
        return f"Agent 2 Error: Invalid JSON input format. {e}"

    if not urls:
        return "Agent 2 Error: No URLs provided to scrape."

    # Standard browser header to prevent getting blocked by websites
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    combined_raw_text = ""

    # Loop through each verified link provided by Agent 1
    for index, url in enumerate(urls, 1):
        print(f"[Agent 2] Scraping site {index}/{len(urls)}: {url}")
        try:
            # Fetch page content with a 5-second timeout so it doesn't freeze
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                print(f"  -> Skipping (Status {response.status_code})")
                continue

            # Parse the HTML structure
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove scripts, styles, and common clutter like navbars and footers
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.extract()

            # Extract plain text from paragraphs, headers, and list items
            text_blocks = []
            for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'li']):
                cleaned_text = element.get_text().strip()
                if cleaned_text:
                    text_blocks.append(cleaned_text)

            # Join the text blocks of this specific page
            page_text = "\n".join(text_blocks)

            # Append it to our master data string with clear separators
            combined_raw_text += f"\n\n{'=' * 50}\nSOURCE: {url}\n{'=' * 50}\n\n{page_text}\n"

        except Exception as e:
            print(f"  -> Failed to scrape {url}: {e}")
            continue

    return combined_raw_text