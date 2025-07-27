chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "show-result") {
    showResult(msg.result);
  }
});

function showResult(text) {
  const existing = document.getElementById('mediqwen-overlay');
  if (existing) existing.remove();

  const overlay = document.createElement('div');
  overlay.id = 'mediqwen-overlay';
  overlay.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    width: 300px;
    max-height: 400px;
    background: white;
    border: 2px solid #007cba;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 10000;
    font-family: Arial, sans-serif;
    font-size: 14px;
    overflow-y: auto;
  `;

  overlay.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
      <strong style="color: #007cba;">MediQwen Analysis</strong>
      <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; font-size: 18px; cursor: pointer;">×</button>
    </div>
    <div style="border-top: 1px solid #000000; padding-top: 10px;">
      ${text}
    </div>
  `;

  document.body.appendChild(overlay);

  setTimeout(() => {
    if (overlay.parentElement) overlay.remove();
  }, 10000);
}
