from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json
import os

PAGE_URL = 'https://www.amazon.in/s?k=macbooks&crid=3DZ427SF0MAXC&sprefix=macbook%2Caps%2C281&ref=nb_sb_noss_2'

def extract_asin(product_url):
    match = re.search(r'/([A-Z0-9]{10})(?:[/?]|$)', product_url)
    return match.group(1) if match else None

def save_to_json(data, filename="ScrapeData.json"):
    # Load existing data if the file exists
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                file_data = []
    else:
        file_data = []
    
    # Append new data
    file_data.append(data)

    # Save updated data to the file without Unicode escape sequences
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(file_data, file, indent=4, ensure_ascii=False)

def scrape_amazon_products(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the page
        page.goto(page_url)
        html = page.content()

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        products = []

        # Extract product details
        for container in soup.select('.s-widget-container'):
            title_element = container.select_one('.s-title-instructions-style')
            price_element = container.select_one('.a-price > span')
            link_element = container.select_one('a.a-link-normal.s-no-outline')
            rating_element = container.select_one('.a-icon-alt')  # Extract rating
            rating_count_element = container.select_one('.a-size-base')  # Extract number of ratings
            
            if not title_element or not price_element or not link_element:
                continue

            title = title_element.get_text(strip=True)
            price_text = price_element.get_text(strip=True)
            price_text_cleaned = re.sub(r'[₹,]', '', price_text)  # Remove ₹ and commas
            try:
                price = int(price_text_cleaned)
            except ValueError:
                continue
            
            # Get rating and rating count if available
            rating = rating_element.get_text(strip=True) if rating_element else None
            rating_count = rating_count_element.get_text(strip=True) if rating_count_element else "0"

            product_url = link_element['href']
            asin = extract_asin(product_url)
            if not asin:
                continue

            # Navigate to the product page to fetch reviews
            product_page = browser.new_page()
            product_page.goto(f"https://www.amazon.in{product_url}")
            product_html = product_page.content()
            product_soup = BeautifulSoup(product_html, 'html.parser')
            product_page.close()

            # Collect reviews
            reviews = [review.get_text(strip=True) for review in product_soup.select('.review-text-content')]
            
            product_info = {
                "title": title,
                "price": price,
                "priceInDollarFormat": price_text,
                "url": f"https://www.amazon.in{product_url}",
                "asin": asin,
                "rating": rating,
                "rating_count": rating_count,
                "reviews": reviews
            }

            products.append(product_info)

        # Save products to ScrapeData.json
        for product in products:
            try:
                save_to_json(product, "ScrapeData.json")
            except Exception as e:
                print(f"Failed to save product: {e}")

        print("Product data saved to ScrapeData.json")
        browser.close()

def main():
    scrape_amazon_products(PAGE_URL)

if __name__ == "__main__":
    main()
