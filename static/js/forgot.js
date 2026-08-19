function validateForm() {
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value;
    let confirm = document.getElementById("confirmpassword").value;

    // Check if all fields are filled
    if (email === "" || password === "" || confirm === "") {
        alert("All fields are required.");
        return false;
    }

    // Email validation
    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    // Password match validation
    if (password !== confirm) {
        alert("Passwords do not match.");
        return false;
    }

    return true;
}