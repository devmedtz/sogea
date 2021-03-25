
$(".offcanvas-toggle").on("click", function(e){
  e.preventDefault();
  e.stopPropagation();
  $('.offcanvas-collapse').toggleClass("open");
  $('body').toggleClass("offcanvas-active");
  $(".screen-overlay").toggleClass("show");
}); 

$(".btn-close, .screen-overlay").click(function(e){
  $(".screen-overlay").removeClass("show");
  $(".offcanvas-collapse").removeClass("open");
  $("body").removeClass("offcanvas-active");
}); 