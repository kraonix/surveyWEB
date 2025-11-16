import pandas as pd
import plotly.express as px
import plotly.io as pio
from flask import Flask, render_template, request, jsonify
from services.income_service import IncomePredictorService


app = Flask(__name__)
pio.templates.default = "plotly_white"
income_service = IncomePredictorService()

@app.route("/predict/income", methods=["POST"])
def predict_income():
    data = request.json

    age = float(data.get("age"))
    study = float(data.get("study_hours"))
    year = data.get("academic_year")

    try:
        pred = income_service.predict(age, study, year)
        return jsonify({
            "predicted_income": round(pred, 2),
            "accuracy": 0.6271
        })
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ---------------- EXPENDITURE PREDICTION ----------------
@app.route("/predict/expenditure", methods=["POST"])
def predict_expenditure():
    try:
        data = request.json

        monthly_income = float(data["income"])
        gender = data["gender"]
        wlb = float(data["wlb_rating"])
        study = float(data["daily_study"])
        screen = float(data["screen_time"])
        eat = data["eat_out_frequency"]
        academic = data["academic_year"]
        accommodation = data["accommodation"]
        part_time = data["part_time"]

        from services.expenditure_service import ExpenditureService
        svc = ExpenditureService()

        pred = svc.predict(
            monthly_income,
            study,
            screen,
            wlb,
            eat,
            gender,
            academic,
            accommodation,
            part_time
        )

        return jsonify({
            "prediction": round(pred, 2),
            "accuracy": 0.8757
        })

    except Exception as e:
        print("🔥 EXPENDITURE ERROR:", e)
        return jsonify({"error": str(e)}), 500






def preprocess_eating_frequency(df):
        mapping = {
        "Never": 0,
        "1 time": 1,
        "1-2 times": 1.5,
        "2-3 times": 2.5,
        "3-4 times": 3.5,
        "4-5 times": 4.5,
        "5+ times": 5,
        "Often": 4,
        "Rarely": 1,
        "Sometimes": 2.5,
        }

        df["eat_out_frequency_numeric"] = df["eat_out_frequency"].map(mapping)
        df["exp_food"] = df["exp_food"].clip(lower=0, upper=20000)

        return df


# -------------------- Data Loader -----------------------
def load_data():
    df = pd.read_csv("student_survey_data.csv")
    df.columns = df.columns.str.strip()

    # Rename columns for easier use
    df = df.rename(columns={
        "On average, how many hours do you spend on academic activities (classes, studying, assignments) per week?": "weekly_academic_hours",
        "How many hours do you study daily (outside classes)?": "daily_study_hours",
        "How would you rate your overall satisfaction with your current work-life balance?": "wlb_rating",
        "What is your primary source of income (if any)?": "income_source",
        "Average monthly allowance / income (₹)": "monthly_income",
        "Approximately, what is your monthly expenditure on the following categories? [Rent/Accommodation]": "exp_rent",
        "Approximately, what is your monthly expenditure on the following categories? [Utilities (electricity, internet, etc.)]": "exp_utilities",
        "Approximately, what is your monthly expenditure on the following categories? [Groceries/Food]": "exp_food",
        "Approximately, what is your monthly expenditure on the following categories? [Transportation]": "exp_transport",
        "Approximately, what is your monthly expenditure on the following categories? [Academic Supplies (books, stationery)]": "exp_supplies",
        "Approximately, what is your monthly expenditure on the following categories? [Social/Entertainment]": "exp_entertainment",
        "Approximately, what is your monthly expenditure on the following categories? [Personal Care]": "exp_care",
        "Approximately, what is your monthly expenditure on the following categories? [Other]": "exp_other",
        "How often do you eat out or order takeout per week?": "eat_out_frequency",
        "What’s your average screen time per day (hrs)?": "screen_time",
        "Do you participate in any part-time work / freelancing?": "part_time_work"
    })

    # List of all money-related fields
    money_cols = [
        "monthly_income", "exp_rent", "exp_utilities", "exp_food",
        "exp_transport", "exp_supplies", "exp_entertainment",
        "exp_care", "exp_other"
    ]

    
    def clean_money(value):
        if pd.isna(value):
            return None

        value = str(value).strip()

        # Remove currency + commas
        value = value.replace("₹", "").replace(",", "").strip()

        # Patterns:
        # "< 5000" → 5000 (upper bound)
        # "> 30000" → 30000 (lower bound)
        # "5000 - 10000" → take AVERAGE
        if "<" in value:
            return float(value.replace("<", "").strip())

        if ">" in value:
            return float(value.replace(">", "").strip())

        if "-" in value:
            low, high = value.split("-")
            return (float(low.strip()) + float(high.strip())) / 2

        return float(value)

    # Apply cleaning to all money columns
    for col in money_cols:
        df[col] = df[col].apply(clean_money)

    # Convert screen time to numeric
    df["screen_time"] = pd.to_numeric(df["screen_time"], errors="coerce")

    # Convert study hours to numeric
    df["daily_study_hours"] = pd.to_numeric(df["daily_study_hours"], errors="coerce")

    # Fix duplicates
    df = df.drop_duplicates()

    return df



# -------------------- Main Pages -------------------------

@app.route('/')
def home():
    return render_template('landing_page.html')


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")  




# -------------------- Dynamic Graph Loader -------------------------

@app.route('/graph/<chart_id>')
def load_graph(chart_id):
    df = load_data()
    fig = None

    # --- 1. Predictions Page ---
    if chart_id == "predictions":
        return render_template("graphs/predictions.html")

    # --- 2. Data Overview (Pie Chart) ---
    if chart_id == "data_overview":
        gender_counts = df["Gender"].value_counts()
        labels = gender_counts.index.tolist()
        values = gender_counts.values.tolist()

        return render_template("graphs/chartjs_pie.html",
                           labels=labels,
                           values=values,
                           title="Gender Distribution")


    # --- 3. Academic Hours vs Daily Study Hours ---
    elif chart_id == "academic_hours":
    # Prepare data for Chart.js
        males = df[df["Gender"] == "Male"]
        females = df[df["Gender"] == "Female"]

        chart_data = {
            "title": "Weekly Academic Hours vs Daily Study Hours",
            "datasets": [
                {
                    "label": "Male",
                    "data": [
                        {"x": float(x), "y": float(y)}
                        for x, y in zip(males["weekly_academic_hours"], males["daily_study_hours"])
                ],
                "backgroundColor": "rgba(54, 162, 235, 0.8)",
            },
            {
                "label": "Female",
                "data": [
                    {"x": float(x), "y": float(y)}
                    for x, y in zip(females["weekly_academic_hours"], females["daily_study_hours"])
                ],
                "backgroundColor": "rgba(255, 99, 132, 0.8)",
            },
        ],
        "x_label": "Weekly Academic Hours",
        "y_label": "Daily Study Hours"
    }

        return render_template("graphs/scatter_chart.html", **chart_data)


    # --- 4. Food Expenditure vs Eating Frequency ---
    elif chart_id == "food_vs_eating":

        df = preprocess_eating_frequency(df)

        import numpy as np

        males = df[df["Gender"] == "Male"]
        females = df[df["Gender"] == "Female"]

        clean_df = df.dropna(subset=["eat_out_frequency_numeric", "exp_food"])
        X = clean_df["eat_out_frequency_numeric"].astype(float).values
        Y = clean_df["exp_food"].astype(float).values

        if len(X) > 1:
            m, b = np.polyfit(X, Y, 1)
            x_line = np.linspace(min(X), max(X), 50)
            y_line = m * x_line + b

            trendline = [{"x": float(x), "y": float(y)} for x, y in zip(x_line, y_line)]
        else:
            trendline = []

        chart_data = {
        "title": "Eating Frequency vs Monthly Food Expenditure",
        "datasets": [
            {
                "label": "Male",
                "data": [
                    {"x": float(x), "y": float(y)}
                    for x, y in zip(males["eat_out_frequency_numeric"], males["exp_food"])
                ],
                "backgroundColor": "rgba(54, 162, 235, 0.8)"
            },
            {
                "label": "Female",
                "data": [
                    {"x": float(x), "y": float(y)}
                    for x, y in zip(females["eat_out_frequency_numeric"], females["exp_food"])
                ],
                "backgroundColor": "rgba(255, 99, 132, 0.8)"
            },
            {
                "label": "Trendline",
                "data": trendline,
                "type": "line",
                "borderColor": "white",
                "borderWidth": 3,
                "pointRadius": 0
            }
        ],
        "x_label": "Eating Out Frequency (per week)",
        "y_label": "Monthly Food Expenditure (₹)"
        }

        return render_template("graphs/scatter_chart.html", **chart_data)


   # --- 5. Work-Life Balance vs Academic Load ---
    elif chart_id == "wlb_vs_academic_load":

        males = df[df["Gender"] == "Male"]
        females = df[df["Gender"] == "Female"]

        chart_data = {
        "title": "Weekly Academic Hours vs Work-Life Balance",
        "datasets": [
            {
                "label": "Male",
                "data": [
                    {"x": float(x), "y": float(y)}
                    for x, y in zip(males["weekly_academic_hours"], males["wlb_rating"])
                ],
                "backgroundColor": "rgba(54, 162, 235, 0.8)"
            },
            {
                "label": "Female",
                "data": [
                    {"x": float(x), "y": float(y)}
                    for x, y in zip(females["weekly_academic_hours"], females["wlb_rating"])
                ],
                "backgroundColor": "rgba(255, 99, 132, 0.8)"
            }
        ],
        "x_label": "Weekly Academic Hours",
        "y_label": "Work-Life Balance Rating"
    }

        return render_template("graphs/scatter_chart.html", **chart_data)


    # --- 6. Screen Time vs WLB ---
    elif chart_id == "screen_time":
    # Group by screen_time and gender
        grouped = (
        df.groupby(["screen_time", "Gender"])["wlb_rating"]
        .mean()
        .reset_index()
        .sort_values("screen_time")
    )

    # Unique x values
        labels = sorted(df["screen_time"].dropna().unique().tolist())

    # Male values
        male_data = grouped[grouped["Gender"] == "Male"]
        male_y = [male_data[male_data["screen_time"] == x]["wlb_rating"].iloc[0]
              if x in male_data["screen_time"].values else None
              for x in labels]

    # Female values
        female_data = grouped[grouped["Gender"] == "Female"]
        female_y = [female_data[female_data["screen_time"] == x]["wlb_rating"].iloc[0]
                if x in female_data["screen_time"].values else None
                for x in labels]

        chart_data = {
        "title": "Screen Time vs Work-Life Balance (Line Chart)",
        "labels": labels,
        "datasets": [
            {
                "label": "Male",
                "data": male_y,
                "borderColor": "rgba(54, 162, 235, 1)",
                "backgroundColor": "rgba(54, 162, 235, 0.3)",
                "borderWidth": 3,
                "tension": 0.3
            },
            {
                "label": "Female",
                "data": female_y,
                "borderColor": "rgba(255, 99, 132, 1)",
                "backgroundColor": "rgba(255, 99, 132, 0.3)",
                "borderWidth": 3,
                "tension": 0.3
            }
        ],
        "x_label": "Screen Time (hours per day)",
        "y_label": "Work-Life Balance Rating"
    }

        return render_template("graphs/line_chart.html", **chart_data)


    # --- 7. Accommodation Type vs Rent ---
    elif chart_id == "monthly_rent":

        categories = df["Which of the following best describes your primary accommodation?"].dropna().unique().tolist()

        data = []
        for cat in categories:
            vals = df[df["Which of the following best describes your primary accommodation?"] == cat]["exp_rent"].dropna().tolist()

            data.append({
            "type": "box",
            "y": vals,
            "name": cat,
            "marker": {"color": "rgba(255, 255, 255, 0.6)"},
            "line": {"color": "white"},
            "boxmean": True
        })

        return render_template(
        "graphs/plotly_box.html",
        title="Accommodation Type vs Monthly Rent",
        plot_data=data
        )




    # --- 8. Income Source vs Income Amount ---
    elif chart_id == "income_vs_monthly":
        import numpy as np

        df_clean = df.dropna(subset=["income_source", "monthly_income"])

    # Create income bins
        bins = [0, 5000, 10000, 15000, 20000, 30000, 50000]
        labels = ["0-5k", "5k-10k", "10k-15k", "15k-20k", "20k-30k", "30k-50k"]

        df_clean["income_bin"] = pd.cut(df_clean["monthly_income"], bins=bins, labels=labels)

    # Pivot table for heatmap
        pivot = df_clean.pivot_table(
            index="income_source",
            columns="income_bin",
            values="monthly_income",
            aggfunc="count",
            fill_value=0
            )

        heatmap_data = {
        "z": pivot.values.tolist(),
        "x": pivot.columns.tolist(),
        "y": pivot.index.tolist(),
        "title": "Income Source vs Monthly Income (Heatmap)"
        }

        return render_template("graphs/heatmap.html", **heatmap_data)


    # --- 9. Academic Year vs Expenditure ---
    elif chart_id == "academic_year_exp":

    # Clean academic year labels
        df["What is your current academic year?"] = df["What is your current academic year?"].astype(str)

    # Group and calculate average expenditure
        grouped = (
        df.groupby("What is your current academic year?")["exp_food"]
        .mean()
        .reset_index()
    )

        labels = grouped["What is your current academic year?"].tolist()
        values = grouped["exp_food"].round(2).tolist()

        chart_data = {
        "title": "Academic Year vs Average Monthly Food Expenditure",
        "labels": labels,
        "values": values,
        "y_label": "Avg Monthly Food Expenditure (₹)"
    }

        return render_template("graphs/bar_chart.html", **chart_data)


    # --- 10. Part-Time Work vs WLB ---
    elif chart_id == "part_time_vs_wlb":

        grouped = (
        df.groupby("part_time_work")["wlb_rating"]
        .mean()
        .reset_index()
    )

        labels = grouped["part_time_work"].tolist()
        values = grouped["wlb_rating"].round(2).tolist()

        chart_data = {
        "title": "Part-Time Work vs Work-Life Balance Rating",
        "labels": labels,
        "values": values,
        "y_label": "Average WLB Rating"
    }

        return render_template("graphs/bar_chart.html", **chart_data)



    # If no chart matched:
        if fig is None:
            return "<p>No graph available for this selection.</p>"

    # Convert figure to HTML
        graph_html = graph_html = fig.to_html(full_html=False, include_plotlyjs=False, include_mathjax=False, config={"responsive": True})
        return render_template("graphs/graph_tile.html", graph=graph_html)



# -------------------- Run App -------------------------

if __name__ == '__main__':
    app.run(debug=True)
