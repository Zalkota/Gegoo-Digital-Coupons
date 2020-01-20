$(function () {
  $(document).scroll(function () {
    var $nav = $(".navbar-default");
    $nav.toggleClass('fixed-top', $(this).scrollTop() > 54);
  });
});
