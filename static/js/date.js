// function showDate() {

//     const today = new Date();

//     const days = [
//         "Sunday","Monday","Tuesday","Wednesday",
//         "Thursday","Friday","Saturday"
//     ];

//     const months = [
//         "January","February","March","April",
//         "May","June","July","August",
//         "September","October","November","December"
//     ];

//     document.getElementById("currentDate").innerHTML =
//         days[today.getDay()] + ", " +
//         today.getDate() + " " +
//         months[today.getMonth()] + " " +
//         today.getFullYear();
// }

// document.addEventListener("DOMContentLoaded", function () {
//     showDate();
// });

function updateDateTime() {

    const now = new Date();

    const days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];

    const day = days[now.getDay()];
    const date = now.getDate();
    const month = months[now.getMonth()];
    const year = now.getFullYear();

    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

    let ampm = hours >= 12 ? "PM" : "AM";

    hours = hours % 12;
    hours = hours ? hours : 12;

    minutes = String(minutes).padStart(2, '0');
    seconds = String(seconds).padStart(2, '0');

    document.getElementById("dateTime").innerHTML =
        `${day}, ${date} ${month} ${year} | ${hours}:${minutes}:${seconds} ${ampm}`;
}

setInterval(updateDateTime, 1000);
updateDateTime();