document.addEventListener('DOMContentLoaded', function() {
    var username_error = document.getElementById("script").getAttribute("data-username_error");
    var password_error = document.getElementById("script").getAttribute("data-password_error");
    var email_error = document.getElementById("script").getAttribute("data-email_error");
    var confirm_error = document.getElementById("script").getAttribute("data-confirm_error");
    assign_class(username_error, email_error, password_error, confirm_error);
});

function assign_class(var1, var2, var3, var4) {
    if (var1.length >= 3){
        document.getElementById("username").className = "form-control is-invalid";
    }
    if (var2.length >= 3){
    	document.getElementById("email").className = "form-control is-invalid";
    }
    if (var3.length >= 3){
        document.getElementById("password").className = "form-control is-invalid";
    }
    if (var4.length >= 3){
    	document.getElementById("confirm").className = "form-control is-invalid";
    }
}
