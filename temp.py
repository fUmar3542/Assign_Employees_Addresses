# import pandas as pd
# from geopy import Nominatim
# from geopy.distance import geodesic
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# from datetime import datetime
# import time
#
# # Set the path to the ChromeDriver executable
# chromedriver_path = "chromedriver-32.exe"
# service = Service(chromedriver_path)
#
# # Set the path to the Portable Chrome executable
# chrome_exe_path = "chrome-win32/chrome.exe"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = chrome_exe_path
#
#
# def get_soup(url):
#     soup = []
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             html = response.text
#             soup = BeautifulSoup(html, 'html.parser')
#             return soup
#     except Exception as ex:
#         with open('errors.txt', 'a') as error_file:
#             error_file.write(f"Error: {str(ex)}\n")
#         print(ex)
#     finally:
#         return soup
#
#
# # Define functions for clarity
# def calculate_distance(location1, location2):
#   return geodesic(location1.latitude, location1.longitude, location2.latitude, location2.longitude).m
#
#
# def assign_addresses(commercial_df, employee_df, addresses_per_employee, driver):
#   driver.get('https://www.latlong.net/')
#   time.sleep(2)
#   assignments = {}
#   for employee_index, employee_row in employee_df.iterrows():
#     assignments[employee_row["Name"]] = []
#
#   for employee_index, employee_row in employee_df.iterrows():
#     zip = str(employee_row['Zip'])
#     if '-' in zip:
#       zip = (zip.split('-'))[0]
#     employee_address = f"{employee_row['Address']}, {employee_row['City']}, {employee_row['State']}, {zip}"
#
#     # Locate the input field by its id
#     input_field = driver.find_element_by_id("place")
#
#     # Clear the input field (optional, if you want to replace existing text)
#     input_field.clear()
#
#     # Enter the desired text into the input field
#     input_field.send_keys(employee_address)
#
#     # Click on the button with id "btnfind"
#     find_button = driver.find_element(By.ID, "btnfind")
#     find_button.click()
#
#     # Find the text field element by its id
#     lat_field = driver.find_element_by_id("lat")
#
#     # Get the value of the text field
#     lat_value = lat_field.get_attribute("value")
#
#     # Find the text field element by its id
#     lng_field = driver.find_element_by_id("lng")
#
#     # Get the value of the text field
#     lng_value = lat_field.get_attribute("value")
#
#
#
#     # distances = []
#     # for commercial_index, commercial_row in commercial_df.iterrows():
#     #   zip = str(commercial_row['Zip'])
#     #   if '-' in zip:
#     #     zip = (zip.split('-'))[0]
#     #   commercial_address = f"{commercial_row['Address']}, {commercial_row['City']}, {commercial_row['State']}, {zip}"
#     #   distance = calculate_distance(employee_address, commercial_address)
#     #   distances.append((distance, commercial_index))
#     # # Sort distances in ascending order
#     # distances.sort(key=lambda x: x[0])
#     #
#     # # Assign addresses based on closest locations
#     # for _ in range(addresses_per_employee):
#     #   if distances:
#     #     closest_index = distances.pop(0)[1]
#     #     assignments[employee_row["names"]].append(commercial_df.iloc[closest_index])
#
#   return assignments
#
#
# def main():
#   excel_file = 'Addresses1.xlsx'
#   xls = pd.ExcelFile(excel_file)
#
#   commercial_df = pd.read_excel(xls, 'Commercial')
#   employee_df = pd.read_excel(xls, 'Employee')
#
#   addresses_per_employee = 2
#
#   # Create a Chrome driver instance
#   driver = webdriver.Chrome(service=service, options=chrome_options)
#   assignments = assign_addresses(commercial_df, employee_df, addresses_per_employee, driver)
#   # Delete all cookies
#   driver.delete_all_cookies()
#   # Close the browser
#   driver.quit()
#
#   # data = []
#   # for employee_name, assigned_addresses in assignments.items():
#   #   for address in assigned_addresses:
#   #     data.append({
#   #       "Employee Name": employee_name,
#   #       "Address": address["address"],
#   #       "City": address["city"],
#   #       "State": address["state"],
#   #       "Zip": address["zip"],
#   #     })
#   #
#   # df = pd.DataFrame(data)
#   # df.to_csv("Output.csv", index=False)
#
#
# main()









import requests

def geocode_address(address):
    # Replace YOUR_API_KEY with your actual API key from the Google Cloud Console
    api_key = "YOUR_API_KEY"
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        latitude = location["lat"]
        longitude = location["lng"]
        return latitude, longitude
    else:
        print("Geocoding failed with status:", data["status"])
        return None, None

# Example usage:
address = "1600 Amphitheatre Parkway, Mountain View, CA"
latitude, longitude = geocode_address(address)
print("Latitude:", latitude)
print("Longitude:", longitude)

