const video = document.querySelector('.video');
const vdo = video.querySelector('video');
const txt = video.querySelector('h2');
//end section
const span = document.querySelector('span')
const end = span.querySelector('h1');

//scroll magic
const controller = new ScrollMagic.Controller();
const scene = new ScrollMagic.Scene({
    duration: 50,
    triggerelement: video,
    triggerHook: 0
})  
 .addIndicators()
 .setPin(video)
 .addTo(controller)

let accelamount = 0.1;
let scrollpos = 0;
let delay = 10;

scene.on('update', e => {
    scrollpos = e.scrollpos / 1000;
});

setInterval(() => {
    delay += (scrollpos - delay) * accelamount;
    console.log(scrollpos, delay);

    video.currentTime = delay;
}, 33,3);



function myFunction() {
    var dots = document.getElementById("dots");
    var moreText = document.getElementById("more");
    var btnText = document.getElementById("myBtn");
  
    if (dots.style.display == "none") {
      dots.style.display = "inline";
      btnText.innerHTML = "Read more";
      moreText.style.display = "none";
    } else {
      dots.style.display = "none";
      btnText.innerHTML = "Read less";
      moreText.style.display = "inline";
    }
}
 

window.sr = ScrollReveal();

sr.reveal('.animate-left', {
    origin: 'left',
    duration: 3000,
    distance: '25rem',
    delay: 0
});

sr.reveal('.animate-right', {
    origin: 'right',
    duration: 1000,
    distance: '25rem',
    delay: 600
});

sr.reveal('.animate-top', {
    origin: 'top',
    duration: 1000,
    distance: '25rem',
    delay: 600
});



document.onreadystatechange = function() { 
    if (document.readyState !== "complete") { 
        document.querySelector("body").style.visibility = "hidden"; 
        document.querySelector("#loader").style.visibility = "visible"; 
    } else { 
        document.querySelector("#loader").style.display = "none"; 
        document.querySelector("body").style.visibility = "visible"; 
    } 
}; 




