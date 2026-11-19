/* Minimal JS: mobile nav, gallery lightbox, contact form. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* Lightbox for elements with data-lightbox */
  var boxes = document.querySelectorAll("[data-lightbox]");
  if (boxes.length) {
    var overlay = document.createElement("div");
    overlay.className = "lightbox";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Image preview");
    overlay.innerHTML =
      '<button type="button" class="lightbox-close" aria-label="Close">&times;</button><img alt="">';
    document.body.appendChild(overlay);
    var img = overlay.querySelector("img");
    var closeBtn = overlay.querySelector(".lightbox-close");

    function close() {
      overlay.classList.remove("is-open");
      img.removeAttribute("src");
    }
    function open(src, alt) {
      img.src = src;
      img.alt = alt || "";
      overlay.classList.add("is-open");
      closeBtn.focus();
    }

    boxes.forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        var src = el.getAttribute("href") || (el.querySelector("img") || {}).src;
        var alt = ((el.querySelector("img") || {}).alt) || "";
        if (src) open(src, alt);
      });
    });
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay || e.target === closeBtn) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  /* Contact form → Web3Forms (or Formspree if the action is changed). */
  var form = document.querySelector("form[data-contact]");
  if (!form) return;

  var status = form.querySelector(".form-status");
  var submit = form.querySelector("[type=submit]");
  var PLACEHOLDER = "YOUR_WEB3FORMS_ACCESS_KEY";

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var keyInput = form.querySelector("[name=access_key]");
    var key = keyInput ? keyInput.value.trim() : "";
    if (!key || key === PLACEHOLDER) {
      if (status) {
        status.className = "form-status err";
        status.textContent =
          "The form is not connected yet. Replace YOUR_WEB3FORMS_ACCESS_KEY in contact/index.html with a free key from web3forms.com (set the recipient to ab-tech@bladelius.com).";
      }
      return;
    }

    if (submit) submit.disabled = true;
    if (status) {
      status.className = "form-status";
      status.textContent = "Sending…";
    }

    var data = new FormData(form);
    fetch(form.action, {
      method: "POST",
      body: data,
      headers: { Accept: "application/json" }
    })
      .then(function (res) {
        return res.json().catch(function () { return { ok: res.ok }; });
      })
      .then(function (json) {
        var ok = json.success === true || json.ok === true || json.ok === "true";
        if (ok) {
          form.reset();
          if (status) {
            status.className = "form-status ok";
            status.textContent = "Thank you. Your message has been sent.";
          }
        } else {
          throw new Error((json && (json.message || json.error)) || "Could not send.");
        }
      })
      .catch(function (err) {
        if (status) {
          status.className = "form-status err";
          status.textContent =
            "The message could not be sent. Please try again later or email ab-tech@bladelius.com. " +
            (err && err.message ? "(" + err.message + ")" : "");
        }
      })
      .finally(function () {
        if (submit) submit.disabled = false;
      });
  });
})();
