import pandas as pd

# Load the data from the provided URL
url = "https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv"
data = pd.read_csv(url)

# Extract unique place_name and place_id values
unique_place_names = data['place_name'].unique()
unique_place_ids = data['place_id'].unique()

# Display the unique place names and ids
print("Unique Place Names:")
print(unique_place_names)

print("\nUnique Place IDs:")
print(unique_place_ids)

# Save to CSV if needed
place_names_df = pd.DataFrame({'place_name': unique_place_names})
place_ids_df = pd.DataFrame({'place_id': unique_place_ids})

# Save the unique values to CSV
place_names_df.to_csv('unique_place_names.csv', index=False)
place_ids_df.to_csv('unique_place_ids.csv', index=False)

