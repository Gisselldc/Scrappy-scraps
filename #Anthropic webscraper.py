#Anthropic webscraper

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium to run headless (without opening the browser window)
options = Options()
options.headless = True  # Run browser in background (headless mode)

# Set up the ChromeDriver service
service = Service(ChromeDriverManager().install())

# Create the driver using the service and options
driver = webdriver.Chrome(service=service, options=options)

# List of URLs to scrape
urls = [
    "https://www.anthropic.com/news/anthropic-raises-series-b-to-build-safe-reliable-ai"
]

# Define the folder path for the new folder on the desktop
folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'ScrapedBlogs')

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

# Loop through each URL and scrape the content
for url in urls:
    # Open the webpage
    driver.get(url)

    # Wait for a specific element to load (adjust this selector based on your needs)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))  # Wait for article to load
    except:
        print(f"Timed out waiting for page to load: {url}")
        continue

    # Extract content from the article (adjust to the actual content location)
    article = driver.find_element(By.TAG_NAME, 'article')
    
    # Get all the text in the article
    text_content = article.text.strip()

    # Try to get the blog title from the <title> tag
    try:
        page_title = driver.title.strip()
    except:
        page_title = None

    # Extract filename from the last part of the URL
    url_filename = url.split("/")[-1].split("?")[0].split("#")[0]  # Removes query and fragment parts

    # Use page title if available, otherwise fallback to URL-based filename
    filename = page_title if page_title else url_filename

    # Ensure filename is valid
    invalid_chars = r'\/:*?"<>|'
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    filename = filename + ".txt"

    # Define the full path for the file in the new folder
    file_path = os.path.join(folder_path, filename)

    # Write the extracted text to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text_content)

    print(f"Content from {url} has been saved to: {file_path}")

# Close the driver
driver.quit()

# Print confirmation message
print(f"All blogs have been saved to: {folder_path}")
