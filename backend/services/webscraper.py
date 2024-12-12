from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')  # No sandbox for headless mode
chrome_options.add_argument('--remote-debugging-port=9222') # Debugging port
chrome_options.add_argument('--start-maximized') # Start maximized
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") # Set user agent
chrome_options.add_argument('--enable-logging') # Enable logging
chrome_options.add_argument('--v=1') # Set logging level

def export_to_file(filename, data):
    with open(filename, 'w') as file:
        for item in data:
            file.write(item + '\n')
    
def get_listing_near_university(state, city, school):
    base_url = "https://www.apartments.com/off-campus-housing/"
    data = []
    
    driver = webdriver.Chrome(options=chrome_options)
    url = f"{base_url}{state}/{city}/{school}/"
    driver.get(url)

    try:
        containers = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "placardContainer"))
        )

        for container in containers:
            ul_element = container.find_element(By.TAG_NAME, "ul")
            li_elements = ul_element.find_elements(By.CLASS_NAME, "mortar-wrapper")

            print(f"Number of listings: {len(li_elements)}")

            for li in li_elements:
                try:
                    url = li.find_element(By.CLASS_NAME, "property-link").get_attribute("href")
                    title = li.find_element(By.CLASS_NAME, "property-title").text
                    address = li.find_element(By.CLASS_NAME, "property-address").text
                    price = li.find_element(By.CLASS_NAME, "property-pricing").text
                    beds = li.find_element(By.CLASS_NAME, "property-beds").text
                    #bath = li.find_element(By.CLASS_NAME, "property-baths").text
                    phone = li.find_element(By.CLASS_NAME, "phone-link").get_attribute("href")
                    img_url = li.find_element(By.CLASS_NAME, "carousel-item").find_element(By.TAG_NAME, "img").get_attribute("src")

                    try:
                        amenities_container = li.find_element(By.CLASS_NAME, "property-amenities")
                        amenities = [span.text for span in amenities_container.find_elements(By.TAG_NAME, "span")]
                    except:
                        amenities = []
                except:
                    continue
                
                min_price, max_price = (price.split("-") if "-" in price else (price, price))
                min_bed, max_bed = (beds.split("-") if "-" in beds else (beds, beds))
                #min_bath, max_bath = (beds.split("-") if "-" in bath else (bath, bath))

                data.append({
                    "url": url,
                    "title": title,
                    "address": address,
                    "min_price": min_price,
                    "max_price": max_price,
                    "min_bed": min_bed,
                    "max_bed": max_bed,
                    # "min_bath": min_bath,
                    # "max_bath": max_bath,
                    "phone": phone,
                    "img_url": img_url,
                    "amenities": amenities
                })

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

    return data