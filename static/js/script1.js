  $(document).ready(function(){
  $(window).scroll(function(){
  if($(window).scrollTop() > 60 ){
  $('.my-navbar').addClass('navbar-scroll');
  }
  else{
  $('.my-navbar').removeClass('navbar-scroll');
  }
  });
  });