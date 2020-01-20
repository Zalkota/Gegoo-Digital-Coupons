$(document).ready(function(){

    // setup session cookie data. This is Django-related
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // end session cookie data setup.



// declare an empty array for potential uploaded files
var fileItemList = []

// auto-upload on file input change.
$(document).on('change','.cfeproj-upload-file', function(event){
    var selectedFiles = $(this).prop('files');
    formItem = $(this).parent()
    $.each(selectedFiles, function(index, item){
        var myFile = verifyFileIsImageMovieAudio(item)
        if (myFile){
            uploadFile(myFile)
        } else {
            // alert("Some files are invalid uploads.")
        }
    })
    $(this).val('');

})



function verifyFileIsImageMovieAudio(file){
    // verifies the file extension is one we support.
    var extension = file.name.split('.').pop().toLowerCase(); //file.substr( (file.lastIndexOf('.') +1) );
    switch(extension) {
        case 'jpg':
        case 'png':
        case 'gif':
        case 'jpeg':
            return file
        case 'mov':
        case 'mp4':
        case 'mpeg4':
        case 'avi':
            return file
        case 'mp3':
            return file
        default:
            notAllowedFiles.push(file)
            return null
    }
};

function constructFormPolicyData(policyData, fileItem) {
   var contentType = fileItem.type != '' ? fileItem.type : 'application/octet-stream'
    var url = policyData.url
    var filename = policyData.filename
    var repsonseUser = policyData.user
    // var keyPath = 'www/' + repsonseUser + '/' + filename
    var keyPath = policyData.file_bucket_path
    var fd = new FormData()
    fd.append('key', keyPath + filename);
    fd.append('acl','private');
    fd.append('Content-Type', contentType);
    fd.append("AWSAccessKeyId", policyData.key)
    fd.append('Policy', policyData.policy);
    fd.append('filename', filename);
    fd.append('Signature', policyData.signature);
    fd.append('file', fileItem);
    return fd
}

function fileUploadComplete(fileItem, policyData){
    data = {
        uploaded: true,
        fileSize: fileItem.size,
        file: policyData.file_id,

    }
    $.ajax({
        method:"POST",
        data: data,
        url: "/api/files/complete/",
        success: function(data){
            displayItems(fileItemList)
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("An error occured, please refresh the page.")
        }
    })
}

function displayItems(fileItemList){
    var itemList = $('.item-loading-queue')
    itemList.html("")
    $.each(fileItemList, function(index, obj){
        var item = obj.file
        var id_ = obj.id
        var order_ = obj.order
        var html_ = "<div class=\"progress\">" +
          "<div class=\"progress-bar\" role=\"progressbar\" style='width:" + item.progress + "%' aria-valuenow='" + item.progress + "' aria-valuemin=\"0\" aria-valuemax=\"100\"></div></div>"
        itemList.append("<div>" + order_ + ") " + item.name + "<a href='#' class='srvup-item-upload float-right' data-id='" + id_ + ")'>X</a> <br/>" + html_ + "</div><hr/>")

    })
}


function uploadFile(fileItem){
        var policyData;
        var newLoadingItem;
        // get AWS upload policy for each file uploaded through the POST method
        // Remember we're creating an instance in the backend so using POST is
        // needed.
        $.ajax({
            method:"POST",
            data: {
                filename: fileItem.name
            },
            url: "/api/files/policy/",
            success: function(data){
                    policyData = data
            },
            error: function(data){
                alert("An error occured, please try again later")
            }
        }).done(function(){
            // construct the needed data using the policy for AWS
            var fd = constructFormPolicyData(policyData, fileItem)

            // use XML http Request to Send to AWS.
            var xhr = new XMLHttpRequest()

            // construct callback for when uploading starts
            xhr.upload.onloadstart = function(event){
                var inLoadingIndex = $.inArray(fileItem, fileItemList)
                if (inLoadingIndex == -1){
                    // Item is not loading, add to inProgress queue
                    newLoadingItem = {
                        file: fileItem,
                        id: policyData.file_id,
                        order: fileItemList.length + 1
                    }
                    fileItemList.push(newLoadingItem)
                  }
                fileItem.xhr = xhr
            }

            // Monitor upload progress and attach to fileItem.
            xhr.upload.addEventListener("progress", function(event){
                if (event.lengthComputable) {
                 var progress = Math.round(event.loaded / event.total * 100);
                    fileItem.progress = progress
                    displayItems(fileItemList)
                }
            })

            xhr.upload.addEventListener("load", function(event){
                console.log("Complete")
                // handle FileItem Upload being complete.
                fileUploadComplete(fileItem, policyData)

 })

            xhr.open('POST', policyData.url , true);
            xhr.send(fd);
        })
}});
