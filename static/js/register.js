function validateForm(){

    let fullName = document.getElementById("fullname").value.trim();
    let username = document.getElementById("username").value.trim();
    let email = document.getElementById("email").value.trim();
    let contact = document.getElementById("contact").value.trim();
    let dob = document.getElementById("dob").value.trim();
    let gender = document.getElementById("gender").value;
    let bloodgroup = document.getElementById("bloodgroup").value;
    let password = document.getElementById("password").value.trim();
    let state = document.getElementById("state").value.trim();
    let city = document.getElementById("city").value.trim();
    let pin = document.getElementById("pin").value.trim();
    let role = document.getElementById("role").value;

    if (fullName=="" || username=="" || email=="" || contact=="" || dob=="" || gender=="" || bloodgroup=="" || password=="" || state == "" || 
        city=="" || pin=="" || role==""){
    alert("All fields are required");
    return false;
}
return true;
}
