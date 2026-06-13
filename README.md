# 🛒 E-Commerce Sentiment & Pricing Engine

**AI-powered dynamic pricing recommendations based on customer sentiment analysis**

<div align="center">

📊 [Live Dashboard](https://ecommerce-sentiment-pricing-mdndwngpuggu4jpsyfajrp.streamlit.app/) | 🐙 [GitHub Repo](https://github.com/ani-1129/ecommerce-sentiment-pricing) | 💼 [LinkedIn](https://linkedin.com/in/yourprofile)

</div>

---

## 🎯 **Overview**

This project analyzes customer reviews and order data to generate **AI-driven pricing recommendations**. By leveraging sentiment analysis, it identifies which products should increase or decrease prices based on customer satisfaction scores.

### **Key Features:**
- ✅ **Sentiment Analysis** - Convert ratings to sentiment scores (-1 to +1)
- ✅ **Dynamic Pricing Engine** - AI recommendations with % change percentages
- ✅ **Interactive Dashboard** - 5 pages with 15+ Plotly charts
- ✅ **Real-time Filtering** - Filter by category, product, rating range
- ✅ **Review Feed** - AI-powered sentiment classification
- ✅ **Product Deep Dive** - Individual product analytics

---

## 🚀 **Live Demo**

**👉 Access the Dashboard:** [E-Commerce Sentiment Dashboard](https://ecommerce-sentiment-pricing-mdndwngpuggu4jpsyfajrp.streamlit.app/)

### **Dashboard Preview:**
![Dashboard Overview](https://img.shields.io/badge/Dashboard-Live-blue)

**Pages:**
1. 📊 **Overview** - KPIs, sentiment donut, rating histogram, product sentiment
2. 💰 **Pricing Engine** - Price recommendations vs current prices
3. 💬 **Reviews** - AI sentiment analysis feed with filtering
4. 📦 **Orders** - Order analytics and revenue trends
5. 🔍 **Product Deep Dive** - Individual product analytics

---

## 🛠️ **Technology Stack**

### **Backend & Data:**
- 🐍 **Python 3.14** - Main programming language
- 📊 **Pandas** - Data manipulation and aggregation
- 🔢 **NumPy** - Numerical computations
- 🗄️ **PostgreSQL 15** - Database storage
- 🔴 **Redis Streams** - Real-time data streaming
- 📦 **dbt Core** - Data transformations

### **AI & ML:**
- 🤖 **Ollama (llama3.2)** - Local LLM for sentiment analysis
- ✨ **Sentiment Scoring** - Custom mapping: 5⭐=0.92, 4⭐=0.60, 3⭐=0.05, 2⭐=-0.50, 1⭐=-0.88

### **Dashboard & Visualization:**
- 📱 **Streamlit** - Interactive web dashboard
- 📊 **Plotly** - 15+ interactive charts
- 🎨 **Custom CSS** - Dark theme UI design

### **Utilities:**
- 🔄 **faker** - Mock data generation
- 🔐 **python-dotenv** - Environment configuration
- 🔄 **tenacity** - Retry logic
- 🔁 **retry** - Error handling

---

## 📦 **Architecture**
