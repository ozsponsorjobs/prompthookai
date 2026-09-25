/**
 * PromptHook AI - Blueprint Runtime Engine
 * Interactive Parameter Injection, Token Metric Calculation, 1-Click Copy, and FAQ Interactivity.
 */
(function() {
  'use strict';

  function initBlueprintRuntime() {
    const sandboxCard = document.querySelector('.sandbox-card');
    const promptStreamBox = document.getElementById('promptStreamContent');
    const copyBtn = document.getElementById('btnCopyInjectedPrompt');
    const resetBtn = document.getElementById('btnResetParams');
    const tokenBadge = document.getElementById('liveTokenEstimate');
    const templateElement = document.getElementById('rawPromptTemplate');

    if (!sandboxCard || !promptStreamBox || !templateElement) {
      // Not a blueprint page with sandbox
      initFaqAccordions();
      return;
    }

    const rawTemplate = templateElement.textContent.trim();
    const inputs = sandboxCard.querySelectorAll('[data-param-key]');

    function updateInjectedPrompt() {
      let populated = rawTemplate;
      let totalLength = 0;

      inputs.forEach(input => {
        const key = input.getAttribute('data-param-key');
        const val = input.value || input.placeholder || '';
        const regex = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
        populated = populated.replace(regex, val);
      });

      promptStreamBox.textContent = populated;
      totalLength = populated.length;

      // Estimate tokens (~4 characters per token average in English/code)
      if (tokenBadge) {
        const estimatedTokens = Math.max(1, Math.round(totalLength / 3.9));
        tokenBadge.textContent = `~${estimatedTokens} tokens`;
      }
    }

    // Attach listeners to all parameter inputs
    inputs.forEach(input => {
      input.addEventListener('input', updateInjectedPrompt);
      input.addEventListener('change', updateInjectedPrompt);
    });

    // 1-Click Copy with feedback
    if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        try {
          const textToCopy = promptStreamBox.textContent;
          await navigator.clipboard.writeText(textToCopy);

          const originalText = copyBtn.innerHTML;
          copyBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            Copied to Clipboard!
          `;
          copyBtn.style.background = 'linear-gradient(135deg, #10B981, #059669)';

          setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = '';
          }, 2000);
        } catch (err) {
          console.error('Failed to copy prompt: ', err);
        }
      });
    }

    // Reset parameters to defaults
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        inputs.forEach(input => {
          const defaultVal = input.getAttribute('data-default') || '';
          input.value = defaultVal;
        });
        updateInjectedPrompt();
      });
    }

    // Code blocks copy buttons
    const codeBlocks = document.querySelectorAll('.code-block-wrapper');
    codeBlocks.forEach(wrapper => {
      const btn = wrapper.querySelector('.code-copy-btn');
      const pre = wrapper.querySelector('pre');
      if (btn && pre) {
        btn.addEventListener('click', async () => {
          try {
            await navigator.clipboard.writeText(pre.textContent);
            const orig = btn.innerHTML;
            btn.innerHTML = '<span>Copied!</span>';
            setTimeout(() => {
              btn.innerHTML = orig;
            }, 1800);
          } catch (e) {
            console.error('Copy failed', e);
          }
        });
      }
    });

    // Initial render
    updateInjectedPrompt();
    initFaqAccordions();
  }

  function initFaqAccordions() {
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
      const questionBtn = item.querySelector('.faq-question');
      if (questionBtn) {
        questionBtn.addEventListener('click', () => {
          const isOpen = item.classList.contains('active');
          
          // Optional: close other accordions
          faqItems.forEach(other => {
            if (other !== item) other.classList.remove('active');
          });

          item.classList.toggle('active', !isOpen);
          questionBtn.setAttribute('aria-expanded', !isOpen);
        });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBlueprintRuntime);
  } else {
    initBlueprintRuntime();
  }
})();
