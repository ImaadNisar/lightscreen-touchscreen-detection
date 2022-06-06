function func(command) {
    var txt = document.getElementById(command).innerHTML;
    navigator.clipboard.writeText(txt);
    
    if (command=="pip1") {
        var x = document.getElementById("t1");
        const btn = document.getElementById("copy1");
    }
    if (command=="pip2") {
        var x = document.getElementById("t2");
        const btn = document.getElementById("copy2");
    }
    if (command=="pip3") {
        var x = document.getElementById("t3");
        const btn = document.getElementById("copy3");
    }
    if (command=="pip4") {
        var x = document.getElementById("t4");
        const btn = document.getElementById("copy4");
    }
    if (command=="pip5") {
        var x = document.getElementById("t5");
        const btn = document.getElementById("copy5");
    }
    

    x.innerText = "Copied";
    x.style.padding = "12.6px 15px 12.6px 14.9px";
    
}



function revert(id) {
    var id = document.getElementById(id);
    id.innerHTML = "Copy to clipboard";
    id.style.padding = "5px 15px 5px 15px";

}




function slideshow() {
    const slideshowimages = document.querySelectorAll(".image")

    const nextImageDelay = 5000;
    let currentImageCounter = 0
    circle = document.getElementById('c1')
    circle.style.backgroundColor ="#FFFFFF";

    slideshowimages[currentImageCounter].style.opacity = 1;

    setInterval(nextImage, nextImageDelay)


    function nextImage() {
        for (i=0; i<slideshowimages.length; i++) {
            slideshowimages[i].style.zIndex = 0;
        }
        slideshowimages[currentImageCounter].style.opacity = 0;
        currentImageCounter = (currentImageCounter + 1) % slideshowimages.length;
        slideshowimages[currentImageCounter].style.opacity = 1;
        slideshowimages[currentImageCounter].style.zIndex = 5;

        circles = document.querySelectorAll(".c");
        for (i=0; i<circles.length; i++) {
            circles[i].style.backgroundColor ="#808080";
        }
        circles[currentImageCounter].style.backgroundColor ="#FFFFFF";
        
        
    }
}


