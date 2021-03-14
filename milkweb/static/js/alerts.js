document.getElementById("user_avatar").onclick = function () {
    document.getElementById("profile_alert").style.display = "block";
    let disalert = function () {
        document.getElementById("profile_alert").style.display = "none";
    };
    setTimeout(disalert, 5000);
};