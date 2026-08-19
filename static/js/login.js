function validateForm(){

    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    if (email=="" || password==""){
    alert("All fields are required");
    return false;
}
return true;
}