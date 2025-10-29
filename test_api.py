import requests
import json

# Test the crop production API
API_URL = "https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de"
API_KEY = "579b464db66ec23bdd000001955640b6e396463b64c7bc5545fd6530"

# Simple test - fetch 5 records
params = {
    'api-key': API_KEY,
    'format': 'json',
    'limit': 5
}

print("Testing API connection...")
print("Please wait...\n")

try:
    response = requests.get(API_URL, params=params)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n✓ SUCCESS! API is working!")
        print(f"\nTotal records available: {data.get('total', 'Unknown')}")
        print(f"Records fetched: {len(data.get('records', []))}")
        
        print("\n--- Sample Record ---")
        if data.get('records'):
            first_record = data['records'][0]
            for key, value in first_record.items():
                print(f"{key}: {value}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"✗ Error occurred: {e}")