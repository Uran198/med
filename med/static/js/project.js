/* Project specific Javascript goes here. */
$(document).ready(function() {
    console.log("ready!");
    $("#upload_image_form").on('submit', function(e) {
        e.preventDefault();
        console.log("Submitted!");
        file = e.target.file;
        data = new FormData(e.target);
        $.ajax({
            url: e.target.action,
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function(data) {
                console.log("Success");
                console.log(arguments);
                if (data['location']) {
                    $('#id_text_ifr').contents().find('body').append(
                            '<img width="400" height="400" src="'+data['location']+'" />');
                } else {
                    console.log(data['error']);
                }
            },
            error: function() {
                console.log("Error");
                console.log(arguments);
            }
        });
    });
});
