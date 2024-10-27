from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the Chrome driver
service = ChromeService(executable_path='C:/Program Files (x86)/chromedriver-win64/chromedriver.exe')  # Change to your chromedriver path
driver = webdriver.Chrome(service=service, options=chrome_options)


# Function to scrape obituary listings
def scrape_obituary_listings(url):
    driver.get(url)

    try:
        # Wait for the obituary list to load, with a polling interval
        wait = WebDriverWait(driver, 10, poll_frequency=1)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Find all obituary items
        obituary_items = driver.find_elements(By.CSS_SELECTOR, '.obituary-list .obituary-item')

        # Extract data
        obituaries = []
        for item in obituary_items:
            name = item.find_element(By.CSS_SELECTOR, 'h2').text
            date = item.find_element(By.CSS_SELECTOR, '.obituary-date').text
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            obituaries.append({
                'name': name,
                'date': date,
                'link': link
            })

        return obituaries

    except TimeoutException:
        print("The page took too long to load or the expected element was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
url = 'https://www.asancheztfh.com/obituary-listing'
obituary_listings = scrape_obituary_listings(url)

if obituary_listings:
    for obituary in obituary_listings:
        print(f"Name: {obituary['name']}, Date: {obituary['date']}, Link: {obituary['link']}")

# Clean up
driver.quit()