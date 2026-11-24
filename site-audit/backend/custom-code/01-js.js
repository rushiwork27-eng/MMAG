document.addEventListener('mousemove', function(e) {
    const cursorImg = document.getElementById('cursor-image');

    cursorImg.style.left = e.clientX + 'px';
    cursorImg.style.top = e.clientY + 'px';
});