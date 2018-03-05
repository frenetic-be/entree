$(function(){
    $("input[name=projectname]")[0].oninvalid = function () {
        if (this.value === ""){
            this.setCustomValidity("Project name cannot be empty");
        } else {
            this.setCustomValidity("Invalid project name: project names cannot contain spaces, must start by a letter and can only contain letters, numbers and underscores");
        }

    };
});

$("#entree-form").submit(function(e){
    $(".alert")
        .removeClass("alert-danger alert-success")
        .addClass("alert-success")
        .text("Yay! You're good to go. Thank you for using entree.")
        .show();
});

function displayError(msg){
    $(".alert")
        .removeClass("alert-danger alert-success")
        .addClass("alert-danger")
        .text(msg)
        .show();
}