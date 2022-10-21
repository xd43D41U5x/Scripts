document.getElementById('b64').addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['convertB64.js']
    });
});

document.getElementById('hex').addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['convertHex.js']
    });
});

document.getElementById('compd').addEventListener("click", async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['checkCompd.js']
    });
});
