import os
import streamlit as st
import pandas as pd
from groq import Groq
from data_handler import DataGovAPI
from query_analyzer import QueryAnalyzer
from dotenv import load_dotenv


class IntelligentQASystem:
    """Main AI Q&A System for agricultural and climate data."""

    def __init__(self):
        # Load local .env if present
        load_dotenv()

        self.data_api = DataGovAPI()
        self.query_analyzer = QueryAnalyzer()

        # --- Load API key (Streamlit secrets > environment variable) ---
        api_key = None

        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
        elif os.getenv("GROQ_API_KEY"):
            api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            st.error("⚠️ GROQ_API_KEY not found! Please add it to .env or Streamlit secrets.")
            st.stop()

        # Initialize Groq client
        self.groq_client = Groq(api_key=api_key)

    # ------------------------------------------------------------------
    def fetch_relevant_data(self, analysis: dict) -> dict:
        """Fetch data from APIs based on query analysis."""
        result = {"crop_data": None, "rainfall_data": None, "sources": []}

        states = analysis["states"]
        crops = analysis["crops"]
        years = analysis["years"]

        # Handle crop data (available up to 2014)
        crop_year = 2014
        if years:
            crop_year = min(years[0], 2014)

        if crops and states:
            print(f"📊 Fetching crop data for {crops} in {states} (year: {crop_year})...")
            for state in states[:2]:
                for crop in crops[:2]:
                    df = self.data_api.fetch_crop_data(
                        state=state,
                        crop=crop,
                        year=crop_year,
                        limit=200,
                    )
                    if df is not None and len(df) > 0:
                        result["crop_data"] = (
                            df if result["crop_data"] is None else pd.concat([result["crop_data"], df])
                        )
                        result["sources"].append(
                            f"Crop Production API (data.gov.in) - {state}, {crop}, {crop_year}"
                        )

        # Handle rainfall data (default year 2020)
        if states:
            rain_year = years[0] if years else 2020
            print(f"🌧️ Fetching rainfall data for {states} (year: {rain_year})...")
            for state in states[:2]:
                df = self.data_api.fetch_rainfall_data(state=state, year=rain_year, limit=300)
                if df is not None and len(df) > 0:
                    result["rainfall_data"] = (
                        df if result["rainfall_data"] is None else pd.concat([result["rainfall_data"], df])
                    )
                    result["sources"].append(
                        f"Daily District Rainfall API (data.gov.in) - {state}, {rain_year}"
                    )

        return result

    # ------------------------------------------------------------------
    def analyze_data(self, data: dict, analysis: dict) -> str:
        """Generate a text summary of the fetched data."""
        summary = []

        # Crop data
        if data["crop_data"] is not None and not data["crop_data"].empty:
            crop_df = data["crop_data"]
            summary.append("Crop Data Summary:")
            summary.append(f"- Total records: {len(crop_df)}")
            summary.append(f"- States: {crop_df['state_name'].unique().tolist()}")
            summary.append(f"- Crops: {crop_df['crop'].unique().tolist()}")
            summary.append(f"- Districts: {crop_df['district_name'].nunique()}")

            if "production_" in crop_df.columns:
                state_production = crop_df.groupby("state_name")["production_"].sum()
                summary.append("\nProduction by State:")
                for state, prod in state_production.items():
                    summary.append(f"  - {state}: {prod:,.0f} tonnes")

                district_production = (
                    crop_df.groupby(["state_name", "district_name"])["production_"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(3)
                )
                summary.append("\nTop 3 Districts:")
                for (state, district), prod in district_production.items():
                    summary.append(f"  - {district}, {state}: {prod:,.0f} tonnes")

        # Rainfall data
        if data["rainfall_data"] is not None and not data["rainfall_data"].empty:
            rain_df = data["rainfall_data"]
            summary.append("\n\nRainfall Data Summary:")
            summary.append(f"- Total records: {len(rain_df)}")
            summary.append(f"- States: {rain_df['State'].unique().tolist()}")

            if "Avg_rainfall" in rain_df.columns:
                state_rainfall = rain_df.groupby("State")["Avg_rainfall"].mean()
                summary.append("\nAverage Rainfall by State:")
                for state, rain in state_rainfall.items():
                    summary.append(f"  - {state}: {rain:.2f} mm")

        return "\n".join(summary)

    # ------------------------------------------------------------------
    def generate_answer(self, query: str, data_summary: str, sources: list) -> str:
        """Use Groq model to generate a natural language answer."""
        prompt = f"""You are an AI assistant analyzing Indian agricultural and climate data from data.gov.in APIs.

User Question: {query}

Available Data Summary:
{data_summary}

Data Sources:
{chr(10).join(['- ' + s for s in sources])}

Provide a clear, factual, and concise answer (max 200 words).
Always cite the specific data sources and mention key comparisons.
If data is incomplete, explain what’s missing.
"""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a data analyst specializing in Indian agriculture and climate data. Always cite sources and use clear numbers."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=500,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Error generating answer: {e}"

    # ------------------------------------------------------------------
    def answer_question(self, query: str) -> dict:
        """End-to-end pipeline: analyze → fetch → summarize → answer."""
        print(f"\n{'='*60}")
        print(f"Question: {query}")
        print(f"{'='*60}\n")

        print("🔍 Analyzing question...")
        analysis = self.query_analyzer.analyze(query)
        print(f"Query type: {analysis['query_type']}")
        print(f"Detected states: {analysis['states']}")
        print(f"Detected crops: {analysis['crops']}")
        print(f"Detected years: {analysis['years']}\n")

        data = self.fetch_relevant_data(analysis)

        print("\n📈 Analyzing data...")
        data_summary = self.analyze_data(data, analysis)
        print(data_summary)

        print("\n🤖 Generating answer...\n")
        answer = self.generate_answer(query, data_summary, data["sources"])

        return {
            "question": query,
            "answer": answer,
            "sources": data["sources"],
            "analysis": analysis,
        }


# ----------------------------------------------------------------------
# Local test block
# ----------------------------------------------------------------------
if __name__ == "__main__":
    system = IntelligentQASystem()
    question = "Compare rice production in Punjab and Tamil Nadu for 2013"
    result = system.answer_question(question)

    print("\n" + "=" * 60)
    print("FINAL ANSWER:")
    print("=" * 60)
    print(result["answer"])
    print("\n" + "=" * 60)
    print("SOURCES:")
    print("=" * 60)
    for source in result["sources"]:
        print(f"✓ {source}")
