const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const passwordField = document.querySelector("#passwordField");
const passwordField2 = document.querySelector("#passwordField2");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "Show Password") {
        showPasswordToggle.textContent = "Hide Password";
        passwordField.setAttribute("type", "text");
        passwordField2.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "Show Password";
        passwordField.setAttribute("type", "password");
        passwordField2.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", { 
                body: JSON.stringify({  //endpoint
                    email: emailVal
                }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                if (data.email_error) {
                    submitBtn.disabled = true;   // if there is a error disable the button
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`; // display the error message in html
                } else {
                    submitBtn.removeAttribute("disabled"); //remove the error message
                }
            });
    }
});

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;

    usernameSuccessOutput.style.display = "block";
    
    usernameSuccessOutput.textContent = `${usernameVal}`;

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
                body: JSON.stringify({
                    username: usernameVal
                }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                usernameSuccessOutput.style.display = "none";
                if (data.username_error) {
                    usernameField.classList.add("is-invalid");
                    feedBackArea.style.display = "block";
                    feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
                    submitBtn.disabled = true;
                } else {
                    submitBtn.removeAttribute("disabled");
                }
            });
    }
});