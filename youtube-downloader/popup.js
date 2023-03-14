const form = document.getElementById("download-form");
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const url = document.getElementById("youtube-url").value;
  chrome.runtime.sendMessage({ url: url });
});
