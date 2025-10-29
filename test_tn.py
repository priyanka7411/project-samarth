from data_handler import DataGovAPI

api = DataGovAPI()

print("Testing Tamil Nadu Rice (all years)...")
df = api.fetch_crop_data(state="Tamil Nadu", crop="Rice", limit=100)

if df is not None:
    print(f"✓ Found {len(df)} records")
    print("\nAvailable years:", sorted(df['crop_year'].unique()))
    print("\nSample data:")
    print(df.head())
else:
    print("✗ No data found")