import time
import pandas as pd
from googlemaps import Client

# API key (REPLACE with your own API key)
api_key = "AIzaSyCNVmTF4f5lgJSkhUDJY4q4PeDIl-d6mkY"
count_down = 0


# Define function for geocoding
def geocode_address(address):
  lat = lng = None
  try:
    global count_down
    count_down = count_down + 1
    client = Client(key=api_key)
    geocode_result = client.geocode(address)
    if geocode_result:
      location = geocode_result[0]["geometry"]["location"]
      lat = location["lat"]
      lng = location["lng"]
  except Exception as ex:
    print(ex)
  finally:
    return lat, lng


# Define function for distance calculation
def calculate_distance(lat1, lng1, lat2, lng2):
    try:
        global count_down
        count_down = count_down + 1
        client = Client(key=api_key)
        directions_result = client.directions(origin=(lat1, lng1), destination=(lat2, lng2), mode="driving")
        if directions_result:
            distance = directions_result[0]["legs"][0]["distance"]["value"]
        else:
            distance = None  # or any default value you prefer
    except Exception as ex:
        print(ex)
        distance = None  # or any default value you prefer
    finally:
        return distance


# Function generates an output csv file
def write_output(assignments):
  try:
    # Prepare data for new CSV file
    data = []
    for employee_name, assigned_addresses in assignments.items():
      for address in assigned_addresses:
        data.append({
          "Employee Name": employee_name,
          "Address": address["Address"],
          "City": address["City"],
          "State": address["State"],
          "Zip": address["Zip"],
        })
    # Create a new pandas DataFrame and write it to a CSV file
    df = pd.DataFrame(data)
    df.to_csv("Assignments.csv", index=False)
  except Exception as ex:
    print(ex)
  finally:
    return


# Function reads the excel file and returns dataframes
def read_file(excel_file):
  try:
    addresses_per_employee = 0
    commercial_df = employee_df = ""
    xls = pd.ExcelFile(excel_file)

    commercial_df = pd.read_excel(xls, 'Commercial')
    employee_df = pd.read_excel(xls, 'Employee')

    # Remove duplicate rows from commercial_df
    commercial_df = commercial_df.drop_duplicates()

    # Remove duplicate rows from employee_df
    employee_df = employee_df.drop_duplicates()

    # Reset the indexes if needed
    commercial_df = commercial_df.reset_index(drop=True)
    employee_df = employee_df.reset_index(drop=True)

    # Specify the number of addresses to assign per employee
    addresses_per_employee = int(int(commercial_df.shape[0]) / int(employee_df.shape[0]))
  except Exception as ex:
    print(ex)
  finally:
    return commercial_df, employee_df, addresses_per_employee


# Main driver function
def main():
  try:
    commercial_df, employee_df, addresses_per_employee = read_file("Addresses_1000.xlsx")

    if addresses_per_employee > 0:
      # Create an empty dictionary to store assignments
      assignments = {}
      try:
        nm = ""
        for employee_index, employee_row in employee_df.iterrows():
          employee_address = f"{employee_row['Address']}, {employee_row['City']}, {employee_row['State']}, {employee_row['Zip']}"
          assignments[employee_row["Name"]] = []

          # Geocode employee address
          employee_lat, employee_lng = geocode_address(employee_address)
          if employee_lat is None or employee_lng is None:
            continue
          distances = []
          print("#########################################################")
          print("Extracting addresses for employee " + employee_row['Name'])
          print("#########################################################")
          # Calculate distances for each commercial address
          for commercial_index, commercial_row in commercial_df.iterrows():
            if count_down % 10 == 0:
              time.sleep(1)
            commercial_address = f"{commercial_row['Address']}, {commercial_row['City']}, {commercial_row['State']}, {commercial_row['Zip']}"

            # Geocode commercial address
            commercial_lat, commercial_lng = geocode_address(commercial_address)
            if commercial_lat is None or commercial_lng is None:
              continue

            try:
              # Calculate distance and store in a tuple
              distance = calculate_distance(employee_lat, employee_lng, commercial_lat, commercial_lng)
              if not distance:
                continue
              distance_tuple = (distance, commercial_index)
              # Add distance tuple to a list for sorting
              distances = assignments[employee_row["Name"]]
              distances.append(distance_tuple)
            except:
              pass

          # Sort distances in ascending order
          distances.sort(key=lambda x: x[0])

          indeces =[]
          # Assign closest addresses based on limit
          assignments[employee_row['Name']] = []
          for _ in range(addresses_per_employee):
            if distances:
              closest_index = distances.pop(0)[1]
              assignments[employee_row["Name"]].append(commercial_df.iloc[closest_index])
              indeces.append(closest_index)

          # Remove rows based on the list of indices
          for x in indeces:
              commercial_df = commercial_df.drop(x, axis=0)
          # Reset the indexes
          commercial_df = commercial_df.reset_index(drop=True)
          print(assignments[employee_row['Name']])
          print("-------------------------------------------")
          nm = employee_row['Name']
        if commercial_df.shape[0] < addresses_per_employee:
          for i in range(commercial_df.shape[0]):
            assignments[nm].append(commercial_df.iloc[i])
      except Exception as ex:
        print(ex)
      finally:
        if assignments:
          write_output(assignments)
        else:
          print("No addresses assigned!!!")
  except Exception as ex:
    print(ex)


# Calling main driver function
main()
