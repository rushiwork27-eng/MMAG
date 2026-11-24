function initProcessOnlyAnimation() {

  // ? HARD STOP ON MOBILE
  if (window.matchMedia("(max-width: 767px)").matches) {
    return;
  }

  // Wait until GSAP plugins are available
  if (typeof MotionPathPlugin === "undefined" || typeof ScrollTrigger === "undefined") {
    setTimeout(initProcessOnlyAnimation, 300);
    return;
  }

  gsap.registerPlugin(ScrollTrigger, MotionPathPlugin);

  ScrollTrigger.matchMedia({

    /* =======================
       ✅ DESKTOP ONLY
       ======================= */
    "(min-width: 768px)": function () {

      const section = document.querySelector("#process-section");
      const circles = document.querySelectorAll(".moving-circle");
      const targets = document.querySelectorAll("#process-section .target-position");

      if (!section || circles.length === 0) return;

      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: section,
          start: "top top",
          end: "+=200%",
          scrub: 1.5,
          pin: true,
          pinSpacing: true,
          invalidateOnRefresh: true,
// 					onLeave: () => {
//       // ? swap balls
//       gsap.set("#process-ball", {
//         opacity: 0,
//         visibility: "hidden"
//       });

//       gsap.set("#build-ball", {
//     clearProps: "transform"
//   });

//   // Then apply scale
//   gsap.set("#build-ball", {
//     opacity: 1,
//     visibility: "visible",
//     scale: 0.7
//   });
//   }
					// ? scrolling UP back into the pin
//     onEnterBack: () => {
// //       gsap.set("#build-ball", {
// //         opacity: 0,
// //         visibility: "hidden",
// //         scale: 1
// //       });

// //       gsap.set("#process-ball", {
// //         opacity: 1,
// //         visibility: "visible"
// //       });
//     }
        }
      });

      // INITIAL STATE
      gsap.set(circles, { y: 0, opacity: 0 });

      // PHASE 0: DROP
      tl.to(circles, {
        y: 120,
        opacity: 1,
        duration: 0.5,
        ease: "power1.out"
      });
			tl.to("#process-ball", {
  opacity: 0,
  duration: 1,
  ease: "power1.out"
}, 0.5);

      // PHASE 1: SPREAD TO TARGETS
      circles.forEach((circle, i) => {
        const target = targets[i];
        if (!target) return;

        const p = MotionPathPlugin.getRelativePosition(
          circle,
          target,
          [0.5, 0.5],
          [0.5, 0.5]
        );

        tl.to(circle, {
          x: p.x,
          y: p.y,
          duration: 1.2,
          ease: "power2.inOut"
        }, 0.6);
      });

//       // PHASE 3.5: 4th BALL EXIT
//       const fourthCircle = circles[3];
//       if (fourthCircle) {
//         tl.to(fourthCircle, {
//           y: "+=300",
//           scale: 0.6,
//           opacity: 0,
//           duration: 2,
//           ease: "power3.in"
//         }, ">");
//       }

//       // FINAL HOLD
      tl.to({}, { duration: 1 });
// 			//       // ? NEW PHASE 2: MOVE DOWN TO CENTER
// tl.to(circles, {
//   y: "+=400",
//   duration: 1,
//   ease: "power2.inOut"
// }, ">+=0.2");
    },
		
		

    /* =======================
       ❌ MOBILE ONLY
       ======================= */
    "(max-width: 767px)": function () {

      // Kill everything GSAP-related
      ScrollTrigger.getAll().forEach(st => st.kill());
      gsap.killTweensOf("*");
      gsap.globalTimeline.clear();

      // Reset animated elements (VERY IMPORTANT)
      gsap.set(
        "#process-section, .moving-circle, .target-position",
        { clearProps: "all" }
      );
    }

  });
}

// Run on page load
window.addEventListener("load", initProcessOnlyAnimation);