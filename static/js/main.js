document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('prediction-form');
    const resultEl = document.getElementById('prediction-result');

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Stop the page from reloading

        // 1. Get data from the form
        const formData = new FormData(form);
        const data = {
            age: formData.get('age'),
            study_hours: formData.get('study-hours'),
            income: formData.get('income'),
        };

        // 2. Send data to the Flask API
        fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            // 3. Display the prediction
            resultEl.textContent = result.prediction;
        })
        .catch(error => {
            console.error('Error:', error);
            resultEl.textContent = 'Error making prediction.';
        });
    });
});