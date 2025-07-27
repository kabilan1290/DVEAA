// content.js - Extract ALL Shadow DOM content (no specific selectors)

console.log('[Shadow DOM Extractor] Content script loaded - Generic extraction mode');

function extractAllShadowDOMContent() {
  console.log('[Shadow DOM Extractor] Scanning for ALL Shadow DOM content...');
  
  let extractedData = [];
  let componentsScanned = 0;
  
  // Scan main document AND all iframes
  scanDocumentForShadowDOM(document, 'main document');
  
  const iframes = document.querySelectorAll('iframe');
  iframes.forEach((iframe, index) => {
    try {
      if (iframe.contentDocument) {
        console.log(`[Shadow DOM Extractor] Scanning iframe ${index + 1}`);
        scanDocumentForShadowDOM(iframe.contentDocument, `iframe ${index + 1}`);
      }
    } catch (e) {
      console.log(`[Shadow DOM Extractor] Cannot access iframe ${index + 1}: ${e.message}`);
    }
  });
  
  function scanDocumentForShadowDOM(doc, location) {
    // Get ALL elements in the document
    const allElements = doc.querySelectorAll('*');
    
    allElements.forEach((element) => {
      if (element.shadowRoot) {log(`[Shadow DOM Extractor] Found shadow root in element: ${element.tagName}`);
        
        // Extract EVERYTHING from the shadow root
        const shadowContent = {
          source: `${location} - ${element.tagName.toLowerCase()}`,
          element: element.tagName,
          innerHTML: element.shadowRoot.innerHTML,
          textContent: element.shadowRoot.textContent,
          allText: extractAllTextFromShadowRoot(element.shadowRoot),
          attributes: getShadowRootAttributes(element.shadowRoot),
          timestamp: new Date().toISOString()
        };
        
        extractedData.push(shadowContent);
        
        // Log what we found
        console.log(`[Shadow DOM Extractor] Extracted shadow content:`, shadowContent);
      }
    });
  }
  
  function extractAllTextFromShadowRoot(shadowRoot) {
    let allText = [];
    
    // Get all text nodes and element text content
    const walker = document.createTreeWalker(
      shadowRoot,
      NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
      null,
      false
    );
    
    let node;
    while (node = walker.nextNode()) {
      if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
        allText.push(node.textContent.trim());
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        // Extract data attributes and other interesting attributes
        if (node.hasAttributes()) {
          Array.from(node.attributes).forEach(attr => {
            if (attr.name.includes('data-') || attr.name.includes('id') || attr.name.includes('class')) {
              allText.push(`${attr.name}="${attr.value}"`);
            }
          });
        }
      }
    }
    
    return allText;
  }
  
  function getShadowRootAttributes(shadowRoot) {
    let attributes = {};
    
    // Get all elements with interesting attributes
    const elementsWithAttrs = shadowRoot.querySelectorAll('*[id], *[class], *[data-*]');
    elementsWithAttrs.forEach(el => {
      Array.from(el.attributes).forEach(attr => {
        if (!attributes[el.tagName]) attributes[el.tagName] = {};
        attributes[el.tagName][attr.name] = attr.value;
      });
    });
    
    return attributes;
  }
  
  // Report results
  if (extractedData.length > 0) {
    console.log(`[Shadow DOM Extractor] 🎉 EXTRACTION SUCCESSFUL! Found ${extractedData.length} shadow DOM components`);
    
    // Create comprehensive report
    let report = `Shadow DOM Data Leak Successful!\n\nExtracted ${extractedData.length} shadow DOM components:\n\n`;
    
    extractedData.forEach((data, index) => {
      report += `--- Component ${index + 1} (${data.element}) ---\n`;
      report += `Source: ${data.source}\n`;
      report += `HTML Length: ${data.innerHTML.length} characters\n`;
      report += `Text Content: ${data.textContent.substring(0, 200)}${data.textContent.length > 200 ? '...' : ''}\n`;
      report += `All Text Nodes: ${data.allText.join(' | ')}\n`;
      report += `Attributes: ${JSON.stringify(data.attributes)}\n\n`;
    });
    
    // Show alert with extracted data
    alert(report);
    
    // Also log full HTML content to console for detailed analysis
    extractedData.forEach((data, index) => {
      console.log(`[Shadow DOM Content ${index + 1}] Full HTML:`, data.innerHTML);
      console.log(`[Shadow DOM Content ${index + 1}] Full Text:`, data.textContent);
    });
    
    return extractedData;
  } else {
    console.log(`[Shadow DOM Extractor] ℹ️ No Shadow DOM components found. Scanned ${componentsScanned} elements.`);
    return null;
  }
}

// Enhanced scanning with better timing
function startGenericShadowDOMScanning() {
  // Multiple scan attempts with different delays
  setTimeout(() => extractAllShadowDOMContent(), 500);
  setTimeout(() => extractAllShadowDOMContent(), 1500);
  setTimeout(() => extractAllShadowDOMContent(), 3000);
  
  // Set up MutationObserver to detect ANY new elements
  const observer = new MutationObserver((mutations) => {
    let shouldScan = false;
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        shouldScan = true;
      }
    });
    
    if (shouldScan) {
      setTimeout(() => extractAllShadowDOMContent(), 200);
    }
  });
  
  observer.observe(document.body, { 
    childList: true, 
    subtree: true, 
    attributes: false,
    characterData: false 
  });
  
  // Periodic comprehensive scanning
  setInterval(() => extractAllShadowDOMContent(), 10000);
}

// Initialize scanning
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', startGenericShadowDOMScanning);
} else {
  startGenericShadowDOMScanning();
}

// Also add a manual trigger function for testing
window.extractShadowDOM = extractAllShadowDOMContent;
console.log('[Shadow DOM Extractor] Manual trigger available: window.extractShadowDOM()');
