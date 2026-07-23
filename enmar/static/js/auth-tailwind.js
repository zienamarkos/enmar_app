document.addEventListener("DOMContentLoaded", function () {
  // Toggle password visibility
  document.querySelectorAll(".toggle-password").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var parent = btn.closest("div");
      var input = parent && parent.querySelector("input[type='password'], input[type='text']");
      if (!input) return;
      if (input.type === "password") {
        input.type = "text";
        btn.textContent = "Hide";
      } else {
        input.type = "password";
        btn.textContent = "Show";
      }
      input.focus();
    });
  });

  // Prevent double submit
  var form = document.getElementById("register-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      var submit = document.getElementById("submit-btn");
      if (!submit) return;
      if (submit.disabled) {
        e.preventDefault();
        return;
      }
      submit.disabled = true;
      submit.classList.add("opacity-80", "cursor-not-allowed");
    });
  }
});