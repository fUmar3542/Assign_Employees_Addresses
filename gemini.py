import pandas as pd
from geopy import Nominatim
from geopy.distance import geodesic
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Set the path to the ChromeDriver executable
chromedriver_path = "chromedriver-32.exe"
service = Service(chromedriver_path)

# Set the path to the Portable Chrome executable
chrome_exe_path = "chrome-win32/chrome.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_exe_path


def get_soup(url):
    soup = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            return soup
    except Exception as ex:
        with open('errors.txt', 'a') as error_file:
            error_file.write(f"Error: {str(ex)}\n")
        print(ex)
    finally:
        return soup


# Define functions for clarity
def calculate_distance(location1, location2):
  return geodesic(location1.latitude, location1.longitude, location2.latitude, location2.longitude).m


def get_lat_lng(address, driver):
    # Locate the input field by its id
    input_field = driver.find_element(By.CLASS_NAME, "searchboxinput")
    # Clear the input field (optional, if you want to replace existing text)
    input_field.clear()
    # Enter the desired text into the input field
    input_field.send_keys(address)
    # Click on the button with id "btnfind"
    find_button = driver.find_element(By.ID, "searchbox-searchbutton")
    find_button.click()
    # Wait for the map to load (you may need to adjust the wait time)
    driver.implicitly_wait(10)  # Wait for 10 seconds

    # Extract the longitude and latitude
    location_info = driver.find_element_by_xpath("//button[@aria-label='Share']")
    location_info.click()
    latitude_element = driver.find_element_by_xpath("//input[@aria-label='Latitude']")
    longitude_element = driver.find_element_by_xpath("//input[@aria-label='Longitude']")
    latitude = latitude_element.get_attribute("value")
    longitude = longitude_element.get_attribute("value")
    print("Latitude:", latitude)
    print("Longitude:", longitude)

    return lat_value, lng_value


def assign_addresses(commercial_df, employee_df, addresses_per_employee, driver):
  driver.get('https://www.google.com/maps/')
  time.sleep(1)
  assignments = {}
  for employee_index, employee_row in employee_df.iterrows():
    assignments[employee_row["Name"]] = []

  for employee_index, employee_row in commercial_df.iterrows():
    zip = str(employee_row['Zip'])
    if '-' in zip:
      zip = (zip.split('-'))[0]
    employee_address = f"{employee_row['Address']}, {employee_row['City']}, {employee_row['State']}, {zip}"

    lat_value, lng_value = get_lat_lng(employee_address, driver)
    print(employee_address, lat_value, lng_value)

  # for employee_index, employee_row in employee_df.iterrows():
  #   zip = str(employee_row['Zip'])
  #   if '-' in zip:
  #     zip = (zip.split('-'))[0]
  #   employee_address = f"{employee_row['Address']}, {employee_row['City']}, {employee_row['State']}, {zip}"
  #
  #   lat_value, lng_value = get_lat_lng(employee_address, driver)
  #   print(employee_address, lat_value, lng_value)

  return assignments


def main():
  excel_file = 'Addresses1.xlsx'
  xls = pd.ExcelFile(excel_file)

  commercial_df = pd.read_excel(xls, 'Commercial')
  employee_df = pd.read_excel(xls, 'Employee')

  addresses_per_employee = 2

  # Create a Chrome driver instance
  driver = webdriver.Chrome(service=service, options=chrome_options)
  assignments = assign_addresses(commercial_df, employee_df, addresses_per_employee, driver)
  # Delete all cookies
  driver.delete_all_cookies()
  # Close the browser
  driver.quit()

main()
