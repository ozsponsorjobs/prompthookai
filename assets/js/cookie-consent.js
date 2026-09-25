/**
 * PromptHook AI - Cookie Consent Banner
 * Compliant with Google AdSense, GDPR, CCPA & DoubleClick DART requirements.
 * Stores preferences locally without external tracking.
 */
(function() {
  'use strict';

  const STORAGE_KEY = 'prompthook_cookie_consent';

  function initCookieConsent() {
    const existingConsent = localStorage.getItem(STORAGE_KEY);
    if (existingConsent) {
      return;
    }

    const banner = document.createElement('aside');
    banner.className = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie and Privacy Consent');
    banner.innerHTML = `
      <div class="cookie-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--brand-amber);">
          <path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5"></path>
          <path d="M8.5 8.5v.01"></path>
          <path d="M16 15.5v.01"></path>
          <path d="M12 12v.01"></path>
          <path d="M11 17v.01"></path>
          <path d="M7 13v.01"></path>
        </svg>
        Cookie & Ad Preferences
      </div>
      <p class="cookie-text">
        PromptHook AI uses essential cookies and Google AdSense compliant telemetry to analyze traffic, personalize ads, and deliver hyper-optimized prompt streaming. Read our <a href="/privacy.html">Privacy Policy</a>.
      </p>
      <div class="cookie-actions">
        <button type="button" class="btn-cookie-accept" id="btnAcceptCookies">Accept All</button>
        <button type="button" class="btn-cookie-decline" id="btnDeclineCookies">Essential Only</button>
      </div>
    `;

    document.body.appendChild(banner);

    // Smooth show
    setTimeout(() => {
      banner.classList.add('show');
    }, 400);

    const acceptBtn = banner.querySelector('#btnAcceptCookies');
    const declineBtn = banner.querySelector('#btnDeclineCookies');

    if (acceptBtn) {
      acceptBtn.addEventListener('click', () => {
        localStorage.setItem(STORAGE_KEY, 'accepted_all');
        banner.classList.remove('show');
        setTimeout(() => banner.remove(), 400);
      });
    }

    if (declineBtn) {
      declineBtn.addEventListener('click', () => {
        localStorage.setItem(STORAGE_KEY, 'essential_only');
        banner.classList.remove('show');
        setTimeout(() => banner.remove(), 400);
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCookieConsent);
  } else {
    initCookieConsent();
  }
})();
