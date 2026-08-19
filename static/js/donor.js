function validateForm() {

    let fullName = document.getElementById("fullName").value.trim();
    let bloodgroup = document.getElementById("bloodgroup").value;
    let age = parseInt(document.getElementById("age").value);
    let gender = document.getElementById("gender").value;
    let contact = document.getElementById("contact").value.trim();
    let email = document.getElementById("email").value.trim();
    let state = document.getElementById("state").value;
    let city = document.getElementById("city").value;
    let pin = document.getElementById("pin").value;
    let lastdonationdate = document.getElementById("lastdonationdate").value.trim();
    let availability = document.getElementById("availability").value;

    if (
        fullName == "" || bloodgroup == "" || gender == "" || contact == "" || email == "" || state == "" || city == "" || pin == "" ||
        lastdonationdate == "" || availability == ""
    ) {
        alert("All fields are required.");
        return false;
    }

    if (isNaN(age)) {
        alert("Please enter age.");
        return false;
    }

    return true;
}