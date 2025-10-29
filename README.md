# 🌾 Project Samarth

Intelligent Q&A System for Indian Agricultural & Climate Data

## Overview
AI-powered system that answers natural language questions about Indian agriculture and climate using live data from data.gov.in APIs.

## Features
- Real-time data fetching from government APIs
- Natural language query processing
- AI-powered answer generation with source citations
- Clean web interface

## Data Sources
- **Crop Production API**: 246,091 records (1997-2014)
- **Daily Rainfall API**: 3.4M+ records (2018-present)

## Tech Stack
- Python 3.11+
- Streamlit (Web Interface)
- Groq AI (LLM)
- Pandas (Data Processing)

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usage
Ask questions like:
- "Compare rice production in Punjab and Tamil Nadu for 2013"
- "Show wheat production in Haryana for 2012"
- "What is the rainfall in Kerala for 2020?"

## Architecture
- **Data Handler**: Manages API calls and data fetching
- **Query Analyzer**: Extracts parameters from questions
- **AI Engine**: Generates natural language answers
- **Web Interface**: Streamlit-based UI

## Environment Variables
Create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
```
