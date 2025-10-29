import os
from groq import Groq
from data_handler import DataGovAPI
from query_analyzer import QueryAnalyzer
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class IntelligentQASystem:
    """Main AI Q&A System for agricultural and climate data"""
    
    def __init__(self):
        self.data_api = DataGovAPI()
        self.query_analyzer = QueryAnalyzer()
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
    def fetch_relevant_data(self, analysis: dict) -> dict:
        """Fetch data based on query analysis"""
        result = {
            'crop_data': None,
            'rainfall_data': None,
            'sources': []
        }
        
        states = analysis['states']
        crops = analysis['crops']
        years = analysis['years']
        
        # Adjust years for crop data (only goes to 2014)
        crop_year = None
        if years:
            # Use the most recent year available (2014 or earlier)
            crop_year = min(years[0], 2014) if years[0] <= 2014 else 2014
        else:
            crop_year = 2014  # Default to most recent
        
        # Fetch crop data if crops mentioned
        if crops and states:
            print(f"📊 Fetching crop data for {crops} in {states} (year: {crop_year})...")
            for state in states[:2]:  # Limit to 2 states for speed
                for crop in crops[:2]:  # Limit to 2 crops
                    df = self.data_api.fetch_crop_data(
                        state=state, 
                        crop=crop, 
                        year=crop_year,
                        limit=200
                    )
                    if df is not None and len(df) > 0:
                        result['crop_data'] = df if result['crop_data'] is None else pd.concat([result['crop_data'], df])
                        result['sources'].append(f"Crop Production API (data.gov.in) - {state}, {crop}, {crop_year}")
        
        # Fetch rainfall data if states mentioned
        if states:
            # Use requested year or default to 2020
            rain_year = years[0] if years else 2020
            print(f"🌧️ Fetching rainfall data for {states} (year: {rain_year})...")
            for state in states[:2]:
                df = self.data_api.fetch_rainfall_data(
                    state=state,
                    year=rain_year,
                    limit=300
                )
                if df is not None and len(df) > 0:
                    result['rainfall_data'] = df if result['rainfall_data'] is None else pd.concat([result['rainfall_data'], df])
                    result['sources'].append(f"Daily District Rainfall API (data.gov.in) - {state}, {rain_year}")
        
        return result
    
    def analyze_data(self, data: dict, analysis: dict) -> str:
        """Analyze fetched data and generate summary"""
        summary = []
        
        # Analyze crop data
        if data['crop_data'] is not None and not data['crop_data'].empty:
            crop_df = data['crop_data']
            summary.append(f"Crop Data Summary:")
            summary.append(f"- Total records: {len(crop_df)}")
            summary.append(f"- States: {crop_df['state_name'].unique().tolist()}")
            summary.append(f"- Crops: {crop_df['crop'].unique().tolist()}")
            summary.append(f"- Districts: {crop_df['district_name'].nunique()}")
            if 'production_' in crop_df.columns:
                # Group by state for comparison
                state_production = crop_df.groupby('state_name')['production_'].sum()
                summary.append(f"\nProduction by State:")
                for state, prod in state_production.items():
                    summary.append(f"  - {state}: {prod:,.0f} tonnes")
                
                # Top districts
                district_production = crop_df.groupby(['state_name', 'district_name'])['production_'].sum().sort_values(ascending=False).head(3)
                summary.append(f"\nTop 3 Districts:")
                for (state, district), prod in district_production.items():
                    summary.append(f"  - {district}, {state}: {prod:,.0f} tonnes")
        
        # Analyze rainfall data
        if data['rainfall_data'] is not None and not data['rainfall_data'].empty:
            rain_df = data['rainfall_data']
            summary.append(f"\n\nRainfall Data Summary:")
            summary.append(f"- Total records: {len(rain_df)}")
            summary.append(f"- States: {rain_df['State'].unique().tolist()}")
            if 'Avg_rainfall' in rain_df.columns:
                # Average by state
                state_rainfall = rain_df.groupby('State')['Avg_rainfall'].mean()
                summary.append(f"\nAverage Rainfall by State:")
                for state, rain in state_rainfall.items():
                    summary.append(f"  - {state}: {rain:.2f} mm")
                
                # Monthly breakdown if available
                if 'Month' in rain_df.columns:
                    monthly_rain = rain_df.groupby(['State', 'Month'])['Avg_rainfall'].mean().unstack(fill_value=0)
                    summary.append(f"\nMonthly rainfall patterns available for detailed analysis")
        
        return "\n".join(summary)
    
    def generate_answer(self, query: str, data_summary: str, sources: list) -> str:
        """Generate natural language answer using Groq AI"""
        
        prompt = f"""You are an AI assistant analyzing Indian agricultural and climate data from data.gov.in APIs.

User Question: {query}

Available Data Summary:
{data_summary}

Data Sources:
{chr(10).join(['- ' + s for s in sources])}

Based on the data summary above, provide a clear, accurate answer to the user's question. 
- Always cite the specific data sources used
- Provide specific numbers and comparisons from the data
- If comparing states, highlight key differences
- If the data is insufficient, clearly state what's available and what's missing
- Keep the answer concise but informative (max 200 words)"""

        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful data analyst specializing in Indian agriculture and climate data. Always cite sources and provide specific numbers."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating answer: {e}"
    
    def answer_question(self, query: str) -> dict:
        """Main method to answer user questions"""
        print(f"\n{'='*60}")
        print(f"Question: {query}")
        print(f"{'='*60}\n")
        
        # Step 1: Analyze query
        print("🔍 Analyzing question...")
        analysis = self.query_analyzer.analyze(query)
        print(f"Query type: {analysis['query_type']}")
        print(f"Detected states: {analysis['states']}")
        print(f"Detected crops: {analysis['crops']}")
        print(f"Detected years: {analysis['years']}\n")
        
        # Step 2: Fetch relevant data
        data = self.fetch_relevant_data(analysis)
        
        # Step 3: Analyze data
        print("\n📈 Analyzing data...")
        data_summary = self.analyze_data(data, analysis)
        print(data_summary)
        
        # Step 4: Generate answer
        print("\n🤖 Generating answer...\n")
        answer = self.generate_answer(query, data_summary, data['sources'])
        
        return {
            'question': query,
            'answer': answer,
            'sources': data['sources'],
            'analysis': analysis
        }


# Test the system
if __name__ == "__main__":
    system = IntelligentQASystem()
    
    # Test with a year that has data
    question = "Compare rice production in Punjab and Tamil Nadu for 2014"
    
    result = system.answer_question(question)
    
    print("\n" + "="*60)
    print("FINAL ANSWER:")
    print("="*60)
    print(result['answer'])
    print("\n" + "="*60)
    print("SOURCES:")
    print("="*60)
    for source in result['sources']:
        print(f"✓ {source}")