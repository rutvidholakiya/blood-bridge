function validateForm() {

    let patientname = document.getElementById("patientname").value.trim();
    let bloodgroup = document.getElementById("bloodgroup").value;
    let unit = parseInt(document.getElementById("unit").value);
    let age = parseInt(document.getElementById("age").value);
    let gender = document.getElementById("gender").value;
    let contact = document.getElementById("contact").value.trim();
    let email = document.getElementById("email").value.trim();
    let hospitalname = document.getElementById("hospitalname").value.trim();
    let hospitaladdress = document.getElementById("hospitaladdress").value.trim();
    let city = document.getElementById("city").value;
    let requireddate = document.getElementById("requireddate").value.trim();
    let emergency = document.getElementById("emergency").value;

    if (
        patientname == "" || bloodgroup == "" || gender == "" || contact == "" || email == "" || hospitalname == "" || hospitaladdress == "" || city == "" ||
        requireddate == "" || emergency == ""
    ) {
        alert("All fields are required.");
        return false;
    }

    if (isNaN(unit)) {
        alert("Please enter required units.");
        return false;
    }

    if (isNaN(age)) {
        alert("Please enter age.");
        return false;
    }

    return true;
}