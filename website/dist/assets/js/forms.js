/* =====================================================================
   MMAG website: forms (unminified)
   Fields mirror the live mmag.in forms (Download Portfolio, Schedule A Call,
   Contact). Submission: POST url-encoded to CONFIG.formEndpoint, or "/" for
   Netlify Forms. Spam: honeypot field (bot-field).
   ===================================================================== */
(function () {
  "use strict";

  var CFG = window.MMAG_CONFIG || {};

  var MESSAGES = {
    required: "Please fill this in.",
    email: "Please enter a valid email address.",
    phone: "Please enter a valid phone number (digits only).",
    select: "Please choose an option."
  };

  var EVENTS = {
    "download-portfolio": "portfolio_download_submit",
    "schedule-call": "schedule_call_submit",
    "contact": "contact_submit"
  };

  function fieldOf(input) { return input.closest(".field"); }

  function setError(input, msg) {
    var f = fieldOf(input);
    if (!f) return;
    f.classList.toggle("is-invalid", !!msg);
    var err = f.querySelector(".field__err");
    if (err) err.textContent = msg || "";
    input.setAttribute("aria-invalid", msg ? "true" : "false");
  }

  function validate(input) {
    var v = (input.value || "").trim();
    if (input.required && !v) return input.tagName === "SELECT" ? MESSAGES.select : MESSAGES.required;
    if (v && input.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return MESSAGES.email;
    if (v && input.type === "tel" && !/^[0-9\s-]{6,15}$/.test(v)) return MESSAGES.phone;
    return "";
  }

  function validateForm(form) {
    var firstBad = null;
    Array.prototype.forEach.call(form.querySelectorAll(".field input, .field select, .field textarea"), function (input) {
      if (input.type === "checkbox" || input.closest(".hp")) return;
      var msg = validate(input);
      setError(input, msg);
      if (msg && !firstBad) firstBad = input;
    });
    return firstBad;
  }

  function encode(form) {
    var data = new FormData(form);
    var code = data.get("country_code");
    var phone = data.get("phone");
    if (phone) data.set("phone", (code ? code + " " : "") + String(phone).trim());
    data.delete("country_code");
    var params = new URLSearchParams();
    data.forEach(function (value, key) { params.append(key, value); });
    return params.toString();
  }

  function setStatus(form, text, state) {
    var s = form.querySelector(".form__status");
    if (!s) return;
    s.textContent = text || "";
    if (state) s.setAttribute("data-state", state); else s.removeAttribute("data-state");
  }

  function onSubmit(e) {
    var form = e.target;
    e.preventDefault();
    var bad = validateForm(form);
    if (bad) { bad.focus(); setStatus(form, "Please check the highlighted fields.", "error"); return; }
    if (form.querySelector("[name=bot-field]") && form.querySelector("[name=bot-field]").value) return;

    var button = form.querySelector("button[type=submit]");
    var label = button ? button.innerHTML : "";
    if (button) { button.disabled = true; button.textContent = "Sending…"; }
    setStatus(form, "", null);

    var endpoint = CFG.formEndpoint || "/";
    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json" },
      body: encode(form)
    }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      var name = form.getAttribute("name");
      if (window.MMAG_TRACK) window.MMAG_TRACK(EVENTS[name] || "form_submit", { form: name });
      var wrap = form.closest("[data-form-wrap]");
      if (wrap) {
        wrap.classList.add("is-sent");
        var link = wrap.querySelector("[data-portfolio-link]");
        var waiting = wrap.querySelector("[data-portfolio-wait]");
        if (link && CFG.portfolioUrl) { link.href = CFG.portfolioUrl; link.hidden = false; if (waiting) waiting.hidden = true; }
        var ok = wrap.querySelector(".form__success");
        if (ok) ok.focus();
      }
      form.reset();
    }).catch(function () {
      var phone = CFG.phoneDisplay || "";
      setStatus(form, "We couldn't send this right now." + (phone ? " Please call us on " + phone + "." : " Please try again shortly."), "error");
    }).then(function () {
      if (button) { button.disabled = false; button.innerHTML = label; }
    });
  }

  Array.prototype.forEach.call(document.querySelectorAll("form[data-form]"), function (form) {
    form.addEventListener("submit", onSubmit);
    Array.prototype.forEach.call(form.querySelectorAll(".field input, .field select, .field textarea"), function (input) {
      input.addEventListener("blur", function () { if (input.value) setError(input, validate(input)); });
      input.addEventListener("input", function () { if (fieldOf(input) && fieldOf(input).classList.contains("is-invalid")) setError(input, validate(input)); });
    });
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-form-reset]"), function (btn) {
    btn.addEventListener("click", function () {
      var wrap = btn.closest("[data-form-wrap]");
      if (wrap) wrap.classList.remove("is-sent");
    });
  });
})();
