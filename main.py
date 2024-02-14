from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd

# Read data from Excel file with two sheets
excel_file = 'Addresses.xlsx'
xls = pd.ExcelFile(excel_file)

# Read data from 'Commercial' sheet
commercial_df = pd.read_excel(xls, 'Commercial')

# Read data from 'Employee' sheet
employee_df = pd.read_excel(xls, 'Employee')

# Initialize geocoder
geolocator = Nominatim(user_agent="my_geocoder")


# Function to geocode address
def geocode_address(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


# Geocode commercial addresses
commercial_df['Latitude'], commercial_df['Longitude'] = zip(*commercial_df['Address'].apply(geocode_address))

# Geocode employee addresses
employee_df['Latitude'], employee_df['Longitude'] = zip(*employee_df['Address'].apply(geocode_address))

# Function to calculate distance between two locations
def calculate_distance(commercial_location, employee_location):
    return geodesic(commercial_location, employee_location).miles

# Iterate over each employee and find nearest commercial locations
num_nearest_locations = 3  # Example: Number of nearest commercial locations to assign to each employee
assignments = {}
for _, employee_row in employee_df.iterrows():
    employee_address = (employee_row['Latitude'], employee_row['Longitude'])
    nearest_commercial_locations = commercial_df.apply(lambda x: (x['Latitude'], x['Longitude']), axis=1)
    nearest_commercial_locations = nearest_commercial_locations.apply(lambda x: calculate_distance(x, employee_address))
    nearest_commercial_locations = nearest_commercial_locations.sort_values().index[:num_nearest_locations]
    assignments[employee_row['Name']] = nearest_commercial_locations.tolist()

# Output or save the assignments
for employee, locations in assignments.items():
    print(f"Assignments for {employee}:")
    for location_idx in locations:
        print(commercial_df.loc[location_idx, ['Address', 'City', 'State', 'Zip']])
    print()
