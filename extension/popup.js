document.addEventListener('DOMContentLoaded', function() {
    const scanButton = document.getElementById('scanButton');
    const statusDiv = document.getElementById('status');
    const resultsSection = document.getElementById('resultsSection');
    const resultsDiv = document.getElementById('results');

    // Check if we have stored results
    chrome.storage.local.get(['shadowDomResults'], function(result) {
        if (result.shadowDomResults && result.shadowDomResults.found) {
            displayResults(result.shadowDomResults);
        }
    });

    scanButton.addEventListener('click', function() {
        scanForShadowDOM();
    });

    function scanForShadowDOM() {
        scanButton.disabled = true;
        scanButton.textContent = '🔄 Scanning...';
        statusDiv.textContent = 'Scanning active tab for Shadow DOM components...';
        statusDiv.className = 'status loading';

        // Get current active tab
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs[0]) {
                // Send message to content script
                chrome.tabs.sendMessage(tabs[0].id, {
                    action: 'extractShadowData'
                }, function(response) {
                    if (chrome.runtime.lastError) {
                        statusDiv.textContent = 'Error: ' + chrome.runtime.lastError.message;
                        statusDiv.className = 'status';
                        resetButton();
                        return;
                    }

                    if (response && response.found) {
                        statusDiv.textContent = `✅ Found sensitive data in ${response.sensitiveData.length} Shadow DOM element(s)!`;
                        statusDiv.className = 'status';
                        displayResults(response);
                        
                        // Store results
                        chrome.storage.local.set({shadowDomResults: response});
                    } else {
                        statusDiv.textContent = 'ℹ️ No Shadow DOM components with sensitive data found on this page.';
                        statusDiv.className = 'status';
                    }
                    resetButton();
                });
            }
        });
    }

    function displayResults(results) {
        resultsSection.style.display = 'block';
        resultsDiv.innerHTML = '';

        results.sensitiveData.forEach((data, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            
            let content = `<strong>Shadow DOM Element #${data.elementIndex}</strong><br>`;
            
            if (data.systemFlag) {
                const flagDiv = document.createElement('div');
                flagDiv.className = 'flag-found';
                flagDiv.textContent = `🏁 ${data.systemFlag}`;
                resultItem.appendChild(flagDiv);
            }
            
            if (data.patientRecords) {
                content += `<span class="data-type">👥 Patient Records</span>`;
            }
            
            if (data.staffSalaries) {
                content += `<span class="data-type">💰 Staff Salaries</span>`;
            }
            
            content += `<br><small>Extracted at: ${new Date(results.timestamp).toLocaleString()}</small>`;
            
            const contentDiv = document.createElement('div');
            contentDiv.innerHTML = content;
            resultItem.appendChild(contentDiv);
            
            resultsDiv.appendChild(resultItem);
        });
    }

    function resetButton() {
        scanButton.disabled = false;
        scanButton.textContent = '🔍 Scan for Shadow DOM Data';
    }

    // Listen for messages from content script
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
        if (message.action === 'shadowDataExtracted') {
            displayResults(message.data);
            statusDiv.textContent = `🚨 Live extraction detected! Found ${message.data.sensitiveData.length} vulnerable Shadow DOM element(s).`;
        }
    });
});
