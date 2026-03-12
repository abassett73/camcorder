import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Add modal CSS before the closing </style> tag
modal_css = """
  /* WARNING MODAL */
  .modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    z-index: 2000;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.2s ease;
  }

  .modal-overlay.visible {
    display: flex;
  }

  .modal-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 32px;
    max-width: 440px;
    width: 90%;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    text-align: center;
    animation: pop-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }

  .modal-icon {
    font-size: 2.5rem;
    margin-bottom: 16px;
  }

  .modal-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 10px;
  }

  .modal-message {
    font-size: 0.9rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 24px;
  }

  .modal-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
  }

  .modal-actions .btn {
    padding: 12px 28px;
    font-size: 0.9rem;
  }

  .btn-danger {
    background: var(--red);
    color: white;
    box-shadow: 0 4px 15px var(--red-glow);
  }

  .btn-danger:hover { background: #ff6b7a; transform: translateY(-1px); }
"""

html = html.replace('</style>', modal_css + '\n</style>')

# 2. Add the modal HTML before the toast div
modal_html = """
  <!-- WARNING MODAL -->
  <div class="modal-overlay" id="warning-modal">
    <div class="modal-box">
      <div class="modal-icon">⚠️</div>
      <div class="modal-title">Start New Recording?</div>
      <div class="modal-message">You have files that haven't been downloaded yet. If you continue, they will be lost and can't be recovered.</div>
      <div class="modal-actions">
        <button class="btn btn-secondary" onclick="closeWarningModal()">
          <i class="fas fa-arrow-left"></i> Go Back
        </button>
        <button class="btn btn-danger" onclick="confirmNewRecording()">
          <i class="fas fa-redo"></i> Continue
        </button>
      </div>
    </div>
  </div>
"""

html = html.replace('<div class="toast"', modal_html + '\n<div class="toast"')

# 3. Replace the Re-record button with New Recording button in done-actions
old_actions = """      <button class="btn btn-secondary" onclick="resetApp()">
        <i class="fas fa-redo"></i> Re-record
      </button>"""

new_actions = """      <button class="btn btn-secondary" onclick="handleNewRecording()">
        <i class="fas fa-plus"></i> New Recording
      </button>"""

html = html.replace(old_actions, new_actions)

# 4. Add tracking variables and modal functions before the closing </script> tag
new_js = """
  // ===== DOWNLOAD TRACKING & WARNING MODAL =====
  var txtDownloaded = false;
  var mediaDownloaded = false;

  // Override download functions to track downloads
  var _origDownloadTxt = downloadTxt;
  downloadTxt = function() {
    _origDownloadTxt();
    txtDownloaded = true;
  };

  var _origDownloadMedia = downloadMedia;
  downloadMedia = function() {
    _origDownloadMedia();
    mediaDownloaded = true;
  };

  var _origDownloadAll = downloadAll;
  downloadAll = function() {
    _origDownloadAll();
    txtDownloaded = true;
    mediaDownloaded = true;
  };

  function handleNewRecording() {
    var allDownloaded = txtDownloaded && (mediaBlob ? mediaDownloaded : true);
    if (allDownloaded) {
      resetApp();
    } else {
      document.getElementById('warning-modal').classList.add('visible');
    }
  }

  function closeWarningModal() {
    document.getElementById('warning-modal').classList.remove('visible');
  }

  function confirmNewRecording() {
    closeWarningModal();
    resetApp();
  }

  // Reset download tracking when resetting app
  var _origResetApp = resetApp;
  resetApp = function() {
    txtDownloaded = false;
    mediaDownloaded = false;
    _origResetApp();
  };

  // Close modal on overlay click
  document.getElementById('warning-modal').addEventListener('click', function(e) {
    if (e.target === this) closeWarningModal();
  });

  // Close modal on Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeWarningModal();
  });
"""

html = html.replace('</script>', new_js + '\n</script>')

with open('index.html', 'w') as f:
    f.write(html)

print("Patched successfully")
