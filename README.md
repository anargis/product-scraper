# Product Scraper

## A Python script to scrape product data (title, price, image) from e-shop websites and save it to a CSV file.

### Steps to install python, pip and create a virtual environment in Linux (Ubuntu)

#### Check distro version
```
cat /etc/lsb-release 
```
OUTPUT
```
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.2 LTS"
```

#### Install python3 deb. Provides the Python interpreter to run Python scripts and commands.
```
sudo apt install python3
```
#### Install python3.10-venv deb. Adds the ability to create virtual environments for isolating dependencies.
```
sudo apt install python3.10-venv
```
#### Install python3-dev deb. Provides development headers for compiling Python packages with native code.
```
sudo apt install python3-dev	
```
#### Install pip3
```
sudo apt install python3-pip
```
#### View pip manual
```
man pip3
or
pip3
```
#### Navigate to your project directory, e.g.:
```
cd Projects/product-scraper
```
#### Create a virtual environment
```
python3 -m venv .venv
```
#### Verify the virtual environment directory exists
```
ls -la .venv
```
#### Activate the virtual environment
```
source .venv/bin/activate
```
#### Install a module (e.g., pynput)
```
pip install pynput
```
#### List installed modules
```
pip list
```
#### Generate requirements.txt from current environment
```
pip freeze > requirements.txt
```
#### Install dependencies from requirements.txt
```
pip install -r requirements.txt
```
#### Deactivate the virtual environment
```
deactivate
```
#### (Optional) Reset the terminal prompt manually, if needed
```
export PS1='\u@\h:\w\$ '
```

### How to use this script
1. **Open the target e-shop website in your web browser: e.g https://books.toscrape.com/**
2. **Inspect the product elements**:
   - Right-click on the product title, price, or image on the page.
   - Select **Inspect** or **Inspect Element** to open the browser’s developer tools.
   - Locate the HTML element corresponding to the product detail you want to scrape (title, price, or image).
   - Identify a unique attribute or class that can be used to construct an XPath.

3. **Add or update XPath entries**:
   - Open the `product-scraper-xpath.json` file.
   - Under the appropriate section (`Title`, `Price`, `Images` or `Next pagination`), add your own new XPath(s) that correctly point to the elements you inspected.
   - For example, if the price is located inside the following HTML structure:
     - `div` with class `product_price`
     - `p` tag with class `price_color`

     You should add the XPath below:
     ```json
     "//div[@class='product_price']/p[@class='price_color']"
     ```
     Do the same for others xpaths
   - Save the JSON file.

4. **Run the scraper**:
   - Execute the script.
   ```
   python3 product-scraper.py
   ```
   - It will use the XPaths in `product-scraper-xpath.json` to find and extract the product data.
   - The output will be saved to a CSV file as specified.
