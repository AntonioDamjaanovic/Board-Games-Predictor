// Initialize select2 on multi-select elements
$(document).ready(function () {
    $('.select-multi').select2({
        placeholder: "Select options",
        closeOnSelect: false,
        width: '100%'
    });
});

// Handle form submission
document.getElementById("predict-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const payload = {};
    formData.forEach((value, key) => {
        if (payload[key]) {
            // handle multi-select
            if (!Array.isArray(payload[key])) {
                payload[key] = [payload[key]];
            }
            payload[key].push(value);
        } else {
            payload[key] = value;
        }
    });

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.getElementById("prediction-result").innerText = "Predicting...";

    try {
        const response = await fetch("https://your-api-url/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        document.getElementById("prediction-result").innerText =
            `Predicted rating: ${data.prediction}`;

    } catch (error) {
        document.getElementById("prediction-result").innerText =
            "Prediction failed. Try again.";
        console.error(error);
    }
});