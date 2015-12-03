/* Project specific Javascript goes here. */
$(document).ready(function() {
    console.log("ready!");
    $("#upload_image_form").on('submit', function(e) {
        e.preventDefault();
        console.log("Submitted!");
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
                    $('#error').hide();
                    $('#id_text_ifr').contents().find('body').append(
                            '<img width="400" height="400" src="'+data['location']+'" />');
                } else {
                    var $err = $('#error');
                    $err.text(data['error'].file[0]);
                    $err.show();
                    console.log(data['error']);
                }
                // make file uploading possible again
                e.target.reset();
            },
            error: function() {
                console.log("Error");
                console.log(arguments);
            }
        });
    });
});
