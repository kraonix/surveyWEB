# 📊 SurveyWEB — Interactive Student Finance & Lifestyle Analytics Platform  
A full-stack open-source project that analyzes student lifestyle, academics, and financial patterns using ML-based prediction models and interactive visual dashboards.

---

## 🚀 Features

### 🔹 **1. Interactive Dashboard**
- Clean UI with sidebar navigation  
- Dynamic graphs (Chart.js + Plotly)  
- Student insights from survey data  
- Auto-loading visualizations

### 🔹 **2. Machine Learning Prediction Models**
Includes 3 ML models:
- **Income Predictor**
- **Expenditure Forecast**
- **Lifestyle Balance Model**
- **Study Pattern Model** *(coming soon)*

All models trained using student survey data with preprocessing, encoding & error handling.

### 🔹 **3. Clean Modular Architecture**
- `/models` → ML model training scripts  
- `/services` → Model loading & prediction logic  
- `/templates` → HTML templates  
- `/static` → UI logic (JS) & Styling (CSS)
- `/utils` → Data loading & preprocessing utilities
- `app.py` → Main Flask server  
- `config.py` → Application configuration

---

## 🧠 Tech Stack

### **Frontend**
- HTML5  
- CSS3 (Dark theme UI + custom components)  
- JavaScript (vanilla)  
- Chart.js  
- Plotly.js  

### **Backend**
- Python 3.x  
- Flask (REST API + server)  
- Pandas (data cleaning & preprocessing)  
- NumPy  
- Scikit-Learn (ML models)  

### **ML Models**
- Random Forest Regressors  
- Regression pipelines  
- LightGBM/CatBoost (optional future upgrades)  

### **Data**
- Student lifestyle, academics & finance survey CSV  
- Feature engineering & preprocessing scripts included  

---

## 📂 Project Structure

```
surveyWEB/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
├── student_survey_data.csv # Data source
├── models/                 # Trained ML models
├── services/               # Prediction logic services
├── static/                 # Static assets (CSS, JS)
├── templates/              # HTML templates
├── tests/                  # Unit tests
└── utils/                  # Utility functions (data loading)
```

---

## 🛠 Installation & Setup

### **1️⃣ Clone the repository**
```bash
git clone https://github.com/yourusername/surveyWEB.git
cd surveyWEB
```

### **2️⃣ Install Dependencies**
Ensure you have Python installed. Then run:
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Application**
```bash
python app.py
```
The application will start on `http://127.0.0.1:5000/`.

---

## 🎯 How to Use

### **Dashboard**
- Navigate through sidebar options  
- Visual insights update dynamically  
- Graphs load using **AJAX + Chart.js + Plotly**  

### **Prediction Models**
- Go to **Predictions** section
- Choose a model (Income, Expenditure, Lifestyle)
- Enter required values  
- Live prediction appears instantly  
- Model accuracy score is shown below the output  

---

## 🧩 Contributing

Contributions are welcome!  

Feel free to open:
- **Issues**
- **Feature requests**
- **Pull requests**

Please follow clean coding practices and keep:
- ML models inside `/models`
- Prediction logic inside `/services`

---

## 📄 License
This project is open-source under the **MIT License**.

---

## 💛 Acknowledgements
Thanks to the contributors and students whose survey responses power the analytics.

---

## ⭐ Star the repo if you like it!
