$(function () {
  $(document).scroll(function () {
    var $nav = $(".navbar-default");
    $nav.toggleClass('scrolled', $(this).scrollTop() > 25);
  });
});

$(function () {
  $(document).scroll(function () {
    var $nav = $(".nav-link");
    $nav.toggleClass('scrolled', $(this).scrollTop() > 25);
  });
});

$(function () {
  $(document).scroll(function () {
    var $nav = $(".navbar-brand");
    $nav.toggleClass('scrolled', $(this).scrollTop() > 25);
  });
});

$(function () {
  $(document).scroll(function () {
    var $nav = $(".navbar-toggler");
    $nav.toggleClass('scrolled', $(this).scrollTop() > 25);
  });
});

$(function () {
  $(document).scroll(function () {
    var $nav = $(".btn-outline-navbar");
    $nav.toggleClass('scrolled', $(this).scrollTop() > 25);
  });
});
