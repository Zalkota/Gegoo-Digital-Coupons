/** Document Ready Functions **/
/********************************************************************/

$( document ).ready(function() {

    // // Resive video
    // scaleVideoContainer();
    //
    // initBannerVideoSize('.video-container .poster img');
    // initBannerVideoSize('.video-container .filter');
    // initBannerVideoSize('.video-container video');
    //
    // $(window).on('resize', function() {
    //     scaleVideoContainer();
    //     scaleBannerVideoSize('.video-container .poster img');
    //     scaleBannerVideoSize('.video-container .filter');
    //     scaleBannerVideoSize('.video-container video');
    // });





});
var video = document.getElementById("video")

$("#Unmutebutton").click(function(){
    video.muted = false
    $("#Mutebutton").show()
    $("#Unmutebutton").hide()
});

$("#Mutebutton").click(function(){
    video.muted = true
    $("#Mutebutton").hide()
    $("#Unmutebutton").show()
});

/** Reusable Functions **/
/********************************************************************/
//
// function scaleVideoContainer() {
//
//     var height = $(window).height() * .7;  // I added the * .7
//     var unitHeight = parseInt(height) + 'px';
//     $('.homepage-hero-module').css('height',unitHeight);
//     $('.everything-under-vid').show();  // I added this so logos wont show until video JS is executed
//     $('.vid-bg-footer').show();
// }
//
// function initBannerVideoSize(element){
//
//     $(element).each(function(){
//         $(this).data('height', $(this).height());
//         $(this).data('width', $(this).width());
//     });
//
//     scaleBannerVideoSize(element);
//
// }

// function scaleBannerVideoSize(element){
//
//     var windowWidth = $(window).width(),
//         windowHeight = $(window).height(),
//         videoWidth,
//         videoHeight;
//
//     console.log(windowHeight);
//
//     $(element).each(function(){
//         var videoAspectRatio = $(this).data('height')/$(this).data('width'),
//             windowAspectRatio = windowHeight/windowWidth;
//
//         if (videoAspectRatio > windowAspectRatio) {
//             videoWidth = windowWidth;
//             videoHeight = videoWidth * videoAspectRatio;
//             $(this).css({'top' : -(videoHeight - windowHeight) / 2 + 'px', 'margin-left' : 0});
//         } else {
//             videoHeight = windowHeight;
//             videoWidth = videoHeight / videoAspectRatio;
//             $(this).css({'margin-top' : 0, 'margin-left' : -(videoWidth - windowWidth) / 2 + 'px'});
//         }
//
//         $(this).width(videoWidth).height(videoHeight);
//
//         $('.homepage-hero-module .video-container video').addClass('fadeIn animated');
//
//
//     });
// }
