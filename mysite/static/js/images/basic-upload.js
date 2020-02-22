$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
    start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
        $("#progressbar").show();

        $("#errormessage").hide()
        $("#error-message").html(
              ""
            )
        $("#defaultmessage").hide()
    },
    stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
      $("#progressbar").hide();

    },
    progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },
    done: function (e, data) {
      if (data.result.is_valid) {

          $("#successbutton").show()
          $("#successmessage").show()
          $("#success-message").append(
            'Upload Success'
          )

          $("#defaultbutton").hide()
          $("#uploadbutton").hide()
          $("#defaultmessage").hide()
          $("#errormessage").hide()
          console.log('Success')
      }
      if (! (data.result.is_valid)) {

        $("#defaultmessage").hide()
        $("#successmessage").hide()

        $("#errormessage").show()
        $("#error-message").html(
          ""
        )
        $("#error-message").append(
          data.result.message
        )

      }
    },
  });
});
