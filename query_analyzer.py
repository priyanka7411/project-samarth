import re
from typing import Dict, List, Optional

class QueryAnalyzer:
    """Analyzes user questions to extract parameters"""
    
    INDIAN_STATES = [
        "Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", 
        "Karnataka", "Bihar", "Assam", "Odisha", "Tamil Nadu",
        "Maharashtra", "Rajasthan", "Chhattisgarh", "Andhra Pradesh",
        "West Bengal", "Gujarat", "Telangana", "Kerala"
    ]
    
    COMMON_CROPS = [
        "Rice", "Wheat", "Sugarcane", "Cotton", "Maize", "Bajra",
        "Jowar", "Gram", "Tur", "Groundnut", "Soyabean", "Sunflower"
    ]
    
    def extract_states(self, query: str) -> List[str]:
        """Extract state names from query"""
        query_upper = query.title()
        found_states = []
        
        for state in self.INDIAN_STATES:
            if state.lower() in query.lower():
                found_states.append(state)
        
        return found_states
    
    def extract_crops(self, query: str) -> List[str]:
        """Extract crop names from query"""
        query_lower = query.lower()
        found_crops = []
        
        for crop in self.COMMON_CROPS:
            if crop.lower() in query_lower:
                found_crops.append(crop)
        
        return found_crops
    
    def extract_years(self, query: str) -> List[int]:
        """Extract years from query"""
        # Find 4-digit years
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', query)
        
        # Handle "last N years"
        last_n = re.search(r'last (\d+) years?', query.lower())
        if last_n:
            n = int(last_n.group(1))
            current_year = 2023  # Latest data year
            years = list(range(current_year - n + 1, current_year + 1))
        
        return [int(y) for y in years] if isinstance(years, list) and years and isinstance(years[0], str) else years
    
    def determine_query_type(self, query: str) -> str:
        """Determine the type of query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['compare', 'comparison', 'versus', 'vs']):
            return 'comparison'
        elif any(word in query_lower for word in ['trend', 'over time', 'decade', 'years']):
            return 'trend'
        elif any(word in query_lower for word in ['highest', 'lowest', 'maximum', 'minimum', 'top', 'bottom']):
            return 'ranking'
        elif any(word in query_lower for word in ['correlate', 'relationship', 'impact', 'affect']):
            return 'correlation'
        else:
            return 'general'
    
    def analyze(self, query: str) -> Dict:
        """Analyze query and extract all parameters"""
        return {
            'original_query': query,
            'query_type': self.determine_query_type(query),
            'states': self.extract_states(query),
            'crops': self.extract_crops(query),
            'years': self.extract_years(query)
        }


# Test it
if __name__ == "__main__":
    analyzer = QueryAnalyzer()
    
    test_queries = [
        "Compare rainfall in Punjab and Kerala for last 5 years",
        "What is the rice production trend in Tamil Nadu from 2015 to 2020?",
        "Which district in Maharashtra has highest wheat production in 2021?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = analyzer.analyze(query)
        print(f"Type: {result['query_type']}")
        print(f"States: {result['states']}")
        print(f"Crops: {result['crops']}")
        print(f"Years: {result['years']}")