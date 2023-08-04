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

### Navigate to the website ---------------------------------------------------------------------------------------------------------------------------
driver = webdriver.Chrome()
driver.get('https://www.geologycloud.tw/geohome/DataService/swagger/api')

### Get the id of the elements ------------------------------------------------------------------------------------------------------------------------
wait = WebDriverWait(driver, 5)
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
    print(id_list)

except Exception as e:
    print(f"ID Extraction Error occurred: {e}")

### Check the number of elements ---------------------------------------------------------------------------------------------------------------------
print(len(id_list))

### For Loop to Extract the Data ---------------------------------------------------------------------------------------------------------------------
# Step 1: Press the <GET> button
for i in range(0, len(id_list)):
    get_button = driver.find_element(By.XPATH, f'//*[@id="{id_list[i]}"]')
    get_button.click()

    # Step 2: Press the <測試> button
    try:
        test_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'try-out__btn')))
        test_button.click()
    except Exception as e:
        print(f"Test Button Error occurred: {e}")

    # Step 3: Press the <Execute> button
    try:
        xpath_expression = '//*[@class="btn execute opblock-control__btn"]'
        execute_button = wait.until(EC.presence_of_element_located((By.XPATH, xpath_expression)))
        execute_button.click()
    except Exception as e:
        print(f"Execute Button Error occurred: {e}")

    # Step 4: Extract the <Request URL>
    try:
        xpath_expression = '//*[@class="request-url"]'
        url_text = wait.until(EC.presence_of_element_located((By.XPATH, xpath_expression))).text
    except Exception as e:
        print(f"URL Error occurred: {e}")

    # Step 5: Extract the <Response Body>
    response = requests.get(url_text)
    if response.status_code == 200:
        response_content_bytes = response.content
        json_data = response.json()
        print(json_data)
    else:
        print(f"Data request failed with status code: {response.status_code}")

    # Step 6: Save the data as a csv file
    df = pd.json_normalize(json_data, record_path='features', meta='type', meta_prefix='meta_')
    df.to_csv(f'Crawled_Data/Geology_Cloud/{id_list[i]}.csv')
