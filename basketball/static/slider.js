var i=0;
  var images = [];
  var time=4000;

  images[0]= '/static/schedule0.jpeg'
  images[1]= '/static/schedule1.jpeg'
  images[2]= '/static/schedule2.jpeg'
  images[3]= '/static/schedule3.jpeg'
  images[4]= '/static/schedule4.jpeg'
  images[5]= '/static/schedule5.jpeg'



// Change Image
function changeImg(){
 document.slide.src = images[i];


 if(i < images.length - 1){

   i++;
  } else {

  i = 0;
}


 setTimeout("changeImg()", time);
}


window.onload=changeImg;



