import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, request, jsonify

# --- Setup ---
app = Flask(__name__)
pio.templates.default = "plotly_white" # Light theme for the dashboard

# --- Data Loading Function (No Change) ---
def load_data():
    """Loads and cleans the survey data from the CSV."""
    df = pd.read_csv('student_survey_data.csv')
    df.columns = df.columns.str.strip()
    df['Average monthly allowance / income (₹)'] = df['Average monthly allowance / income (₹)'].str.replace(r'[₹,]', '', regex=True)
    return df

# --- Page Routes ---

@app.route('/')
def home():
    """Renders the new wireframe landing page."""
    # This route now just serves your static wireframe page.
    return render_template('landing_page.html')

@app.route('/dashboard')
def dashboard():
    """Renders the main dashboard with all visualizations."""
    df = load_data()

    # --- Create Visualizations with Plotly ---
    fig_gender = px.pie(df, names='Gender', title='Gender Distribution', hole=0.3)
    fig_year = px.bar(df, x='What is your current academic year?', title='Student Count by Academic Year', labels={'What is your current academic year?': 'Academic Year'})
    fig_accom = px.bar(df, y='Which of the following best describes your primary accommodation?', title='Accommodation Types', orientation='h', labels={'Which of the following best describes your primary accommodation?': 'Accommodation Type'})
    fig_study_vs_screen = px.scatter(df, x='How many hours do you study daily (outside classes)?', y='What’s your average screen time per day (hrs)?', color='Gender', title='Daily Study Hours vs. Screen Time', labels={'How many hours do you study daily (outside classes)?': 'Daily Study Hours', 'What’s your average screen time per day (hrs)?': 'Daily Screen Time (hrs)'})

    # --- Convert Plots to HTML ---
    plot_gender = fig_gender.to_html(full_html=False, include_plotlyjs='cdn')
    plot_year = fig_year.to_html(full_html=False, include_plotlyjs=False)
    plot_accom = fig_accom.to_html(full_html=False, include_plotlyjs=False)
    plot_study_screen = fig_study_vs_screen.to_html(full_html=False, include_plotlyjs=False)

    return render_template(
        'dashboard.html',
        plot_gender=plot_gender,
        plot_year=plot_year,
        plot_accom=plot_accom,
        plot_study_screen=plot_study_screen
    )

@app.route('/prediction')
def prediction():
    """Renders the prediction model page."""
    return render_template('prediction.html')


# --- API for Prediction Model (No Change) ---
@app.route('/api/predict', methods=['POST'])
def predict():
    """Handles prediction requests."""
    data = request.json
    print(f"Received data for prediction: {data}")
    
    # Placeholder: Just return a dummy prediction
    prediction_result = "₹10,000 - ₹20,000" 
    
    return jsonify({'prediction': prediction_result})

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)