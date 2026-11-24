gsap.registerPlugin(ScrollTrigger, MotionPathPlugin);

ScrollTrigger.matchMedia({

  /* =======================
     ✅ DESKTOP ONLY
     ======================= */
  "(min-width: 768px)": function () {

    const master = gsap.timeline({
      scrollTrigger: {
        trigger: ".hero-pin",
        start: "top top",
        pin: true,
        end: "bottom",
        pinSpacing: true,
        scrub: 1.5,
        anticipatePin: 1,
        invalidateOnRefresh: true,
        onLeave: () => {
          console.log("Section Released");
        }
      }
    });

    // INITIAL STATE
    gsap.set("#hero-ball", {
      zIndex: 5,
      xPercent: -50,
      yPercent: -50
    });

    gsap.set(".frame", { zIndex: 10 });

    // CONTINUOUS BALL MOTION
    master.to("#hero-ball", {
      motionPath: {
        path: [
          { x: "-10vw", y: "-5vh" },
          { x: "-25vw", y: "0vh" },
          { x: "-35vw", y: "10vh" },
          { x: "-35vw", y: "50vh" },
          { x: "-35vw", y: "95vh" },
          { x: "-35vw", y: "130vh" }
        ],
        curviness: 1.5
      },
      ease: "none",
      duration: 20
    }, 0);

    master.set(".ball-container", { zIndex: 15 }, 2);

    // PROCESS SECTION HAND-OFF
    gsap.to("#process-ball", {
      y: "160px",
      scrollTrigger: {
        trigger: "#process-section",
        start: "top 95%",
        end: "top 70%",
        scrub: 0.1,
        invalidateOnRefresh: true
      },
      ease: "none"
    });
  },

  /* =======================
     ❌ MOBILE ONLY
     ======================= */
  "(max-width: 767px)": function () {

    // Kill everything
    ScrollTrigger.getAll().forEach(st => st.kill());
    gsap.killTweensOf("*");
    gsap.globalTimeline.clear();

    // Reset ONLY animated elements (important)
    gsap.set(
      "#hero-ball, #process-ball, .hero-pin, .frame, .ball-container",
      { clearProps: "all" }
    );
  }

});