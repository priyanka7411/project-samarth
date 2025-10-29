# 🌾 Project Samarth

**Intelligent Q&A System for Indian Agricultural & Climate Data**

![Project Samarth Interface](screenshots/app-interface.png)

## 🎯 Overview
AI-powered system that answers natural language questions about Indian agriculture and climate using live data from data.gov.in APIs.

## ✨ Key Features
- 🔍 Real-time data fetching from government APIs
- 💬 Natural language query processing
- 🤖 AI-powered answers with source citations
- 📊 Automatic query analysis
- 🎨 Clean web interface

## 📊 Data Sources
- **Crop Production API**: 246,091 records (1997-2014)
- **Daily Rainfall API**: 3.4M+ records (2018-present)
- **Source**: data.gov.in

## ��️ Tech Stack
- Python 3.11+
- Streamlit (Web Interface)
- Groq AI (Free LLM)
- Pandas (Data Processing)

## 🚀 Quick Start
```bash
# Clone repository
git clone https://github.com/priyanka7411/project-samarth.git
cd project-samarth

# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "GROQ_API_KEY=your_key_here" > .env

# Run app
streamlit run app.py
```

## 💡 Example Questions

- "Compare rice production in Punjab and Tamil Nadu for 2013"
- "Show wheat production in Haryana for 2012"
- "What is the rainfall pattern in Kerala for 2020?"

## 🏗️ System Architecture

**Components:**
1. **Query Analyzer** - Extracts states, crops, years from questions
2. **Data Handler** - Fetches data from multiple data.gov.in APIs
3. **AI Engine** - Groq LLM generates natural language answers
4. **Web Interface** - Streamlit-based UI with query history

**Data Flow:**
```
User Query → Query Analysis → API Fetch → AI Generation → Answer + Citations
```

## 🎯 Design Decisions

- **Real-time API fetching**: Ensures accuracy, no local storage needed
- **Free Groq API**: Better data sovereignty vs paid services  
- **Source citations**: Every answer includes data.gov.in API references
- **Modular architecture**: Easy to add new data sources

## 🎥 Demo Video
[Watch 2-minute demo](https://www.loom.com/share/96c8455fcc5b4af5af186af3423eeb66)

## 👩‍💻 Author
Priyanka - Built for data-driven agricultural insights

---
**Powered by data.gov.in APIs | Built with ❤️**
