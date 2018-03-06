$(function(){
    $("input[name=projectname]")[0].oninvalid = function () {
        if (this.value === ""){
            this.setCustomValidity("Project name cannot be empty");
        } else {
            this.setCustomValidity("Invalid project name: project names cannot contain spaces, must start by a letter and can only contain letters, numbers and underscores");
        }

    };
});

$("#entree-form").submit(function(){
    $(".alert")
        .removeClass("alert-danger alert-success")
        .addClass("alert-success")
        .text("Yay! You're good to go. Thanks for using entree.")
        .show();
});

function displayError(msg){
    $(".alert")
        .removeClass("alert-danger alert-success")
        .addClass("alert-danger")
        .text(msg)
        .show();
}

function hideAlert(){
    $('.alert').hide();
}

function getFiles(){
    if ($('#projectname').is(':invalid')) {
        $('.files').html('');
        return;
    }

    var projectType = $("#projecttype").val();
    var projectName = $("#projectname").val();
    var queryString = $.param({projectname: projectName});
    var baseURL = "/filestructure/" + projectType;
    var url = queryString === "" ? baseURL : baseURL + "?" + queryString;

    $.getJSON(url, function(data) {

        var dirs = data.dirs;
        var files = data.files;
        var cdirs = data.common_dirs;
        var cfiles = data.common_files;
        var filesAndDirs = [];
        // Transform object to array of files/dirs and their template names
        $.each(Object.assign({}, dirs, files), function(key, value){
            filesAndDirs.push([key, value]);
        });
        $.each(cdirs.concat(cfiles), function(index, value){
            filesAndDirs.push([value, value]);
        });
        filesAndDirs.sort(function(left, right){
            return left[1] < right[1] ? -1 : 1;
        });
        var items = [];
        var div,
            otherclass,
            tname,
            name,
            id,
            split,
            filename,
            prefix,
            level = 0,
            prevLevel = 0;

        $.each( filesAndDirs, function(index, nameArray) {
            tname = nameArray[0];
            name = nameArray[1];

            split = name.split('/');
            level = split.length;

            filename = "";
            for (var j=0; j<level-1; j++ ){
                filename += "<span class=\"spacer\"></span>";
            }
            filename += split[level-1];

            div = '';
            for (j=level; j<prevLevel; j++ ){
                div += '</div>\n';
            }

            if (tname in dirs){
                otherclass = ' dirs';
                div += '<div class="form-group dirgroup">\n';
            } else {
                otherclass = '';
            }

            prefix = 'cb_';
            if (cdirs.indexOf(tname) > -1 || cfiles.indexOf(tname) > -1) {
                prefix = 'cb_common_';
            }
            id = prefix + tname;
            div += '<div class="form-check">\n';
            div += '<input type="checkbox" class="form-check-input' + otherclass + '" id="' + id + '" name="' + id + '" checked>\n';
            div += '<label class="form-check-label' + otherclass + '" for="' + id + '">' + filename + '</label>\n';
            div += '</div>\n';

            prevLevel = level;

            items.push(div);
        });
        div = '';
        for (var j=level-1; j>0; j-- ){
            div += '</div>\n';
        }
        items.push(div);

        $('.files').html(items.join(''));

        $('input[type="checkbox"]').click(function(){
            var isChecked = $(this).prop('checked');
            var isDir = $(this).hasClass('dirs');
            // If it is a directory, check or uncheck all of its children
            if (isDir){
                $(this)
                    .closest('.dirgroup')
                    .find('input[type="checkbox"]')
                    .prop('checked', isChecked);
            }
            // If checked then all of its parent folders should be checked too
            if (isChecked){
                $(this)
                    .parents('.dirgroup')
                    .children('.form-check')
                    .children('input.dirs')
                    .prop('checked', true);
            }
        });

    });
}

$('#projectname').on("change keyup paste", getFiles);
$('#projecttype').on("change", getFiles);

$('input').on('change keyup paste', hideAlert);
$('#projecttype').on('change', hideAlert);