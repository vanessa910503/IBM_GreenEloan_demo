from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
import re

### Get the API Key ---------------------------------------------------------------------------------------------------------------------------
api_key = 'ec40398c-b3cd-45e0-9bfd-462514dfddc6'

### Navigate to the website ---------------------------------------------------------------------------------------------------------------------------
driver = webdriver.Chrome()
driver.get('https://data.epa.gov.tw/swagger/')

### Get the id of the elements ------------------------------------------------------------------------------------------------------------------------
wait = WebDriverWait(driver, 10)
try:
    # Wait for the elements to be present 
    xpath_expression = '//*[@class="opblock opblock-get"]'
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath_expression)))

    # Create an empty list to store the ids
    id_list = []

    # Get the text of the id attribute for each element and append it to the list
    for element in elements:
        id_text = element.get_attribute("id")
        id_list.append(id_text)
    # print(id_list)

except Exception as e:
    print(f"ID Extraction Error occurred: {e}")

### Check the number of elements ---------------------------------------------------------------------------------------------------------------------
print(len(id_list))

### For Loop to Extract the Data ---------------------------------------------------------------------------------------------------------------------
# Step 1: Press the <GET> button
for i in range(0, 20):
    get_button = driver.find_element("xpath", f'//*[@id="{id_list[i]}"]')
    get_button.click()

    # Step 2: Press the <Try it out> button
    try:
        test_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'try-out__btn')))
        test_button.click()
    except Exception as e:
        print(f"Test Button Error occurred: {e}")

    # Step 3: Input the API Key
    try:
        api_key_input = driver.find_element("xpath", "//input[contains(@placeholder, 'api_key')]")
        api_key_input.send_keys(api_key)
    except Exception as e:
        print(f"API Key Input Error occurred: {e}")

    # Step 4: Press the <Execute> button
    try:
        xpath_expression = '//*[@class="btn execute opblock-control__btn"]'
        test_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression)))
        test_button.click()
    except Exception as e:
        print(f"Execute Button Error occurred: {e}")

    # Step 5: Extract the <Curl>
    try:
        xpath_expression = '//*[@class="curl"]'
        url_text = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_expression))).text
    except Exception as e:
        print(f"URL Error occurred: {e}")

    # Step 6: Extract only the URL
    url_pattern = r'curl -X GET "(.*?)" -H "accept: \*/\*"'
    url_match = re.search(url_pattern, url_text)
    if url_match:
        url_part = url_match.group(1) 
    else:
        print("URL not found in the string.")

    # Step 7: Extract the data
    # data = requests.get(url_part)
    # data_json = data.json()

    # Step 7: Extract the data
    try:
        data = requests.get(url_part)
        data.raise_for_status()  # Raises an exception for non-2xx status codes
        data_json = data.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decode error occurred: {json_err}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Step 8: Save the data as a csv file
    df = pd.DataFrame(data_json['records'])
    df.to_csv(f'Crawled_Data/Environment_Protection_Administration/{id_list[i]}.csv')
