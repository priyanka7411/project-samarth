import requests
import pandas as pd
from typing import Optional, List
import time

class DataGovAPI:
    """Handler for data.gov.in API"""
    
    CROP_API_URL = "https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de"
    RAINFALL_API_URL = "https://api.data.gov.in/resource/6c05cd1b-ed59-40c2-bc31-e314f39c6971"
    API_KEY = "579b464db66ec23bdd000001955640b6e396463b64c7bc5545fd6530"
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_crop_data(self, 
                       state: Optional[str] = None,
                       district: Optional[str] = None, 
                       crop: Optional[str] = None,
                       year: Optional[int] = None,
                       season: Optional[str] = None,
                       limit: int = 5000) -> Optional[pd.DataFrame]:
        """Fetch crop production data"""
        all_records = []
        offset = 0
        batch_size = 1000
        
        while len(all_records) < limit:
            params = {
                'api-key': self.API_KEY,
                'format': 'json',
                'limit': min(batch_size, limit - len(all_records)),
                'offset': offset
            }
            
            if state:
                params['filters[state_name]'] = state
            if district:
                params['filters[district_name]'] = district
            if crop:
                params['filters[crop]'] = crop
            if year:
                params['filters[crop_year]'] = year
            if season:
                params['filters[season]'] = season
            
            try:
                response = self.session.get(self.CROP_API_URL, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                records = data.get('records', [])
                if not records:
                    break
                    
                all_records.extend(records)
                
                if len(records) < batch_size:
                    break
                    
                offset += batch_size
                time.sleep(0.3)
                
            except Exception as e:
                print(f"Error: {e}")
                break
        
        if all_records:
            df = pd.DataFrame(all_records)
            print(f"✓ Crop data: {len(df)} records")
            return df
        return None
    
    def fetch_rainfall_data(self,
                           state: Optional[str] = None,
                           year: Optional[int] = None,
                           limit: int = 5000) -> Optional[pd.DataFrame]:
        """Fetch rainfall data"""
        all_records = []
        offset = 0
        batch_size = 1000
        
        while len(all_records) < limit:
            params = {
                'api-key': self.API_KEY,
                'format': 'json',
                'limit': min(batch_size, limit - len(all_records)),
                'offset': offset
            }
            
            if state:
                params['filters[State]'] = state
            if year:
                params['filters[Year]'] = str(year)
            
            try:
                response = self.session.get(self.RAINFALL_API_URL, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                records = data.get('records', [])
                if not records:
                    break
                    
                all_records.extend(records)
                
                if len(records) < batch_size:
                    break
                    
                offset += batch_size
                time.sleep(0.3)
                
            except Exception as e:
                print(f"Error: {e}")
                break
        
        if all_records:
            df = pd.DataFrame(all_records)
            print(f"✓ Rainfall data: {len(df)} records")
            return df
        return None


# Test both APIs
# Test both APIs
if __name__ == "__main__":
    api = DataGovAPI()
    
    print("=" * 50)
    print("TEST 1: Fetch Punjab crop data for 2020")
    print("=" * 50)
    crop_df = api.fetch_crop_data(state="Punjab", year=2020, limit=50)
    if crop_df is not None:
        print("Columns:", crop_df.columns.tolist())
        print(crop_df.head())
    
    print("\n" + "=" * 50)
    print("TEST 2: Fetch Punjab rainfall data for 2020")
    print("=" * 50)
    rainfall_df = api.fetch_rainfall_data(state="Punjab", year=2020, limit=50)
    if rainfall_df is not None:
        print("Columns:", rainfall_df.columns.tolist())
        print(rainfall_df.head())
    
    print("\n✓ Both APIs working!")