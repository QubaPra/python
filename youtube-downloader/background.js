chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  const url = message.url;
  const pythonScript = "youtube.py";
  const command = `python ${pythonScript} "${url}"`;

  chrome.downloads.download({ url: url }, (downloadId) => {
    const process = require("child_process").exec(command);
    process.stdout.on("data", (data) => console.log(data));
    process.stderr.on("data", (data) => console.error(data));
    process.on("close", () => {
      chrome.downloads.search({ id: downloadId }, (downloads) => {
        const download = downloads[0];
        const filename = download.filename;
        const downloadLocation = download.filename.slice(0, download.filename.lastIndexOf("/"));
        const downloadOptions = { filename: filename, saveAs: false };
        chrome.downloads.download(Object.assign({ url: `file://${filename}` }, downloadOptions));
      });
    });
  });
});
