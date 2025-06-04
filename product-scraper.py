import os
import re
import csv
import json 

try:
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import NoSuchElementException
except ImportError as e:
    print("Missing required module. Please install it via: pip install requests selenium")
    print(f"Error: {e}")

class ScrapProductsElements:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')  
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox') 
        options.add_argument('--window-size=1920x1080')  

        self.driver = webdriver.Chrome(options=options)
        self.url = ""
        self.filename = ""
        self.title_xpath = None
        self.price_xpath = None
        self.image_xpath = None
        self.next_xpath = None

    def welcome_msg(self):
        print("\n===Scrape Products===\n")
        print("This script fetches product titles, prices and images from a given URL and saves to CSV.")

    def check_url(self):
        self.url = input("Enter the URL: ").strip()
        if not re.match(r"^https?://", self.url):
            print("URL must start with http:// or https://")
            return False
        
        domain_match = re.match(r"^https?://([^/]+)", self.url)
        if not domain_match or "." not in domain_match.group(1):
            print("URL must include a valid domain (e.g., https://example.com)")
            return False
        
        try:
            response = requests.head(self.url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                return True
            else:
                print("Website responded with non-200 status.")
                return False
        except requests.RequestException:
            print("Could not reach the URL.")
            return False

    def check_export_file(self):
        filename = input("Enter filename (with `.csv` extension): ").strip()
        if not filename:
            filename = "products.csv"

        base, ext = os.path.splitext(filename)
        if ext.lower() != ".csv" or not base:
            print("Invalid filename. Must end with .csv and not be empty.")
            return False

        self.filename = filename
        return True
    
    def get_xpath_by_name(self, name):
        try:
            with open("product-scraper-xpath.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                elements = data["Products"]["Elements"]
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            print(f"Error loading XPath JSON: {e}")
            return []

        for element in elements:
            if element.get("Name", "").strip().lower() == name.lower():
                return element.get("Xpaths", [])
        return []

    def detect_xpath(self, xpaths, name):
        for xpath in xpaths:
            found = self.driver.find_elements(By.XPATH, xpath)

            if found:
                print(f"Found elements for {name} with XPath: {xpath}")

                return xpath
        return None

    def start_scraping(self):
        self.driver.get(self.url)

        self.title_xpath = self.detect_xpath(self.get_xpath_by_name("Title"), "Title")
        self.price_xpath = self.detect_xpath(self.get_xpath_by_name("Price"), "Price")
        self.image_xpath = self.detect_xpath(self.get_xpath_by_name("Images"), "Images")
        self.next_xpath = self.detect_xpath(self.get_xpath_by_name("Xpaths"), "Next")

        missing = []
        if not self.title_xpath:
            missing.append("Title")
        if not self.price_xpath:
            missing.append("Price")
        if not self.image_xpath:
            missing.append("Image")
        
        if missing:
            print(f"Warning: Could not find XPath(s) for: {', '.join(missing)}. Continuing with available data.")

        headers = ["Title"]
        if self.price_xpath:
            headers.append("Price")
        if self.image_xpath:
            headers.append("Image")

        product_count = 0
        
        print(f"Scraped {product_count} items so far...")

        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            while True:
                titles = self.driver.find_elements(By.XPATH, self.title_xpath)
                prices = self.driver.find_elements(By.XPATH, self.price_xpath) if self.price_xpath else []
                images = self.driver.find_elements(By.XPATH, self.image_xpath) if self.image_xpath else []

                max_len = max(len(titles), len(prices), len(images))
                for i in range(max_len):
                    title = titles[i].get_attribute("title") if i < len(titles) else ""
                    if not title and i < len(titles):
                        title = titles[i].text                    
                        
                    price = prices[i].text if i < len(prices) else ""
                    image = images[i].get_attribute("src") if i < len(images) else ""

                    if title.strip():
                        row = [title.strip()]
                        if self.price_xpath:
                            row.append(price.strip())
                        if self.image_xpath:
                            row.append(image.strip())
                        writer.writerow(row)
                        product_count += 1

                try:
                    next_btn = self.driver.find_element(By.XPATH, self.next_xpath)

                    next_btn.click()
                except NoSuchElementException:
                    print("No more pages to scrape.")
                    break

        self.driver.quit()
        print(f"\nScraping completed. Data saved to '{self.filename}'. Found {product_count} product(s).")

    def run(self):
        self.welcome_msg()
        if not self.check_url():
            self.driver.quit()
            return
        if not self.check_export_file():
            self.driver.quit()
            return
        self.start_scraping()

# Run the scraper
if __name__ == "__main__":
    scraper = ScrapProductsElements()
    scraper.run()