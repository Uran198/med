/* Project specific Javascript goes here. */
$(document).ready(function() {
    console.log("ready!");
    $("#upload_image").on('submit', function(e) {
        e.preventDefault();
        console.log("Submitted!");
        file = e.target.file;
        data = new FormData(e.target);
        $.ajax({
            // Probably not very good to hardcode it, maybe should use templates somehow
            // FIXME: THIS IS REALLY BAD
            url: '/en/questions/upload_image/',
            type: 'POST',
            data: data,
            cache: false,
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function(data) {
                console.log("Success");
                console.log(arguments);
                $('#id_text_ifr').contents().find('body').append('<img src="'+data['location']+'" />');
            },
            error: function() {
                console.log("Error");
                console.log(arguments);
            }
        });
    });
});
