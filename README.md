# 📊 AnalytixPro - Sales Data Analytics Dashboard

**AnalytixPro** is a powerful web application designed to analyze and visualize sales data efficiently. Built with **Flask and Python**, this dashboard provides insightful visualizations, statistical forecasting, and advanced filtering capabilities to help businesses make data-driven decisions.

---

## ✨ Features

- **📂 Interactive Data Upload**: Easily upload CSV files containing sales data.
- **📈 Dynamic Visualizations**:
  - Sales and Profit Trends
  - Quantity Analysis
  - Category-wise Distribution
  - Regional Performance
  - Correlation Analysis
- **📊 Advanced Analytics**:
  - Statistical Analysis
  - Time Series Forecasting
  - Key Performance Metrics
- **🔍 Filtering Capabilities**:
  - City
  - Region
  - Category
  - Year

---

## 🔧 Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **Statistical Modeling**: Statsmodels
- **Deployment**: Render

---

## 📂 Project Structure

```
Data_Ana/
├── analysis/
│   ├── data_preprocessing.py
│   ├── machine_learning.py
│   ├── statistical_analysis.py
│   └── visualization.py
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   └── prediction.html
├── utils/
│   ├── file_operations.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1️⃣ Clone the repository
```sh
git clone https://github.com/yourusername/Data_Ana.git
cd Data_Ana
```

### 2️⃣ Create a virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Flask application
```sh
python app.py
```

### 5️⃣ Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🌍 Deployed Application
The application is deployed and can be accessed at the following link: [AnalytixPro](https://analytixpro-2.onrender.com/)

---

## 📜 Data Format

The application expects a CSV file with the following columns:
- **Date**
- **City**
- **Region**
- **Category**
- **Sales**
- **Profit**
- **Quantity**

---

## 🔍 Features in Detail

### 📊 Data Analysis
- Comprehensive statistical analysis
- Time series decomposition
- Trend analysis
- Correlation studies

### 📈 Visualizations
- Interactive line charts
- Bar graphs
- Pie charts
- Heatmaps
- Distribution plots

### ⏳ Forecasting
- Sales forecasting
- Profit forecasting
- Trend analysis
- Seasonality detection

---

## ❤️ Acknowledgments

- Thanks to all contributors
- Inspired by the need for better sales data visualization
- Built with passion for data analytics
