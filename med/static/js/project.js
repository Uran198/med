/* Project specific Javascript goes here. */


// max image size
var MAX_WIDTH = 600;
var MAX_HEIGHT = 600;

var dataURLToBlob = function(dataURL) {
    var BASE64_MARKER = ';base64,';
    if (dataURL.indexOf(BASE64_MARKER) == -1) {
        var parts = dataURL.split(',');
        var contentType = parts[0].split(':')[1];
        var raw = parts[1];

        return new Blob([raw], {type: contentType});
    }

    var parts = dataURL.split(BASE64_MARKER);
    var contentType = parts[0].split(':')[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;

    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], {type: contentType});
}

$(document).ready(function() {
    console.log("ready!");

    var reader = new FileReader();
    reader.onload = function(e) {
        var img = new Image();
        img.onload = function (e) {

            var canvas = $("#preview")[0];

            var width = img.width;
            var height = img.height;

            if (width > height) {
                if (width > MAX_WIDTH) {
                    height *= MAX_WIDTH / width;
                    width = MAX_WIDTH;
                }
            } else {
                if (height > MAX_HEIGHT) {
                    width *= MAX_HEIGHT / height;
                    height = MAX_HEIGHT;
                }
            }
            canvas.width = width;
            canvas.height = height;
            var ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);

            var dataurl = canvas.toDataURL("image/png");
            document.getElementById('src_holder').src = dataurl;
        }
        img.src = e.target.result;
    }

    var handleFiles = function(e) {
        console.log("In handleFiles");
        if (!e.target.files) {
            return;
        }
        var file = e.target.files[0];
        if (!file.type.match(/image.*/)) {
            return;
        }
        reader.readAsDataURL(file);
    };

    $("#id_file").on('change', handleFiles);

    $("#upload_image_form").on('submit', function(e) {
        $('#error').hide();
        $('progress').show();
        var prog = $('progress')[0];
        prog.value = "0";
        e.preventDefault();
        console.log("Submitted!");
        data = new FormData(e.target);
        data.append("file", dataURLToBlob(document.getElementById('src_holder').src), "blob.png");
        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                //Upload progress
                xhr.upload.addEventListener("progress", function(evt){
                    if (evt.lengthComputable) {
                        var percentComplete = evt.loaded / evt.total;
                        //Do something with upload progress
                        prog.value = percentComplete;
                    }
                }, false);
                return xhr;
            },
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
                            '<img src="'+data['location']+'" />');
                } else {
                    var $err = $('#error');
                    $err.text(data['error'].file[0]);
                    $err.show();
                    console.log(data['error']);
                }
                // make file uploading possible again
                e.target.reset();
                // reset source
                document.getElementById('src_holder').src = "";
            },
            error: function() {
                console.log("Error");
                console.log(arguments);
            }
        });
    });

    // Language selection
    $("#select_language_id").change(function(e) {
        $("#select_language_form_id").submit();
    });

    // Image enlargement
    $("img").click(function(e) {
        var im = e.target;
        var enl = $("#enlargedImage img");
        enl[0].src = im.src;
        $("#enlargedImage").show();
    });

    $("#enlargedImage").click(function(e) {
        $("#enlargedImage").hide();
    });
});
