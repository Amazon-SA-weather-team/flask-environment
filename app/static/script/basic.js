function UpdateClick() {
    document.getElementById("UpdateForm").style.display = "block";
    document.getElementById("UpdateButton").style.display = "none";

}

function wheatherchange() {
    document.getElementById("fiveDays").style.display = "block";
    document.getElementById("currentWeather").style.display = "none";
}

function wheatherchange_back() {
    document.getElementById("currentWeather").style.display = "block";
    document.getElementById("fiveDays").style.display = "none";
}