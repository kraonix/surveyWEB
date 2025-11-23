document.addEventListener("DOMContentLoaded", () => {

    const items = document.querySelectorAll(".sidebar-item");
    const container = document.getElementById("chart-container");

    /* AUTO-SELECT PREDICTIONS */
    setTimeout(() => {
        const defaultItem = document.querySelector('[data-target="predictions"]');
        if (defaultItem) {
            defaultItem.classList.add("selected");
            loadModelMenu();
        }
    }, 80);


    /* SIDEBAR CLICK HANDLER */
    items.forEach(item => {
        item.addEventListener("click", () => {
            items.forEach(i => i.classList.remove("selected"));
            item.classList.add("selected");

            const target = item.getAttribute("data-target");

            if (target === "predictions") {
                loadModelMenu();
                return;
            }

            container.innerHTML = `
                <div class="viz-tile dynamic-tile">
                    <h2>${item.innerText}</h2>
                    <p>Loading chart...</p>
                </div>
            `;

            fetch(`/graph/${target}`)
                .then(res => res.text())
                .then(html => {
                    container.innerHTML = html;

                    const scripts = container.querySelectorAll("script");
                    scripts.forEach(oldScript => {
                        const newScript = document.createElement("script");
                        if (oldScript.src) newScript.src = oldScript.src;
                        else newScript.textContent = oldScript.textContent;
                        document.body.appendChild(newScript);
                        oldScript.remove();
                    });
                });
        });
    });


    /* --- MODEL MENU --- */
    window.loadModelMenu = function () {
        container.innerHTML = `
            <div class="viz-tile">
                <h2 style="margin-bottom:20px;">Choose a Prediction Model</h2>

                <div class="model-grid">
                    <button class="model-btn" onclick="loadModel('income')">Income Prediction</button>
                    <button class="model-btn" onclick="loadModel('expenditure')">Expenditure Forecast</button>
                    <button class="model-btn" onclick="loadModel('lifestyle')">Lifestyle Balance Model</button>
                    <button class="model-btn" onclick="loadModel('study')">Study Pattern Model</button>
                </div>
            </div>
        `;
    };


    /* --- LOAD SPECIFIC MODEL UI --- */
    window.loadModel = function (type) {

        const back = `<button class="back-btn" onclick="loadModelMenu()">← Back</button>`;
        let ui = "";

        /* ---------------- INCOME MODEL ---------------- */
        if (type === "income") {
            ui = `
            <div class="viz-tile">
                ${back}
                <h2>Income Prediction</h2>

                <label>Age</label>
                <input id="age" type="number" placeholder="Enter age">

                <label>Daily Study Hours</label>
                <input id="study_hours" type="number" placeholder="Study hours">

                <label>Academic Year</label>
                <select id="academic_year">
                    <option value="1st Year">1st Year</option>
                    <option value="2nd Year">2nd Year</option>
                    <option value="3rd Year">3rd Year</option>
                    <option value="4th Year">4th Year</option>
                </select>

                <button class="submit-btn" onclick="predictIncome()">Predict</button>

                <div id="prediction-box" class="prediction-output"></div>
            </div>
            `;
        }

        /* ---------------- EXPENDITURE MODEL (OPTION B) ---------------- */
        if (type === "expenditure") {
            ui = `
            <div class="viz-tile">
                ${back}
                <h2>Expenditure Forecast</h2>

                <label>Monthly Income (₹)</label>
                <input id="inc_val" type="number" placeholder="e.g. 15000">

                <label>Eat Out Frequency</label>
                <select id="eat_freq">
                    <option value="Never">Never</option>
                    <option value="1 time">1 time</option>
                    <option value="1-2 times">1–2 times</option>
                    <option value="2-3 times">2–3 times</option>
                    <option value="3-4 times">3–4 times</option>
                    <option value="4-5 times">4–5 times</option>
                    <option value="5+ times">5+ times</option>
                    <option value="Rarely">Rarely</option>
                    <option value="Sometimes">Sometimes</option>
                    <option value="Often">Often</option>
                </select>

                <label>Academic Year</label>
                <select id="acad_year">
                    <option value="1st Year">1st Year</option>
                    <option value="2nd Year">2nd Year</option>
                    <option value="3rd Year">3rd Year</option>
                    <option value="4th Year">4th Year</option>
                </select>

                <label>Accommodation</label>
                <select id="accommodation">
                    <option value="Hostel">Hostel</option>
                    <option value="PG">PG</option>
                    <option value="Flat/Apartment">Flat/Apartment</option>
                    <option value="With Family">With Family</option>
                </select>

                <label>Part-Time Work</label>
                <select id="part_time">
                    <option value="No">No</option>
                    <option value="Yes">Yes</option>
                </select>

                <button class="submit-btn" onclick="predictExpenditure()">Predict</button>

                <div id="exp-prediction-box" class="prediction-output"></div>
            </div>
            `;
        }

        /* ---------------- LIFESTYLE BALANCE MODEL ---------------- */
        if (type === "lifestyle") {
            ui = `
            <div class="viz-tile">
                ${back}
                <h2>Lifestyle Balance Predictor</h2>
                <p style="margin-bottom: 20px; opacity: 0.8;">Predict your work-life balance rating (1-5 scale) based on your lifestyle factors</p>

                <label>Age</label>
                <input id="lifestyle_age" type="number" placeholder="Enter age">

                <label>Gender</label>
                <select id="lifestyle_gender">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>

                <label>Academic Year</label>
                <select id="lifestyle_academic_year">
                    <option value="1st Year">1st Year</option>
                    <option value="2nd Year">2nd Year</option>
                    <option value="3rd Year">3rd Year</option>
                    <option value="4th Year">4th Year</option>
                </select>

                <label>Weekly Academic Hours</label>
                <input id="weekly_academic" type="number" placeholder="Hours per week" step="0.5">

                <label>Daily Study Hours (outside classes)</label>
                <input id="daily_study_lifestyle" type="number" placeholder="Hours per day" step="0.5">

                <label>Screen Time (hours per day)</label>
                <input id="screen_time_lifestyle" type="number" placeholder="Hours per day" step="0.5">

                <label>Part-Time Work</label>
                <select id="part_time_lifestyle">
                    <option value="No">No</option>
                    <option value="Yes">Yes</option>
                </select>

                <button class="submit-btn" onclick="predictLifestyle()">Predict Balance</button>

                <div id="lifestyle-prediction-box" class="prediction-output"></div>
            </div>
            `;
        }

        container.innerHTML = ui;
    };


    /* ---------------- TOAST FUNCTION ---------------- */
    window.showToast = function (msg) {
        let toast = document.createElement("div");
        toast.className = "toast-msg";
        toast.innerText = msg;

        document.body.appendChild(toast);

        setTimeout(() => { toast.classList.add("show"); }, 10);
        setTimeout(() => {
            toast.classList.remove("show");
            setTimeout(() => toast.remove(), 300);
        }, 2500);
    };


    /* ---------------- INCOME PREDICTION ---------------- */
    window.predictIncome = async function () {
        const age = Number(document.getElementById("age").value);
        const study_hours = Number(document.getElementById("study_hours").value);
        const academic_year = document.getElementById("academic_year").value;

        if (!age || !study_hours) {
            showToast("⚠️ Please fill all fields.");
            return;
        }

        const res = await fetch("/predict/income", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ age, study_hours, academic_year })
        });

        const data = await res.json();
        document.getElementById("prediction-box").innerHTML = `
            <div class="prediction-card">
                <h3>Predicted Income</h3>
                <p class="pred-value">₹${data.predicted_income}</p>
                <h4>Model Accuracy</h4>
                <p class="acc-value">${(data.accuracy * 100).toFixed(2)}%</p>
            </div>
        `;
    };


    /* ---------------- EXPENDITURE PREDICTION ---------------- */
    window.predictExpenditure = async function () {

        const payload = {
            income: Number(document.getElementById("inc_val").value),
            eat_out_frequency: document.getElementById("eat_freq").value,
            academic_year: document.getElementById("acad_year").value,
            accommodation: document.getElementById("accommodation").value,
            part_time: document.getElementById("part_time").value
        };

        if (Object.values(payload).some(v => v === "" || v === null || v === 0)) {
            showToast("⚠️ Please fill all fields.");
            return;
        }

        const res = await fetch("/predict/expenditure", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();

        let adviceColor = data.advice === "Spend less" ? "#ff6b6b" : "#00c89b";

        document.getElementById("exp-prediction-box").innerHTML = `
            <div class="prediction-card">
                <h3>Estimated Monthly Expenditure</h3>
                <p class="pred-value">₹${Math.round(data.prediction)}</p>
                <p style="color: ${adviceColor}; font-weight: bold; font-size: 1.2rem; margin-top: 10px;">${data.advice}</p>
                <h4>Model Accuracy</h4>
                <p class="acc-value">${(data.accuracy * 100).toFixed(2)}%</p>
            </div>
        `;
    };


    /* ---------------- LIFESTYLE BALANCE PREDICTION ---------------- */
    window.predictLifestyle = async function () {
        const weekly_academic = Number(document.getElementById("weekly_academic").value);
        const daily_study = Number(document.getElementById("daily_study_lifestyle").value);
        const screen_time = Number(document.getElementById("screen_time_lifestyle").value);
        const part_time = document.getElementById("part_time_lifestyle").value;
        const age = Number(document.getElementById("lifestyle_age").value);
        const academic_year = document.getElementById("lifestyle_academic_year").value;
        const gender = document.getElementById("lifestyle_gender").value;

        // Validate inputs
        if (!weekly_academic || !daily_study || !screen_time || !age) {
            const toast = document.getElementById("toast");
            if (toast) {
                toast.textContent = "⚠️ Please fill all fields.";
                toast.classList.add("show");
                setTimeout(() => toast.classList.remove("show"), 3000);
            } else {
                alert("⚠️ Please fill all fields.");
            }
            return;
        }

        const payload = {
            weekly_academic,
            daily_study,
            screen_time,
            part_time,
            age,
            academic_year,
            gender
        };

        // Show loading state
        const predictionBox = document.getElementById("lifestyle-prediction-box");
        predictionBox.innerHTML = '<div class="prediction-card"><p>Predicting...</p></div>';

        try {
            const res = await fetch("/predict/lifestyle", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            const data = await res.json();

            if (data.error) {
                const toast = document.getElementById("toast");
                if (toast) {
                    toast.textContent = "⚠️ " + data.error;
                    toast.classList.add("show");
                    setTimeout(() => toast.classList.remove("show"), 3000);
                } else {
                    alert("⚠️ " + data.error);
                }
                predictionBox.innerHTML = "";
                return;
            }

            if (!data.prediction && data.prediction !== 0) {
                throw new Error("No prediction returned from server");
            }

            const rating = parseFloat(data.prediction);
            let ratingText = "";
            let ratingColor = "";

            if (rating >= 4.5) {
                ratingText = "Excellent";
                ratingColor = "#00c89b";
            } else if (rating >= 3.5) {
                ratingText = "Good";
                ratingColor = "#82ced0";
            } else if (rating >= 2.5) {
                ratingText = "Moderate";
                ratingColor = "#93d6d5";
            } else if (rating >= 1.5) {
                ratingText = "Poor";
                ratingColor = "#a3ddda";
            } else {
                ratingText = "Very Poor";
                ratingColor = "#b3e5e0";
            }

            predictionBox.innerHTML = `
                <div class="prediction-card">
                    <h3>Predicted Work-Life Balance</h3>
                    <p class="pred-value" style="color: ${ratingColor};">${rating.toFixed(2)} / 5.0</p>
                    <p style="margin-top: 10px; font-size: 1.1rem; color: ${ratingColor};">${ratingText}</p>
                    <h4>Model Accuracy</h4>
                    <p class="acc-value">${((data.accuracy || 0.7058) * 100).toFixed(2)}%</p>
                </div>
            `;
        } catch (error) {
            console.error("Lifestyle prediction error:", error);
            const toast = document.getElementById("toast");
            if (toast) {
                toast.textContent = "⚠️ Error making prediction: " + error.message;
                toast.classList.add("show");
                setTimeout(() => toast.classList.remove("show"), 3000);
            } else {
                alert("⚠️ Error making prediction. Please try again.\n" + error.message);
            }
            predictionBox.innerHTML = '<div class="prediction-card"><p style="color: #a3ddda;">Error: Could not get prediction. Please check console for details.</p></div>';
        }
    };

});
