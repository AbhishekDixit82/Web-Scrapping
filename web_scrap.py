from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Define headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Dictionary
data = {"title":[],"price":[],"mrp":[],"link": []}

# Amazon search URL
url = 'https://www.amazon.in/s?k=iphone&crid=CXY8ABTLUDQP&sprefix=iphone%2Caps%2C264&ref=nb_sb_noss_2'

# Send a GET request with headers
res = requests.get(url,headers=headers)

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(res.text,'html.parser')

# Extract all product titles
titles = soup.select("h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span")

prices = soup.select("span.a-price-whole")

mrps = soup.select("span.a-price.a-text-price span.a-offscreen")

links = soup.select("a.a-link-normal.s-line-clamp-2.s-link-style.a-text-normal")

for title in titles:
    print(title.get_text(strip=True))
    data["title"].append(title.string)

for price in prices:
    print(price.get_text(strip=True))
    data["price"].append(price.string)

for mrp in mrps:
    print(mrp.get_text(strip=True))
    data["mrp"].append(mrp.string)

for link in links:
    href = link.get("href")  # Extract href attribute
    if href:
        full_link = "https://www.amazon.in" + href
        data["link"].append(full_link)

df = pd.DataFrame.from_dict(data)
df.to_csv("data.csv",index=False)