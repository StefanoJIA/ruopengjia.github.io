// Keep the same section when moving between the two static language editions.
document.querySelectorAll(".language-switch a").forEach((link) => {
  link.addEventListener("click", () => {
    const target = new URL(link.href);
    target.hash = window.location.hash;
    link.href = target.href;
  });
});
