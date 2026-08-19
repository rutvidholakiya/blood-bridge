function validateForm() {

    let fullName = document.getElementById("fullName").value.trim();
    let email = document.getElementById("email").value;
    let contact = document.getElementById("contact").value.trim();
    let subject = document.getElementById("subject").value;
    let message = document.getElementById("message").value.trim();

    if (
        fullName == "" || email == "" || contact == "" || subject == "" || message == ""
    ) {
        alert("All fields are required.");
        return false;
    }

    return true;
}