/* =====================================================================
   MMAG website: runtime settings. Edit this file, not the other scripts.
   Values left empty are features waiting on a decision (see docs/PROMPT-LOG.md).
   ===================================================================== */
window.MMAG_CONFIG = {
  // Where forms POST. "" = Netlify Forms (POST to "/"); works when deployed on Netlify.
  // For any other host, paste a form-service endpoint (e.g. a Formspree URL) here.
  formEndpoint: "",

  // Link shown after the "Download Portfolio" form is sent.
  // "" = no file yet: the thank-you message says the team will email it.
  portfolioUrl: "",

  // Google Analytics 4 measurement ID. Live site uses G-9WNY7XF2FT.
  // Leave empty on preview deploys so test traffic doesn't reach the real property.
  ga4Id: "",

  // Contact details (from MMAG's portfolio deck on the live site)
  phone: "+918308852044",
  phoneDisplay: "+91 83088 52044",
  email: "rushi@mmag.in",
  whatsapp: "https://wa.me/918308852044",

  // Three.js from a CDN (pinned). Swap the version here if needed.
  threeUrl: "https://cdn.jsdelivr.net/npm/three@0.187.0/build/three.module.js",

  // Showreel (YouTube embed, from the live site).
  showreelEmbed: "https://www.youtube-nocookie.com/embed/HVSOqY1VJ1E?autoplay=1&rel=0"
};
