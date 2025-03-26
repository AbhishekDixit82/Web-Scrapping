from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

# Define headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Base URL (Amazon search query for iPhone)
base_url = "https://www.amazon.in/s?k=iphone&page="

# Number of pages to scrape
num_pages = 5

# Dictionary to store data
data = {"title": [], "price": [], "mrp": [], "link": []}

for page in range(1, num_pages + 1):
    print(f"Scraping Page {page}...")
    
    url = base_url + str(page)
    res = requests.get(url, headers=headers)
    
    if res.status_code != 200:
        print(f"⚠️ Page {page} returned status {res.status_code}. Skipping...")
        continue

    soup = BeautifulSoup(res.text, 'html.parser')

    # Extract data
    titles = soup.select("h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span")
    prices = soup.select("span.a-price-whole")
    mrps = soup.select("span.a-price.a-text-price span.a-offscreen")
    links = soup.select("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal")

    num_products = max(len(titles), len(prices), len(mrps), len(links))

    for i in range(num_products):
        title = titles[i].get_text(strip=True) if i < len(titles) else "N/A"
        price = prices[i].get_text(strip=True) if i < len(prices) else "N/A"
        mrp = mrps[i].get_text(strip=True) if i < len(mrps) else "N/A"
        link = "https://www.amazon.in" + links[i].get("href") if i < len(links) else "N/A"

        data["title"].append(title)
        data["price"].append(price)
        data["mrp"].append(mrp)
        data["link"].append(link)

    # Add a delay to prevent getting blocked
    time.sleep(random.uniform(3, 7))

# Save data to CSV
df = pd.DataFrame.from_dict(data)
df.to_csv("amazon_iphone_data.csv", index=False)

print("✅ Scraping Completed! Data saved to amazon_iphone_data.csv")