chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyze-text",
    title: "Analyze with MediQwen",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "analyze-text") {
    const selectedText = info.selectionText;

    try {
      const response = await fetch("http://localhost:11434/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "qwen2.5:1.5b",
          prompt: `you are a MEDICAL AI BOT and you need to suggest health adive : ${selectedText}`,
          stream: false
        })
      });

      const raw = await response.text();

      let resultText;

      if (!raw.trim()) {
        resultText = "❌ Empty response from LLM server.";
      } else {
        try {
          const data = JSON.parse(raw);
          resultText = data.response || "✅ Got response, but it's empty.";
        } catch (e) {
          resultText = `❌ Invalid JSON:\n${raw}`;
        }
      }

      chrome.scripting.executeScript(
        {
          target: { tabId: tab.id },
          files: ["content.js"]
        },
        () => {
          chrome.tabs.sendMessage(tab.id, {
            type: "show-result",
            result: resultText
          });
        }
      );

    } catch (error) {
      chrome.scripting.executeScript(
        {
          target: { tabId: tab.id },
          files: ["content.js"]
        },
        () => {
          chrome.tabs.sendMessage(tab.id, {
            type: "show-result",
            result: `❌ Fetch error: ${error.message}`
          });
        }
      );
    }
  }
});
