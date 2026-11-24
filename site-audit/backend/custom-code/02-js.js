document.addEventListener("scroll", function () {
  const line = document.getElementById("progressLine");
  const box = document.getElementById("scrollBox");
  const wrapper = document.querySelector(".timeline-wrapper"); // ✅ Fixed: was getElementById("progressLine-wrapper")
  const rect = wrapper.getBoundingClientRect();
  const totalHeight = window.innerWidth <= 767 ? 3000 : 1800;
  let progress = 0;

  if (rect.top <= 0) {
    let scrolled = -rect.top;
    let maxScroll = wrapper.offsetHeight - window.innerHeight;
    progress = scrolled / maxScroll;
  }

  progress = Math.max(0, Math.min(1, progress));

  line.style.strokeDashoffset = totalHeight * (1 - progress);
  box.style.transform = `translateY(${totalHeight * progress}px)`;
});