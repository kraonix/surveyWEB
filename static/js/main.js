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

                <label>Gender</label>
                <select id="gender">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>

                <label>Work-Life Balance Rating</label>
                <input id="wlb_val" type="number" min="1" max="5" placeholder="1–5">

                <label>Daily Study Hours</label>
                <input id="daily_study" type="number">

                <label>Screen Time (hrs)</label>
                <input id="screen_time" type="number">

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
            gender: document.getElementById("gender").value,
            wlb_rating: Number(document.getElementById("wlb_val").value),
            daily_study: Number(document.getElementById("daily_study").value),
            screen_time: Number(document.getElementById("screen_time").value),
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

        document.getElementById("exp-prediction-box").innerHTML = `
            <div class="prediction-card">
                <h3>Estimated Monthly Expenditure</h3>
                <p class="pred-value">₹${Math.round(data.prediction)}</p>
                <h4>Model Accuracy</h4>
                <p class="acc-value">${(data.accuracy * 100).toFixed(2)}%</p>
            </div>
        `;
    };

});
