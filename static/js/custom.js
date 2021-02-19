// (function () {
//   'use strict'

//   document.querySelector('[data-bs-toggle="offcanvas"]').addEventListener('click', function () {
//     document.querySelector('.offcanvas-collapse').classList.toggle('open');
//     document.querySelector('.screen-overlay').toggleClass("show");
//   })
// })()


$("[data-bs-toggle]").on("click", function(e){
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