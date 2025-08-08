document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector("button[type='submit']");
    btn.addEventListener("click", function (e) {
        e.preventDefault();

        const inputs = document.querySelectorAll("input, select, textarea");
        const formData = {};

        inputs.forEach(input => {
            if (input.type === "radio") {
                if (input.checked) {
                    formData[input.name] = input.id;
                }
            } else if (input.type === "checkbox") {
                formData[input.name] = input.checked;
            } else {
                if (input.name || input.id) {
                    formData[input.name || input.id] = input.value;
                }
            }
        });

        console.log("Formulario capturado como JSON:", JSON.stringify(formData, null, 2));
    });
});