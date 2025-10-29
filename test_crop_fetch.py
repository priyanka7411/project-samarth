from data_handler import DataGovAPI

api = DataGovAPI()

print("Testing crop data fetch...")
print("\nTest 1: Punjab Rice 2020")
df1 = api.fetch_crop_data(state="Punjab", crop="Rice", year=2020, limit=100)
if df1 is not None:
    print(f"Found {len(df1)} records")
    print(df1.head())
else:
    print("No data found")

print("\n\nTest 2: Punjab Rice 2019")
df2 = api.fetch_crop_data(state="Punjab", crop="Rice", year=2019, limit=100)
if df2 is not None:
    print(f"Found {len(df2)} records")
    print(df2.head())
else:
    print("No data found")

print("\n\nTest 3: Punjab Rice (no year filter)")
df3 = api.fetch_crop_data(state="Punjab", crop="Rice", limit=100)
if df3 is not None:
    print(f"Found {len(df3)} records")
    print("\nAvailable years:", sorted(df3['crop_year'].unique()))
    print(df3.head())
else:
    print("No data found")