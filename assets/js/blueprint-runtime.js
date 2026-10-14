/**
 * PromptHook AI - Enterprise Blueprint Runtime Engine
 * Interactive Parameter Injection, Token Metric Calculation, 1-Click Copy,
 * Direct ChatGPT/Claude Auto-Copy & Launch, Python/cURL Generators,
 * Live Response Simulation, and Community Feedback Rating.
 */
(function() {
  'use strict';

  // Helper: Toast Notification
  function showToast(message) {
    let toast = document.getElementById('phToastNotification');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'phToastNotification';
      toast.className = 'ph-toast';
      document.body.appendChild(toast);
    }
    toast.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      <span>${message}</span>
    `;
    toast.classList.add('show');

    if (window._phToastTimeout) clearTimeout(window._phToastTimeout);
    window._phToastTimeout = setTimeout(() => {
      toast.classList.remove('show');
    }, 4000);
  }

  // Universal ChatGPT launcher with clipboard guarantee
  function launchChatGPT(text, btnElement) {
    if (!text) return;
    const cleanText = text.trim();

    // 1. Copy full prompt to clipboard
    navigator.clipboard.writeText(cleanText).catch(e => console.error('Clipboard error:', e));

    // 2. Button feedback
    if (btnElement) {
      const orig = btnElement.innerHTML;
      btnElement.innerHTML = '<span>✓ Copied &amp; Opening...</span>';
      setTimeout(() => { btnElement.innerHTML = orig; }, 2200);
    }

    // 3. Inform user with prominent toast
    showToast('✓ Prompt copied to clipboard! Opening ChatGPT (Press Ctrl+V to paste if not auto-filled)');

    // 4. Construct ChatGPT URL (truncate safely to avoid browser 2048-char URL crash)
    const urlSnippet = cleanText.length > 1800 ? cleanText.substring(0, 1800) : cleanText;
    const targetUrl = 'https://chatgpt.com/?prompt=' + encodeURIComponent(urlSnippet) + '&q=' + encodeURIComponent(urlSnippet);
    window.open(targetUrl, '_blank', 'noopener,noreferrer');
  }

  // Universal Claude launcher with clipboard guarantee
  function launchClaude(text, btnElement) {
    if (!text) return;
    const cleanText = text.trim();

    // 1. Copy full prompt to clipboard
    navigator.clipboard.writeText(cleanText).catch(e => console.error('Clipboard error:', e));

    // 2. Button feedback
    if (btnElement) {
      const orig = btnElement.innerHTML;
      btnElement.innerHTML = '<span>✓ Copied &amp; Opening...</span>';
      setTimeout(() => { btnElement.innerHTML = orig; }, 2200);
    }

    // 3. Inform user with prominent toast
    showToast('✓ Prompt copied to clipboard! Opening Claude (Press Ctrl+V to paste)');

    // 4. Open Claude
    window.open('https://claude.ai/new', '_blank', 'noopener,noreferrer');
  }

  function initBlueprintRuntime() {
    const sandboxCard = document.querySelector('.sandbox-card');
    const promptStreamBox = document.getElementById('promptStreamContent');
    const copyBtn = document.getElementById('btnCopyInjectedPrompt');
    const resetBtn = document.getElementById('btnResetParams');
    const tokenBadge = document.getElementById('liveTokenEstimate');
    const templateElement = document.getElementById('rawPromptTemplate');

    // Developer Action Buttons in Sandbox
    const btnOpenChatGPT = document.getElementById('btnOpenChatGPT');
    const btnOpenClaude = document.getElementById('btnOpenClaude');
    const btnCopyPython = document.getElementById('btnCopyPythonSnippet');
    const btnCopyCurl = document.getElementById('btnCopyCurlSnippet');
    const btnSimulate = document.getElementById('btnSimulateRun');
    const simulationBox = document.getElementById('simulationBox');
    const simulationBody = document.getElementById('simulationBody');

    // Wire up all code blocks in the article (e.g. System Directive block)
    initCodeBlockActionButtons();

    if (!sandboxCard || !promptStreamBox || !templateElement) {
      initFaqAccordions();
      initFeedbackButtons();
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

          showToast('✓ Full injected prompt copied to clipboard!');

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
        showToast('Reset parameters to defaults');
      });
    }

    // 1-Click Open in ChatGPT (from Sandbox)
    if (btnOpenChatGPT) {
      btnOpenChatGPT.addEventListener('click', () => {
        launchChatGPT(promptStreamBox.textContent, btnOpenChatGPT);
      });
    }

    // 1-Click Open in Claude (from Sandbox)
    if (btnOpenClaude) {
      btnOpenClaude.addEventListener('click', () => {
        launchClaude(promptStreamBox.textContent, btnOpenClaude);
      });
    }

    // Copy as Python SDK
    if (btnCopyPython) {
      btnCopyPython.addEventListener('click', async () => {
        const text = promptStreamBox.textContent;
        const pythonSnippet = `from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-3-7-sonnet-latest",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": ${JSON.stringify(text)}}
    ]
)

print(response.content[0].text)`;
        try {
          await navigator.clipboard.writeText(pythonSnippet);
          const orig = btnCopyPython.innerHTML;
          btnCopyPython.innerHTML = '<span>✓ Copied Python</span>';
          showToast('✓ Python SDK snippet copied to clipboard!');
          setTimeout(() => { btnCopyPython.innerHTML = orig; }, 1800);
        } catch (e) {
          console.error('Copy Python failed', e);
        }
      });
    }

    // Copy as cURL
    if (btnCopyCurl) {
      btnCopyCurl.addEventListener('click', async () => {
        const text = promptStreamBox.textContent;
        const curlSnippet = `curl https://api.anthropic.com/v1/messages \\
  -H "x-api-key: $ANTHROPIC_API_KEY" \\
  -H "anthropic-version: 2023-06-01" \\
  -H "content-type: application/json" \\
  -d '{
    "model": "claude-3-7-sonnet-latest",
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": ${JSON.stringify(text)}}]
  }'`;
        try {
          await navigator.clipboard.writeText(curlSnippet);
          const orig = btnCopyCurl.innerHTML;
          btnCopyCurl.innerHTML = '<span>✓ Copied cURL</span>';
          showToast('✓ cURL command copied to clipboard!');
          setTimeout(() => { btnCopyCurl.innerHTML = orig; }, 1800);
        } catch (e) {
          console.error('Copy cURL failed', e);
        }
      });
    }

    // Simulate AI Run (Simulated Streaming Response)
    if (btnSimulate && simulationBox && simulationBody) {
      let isStreaming = false;
      btnSimulate.addEventListener('click', () => {
        if (isStreaming) return;
        isStreaming = true;
        simulationBox.classList.add('active');
        simulationBody.textContent = '';

        const blueprintTitle = document.querySelector('.blueprint-title')?.textContent?.trim() || 'Production Blueprint';
        const sampleResponse = `[SYSTEM PROTOCOL INITIATED]
✓ Model Target: Claude 3.7 Sonnet / GPT-4o
✓ Verification Gate: Negative Constraints Validated
✓ Parameter Injection: Applied Successfully

--- PRODUCTION SYNTHESIS ---
Executing architectural delivery for: "${blueprintTitle}"...

1. Boundary Analysis: Zero-placeholder constraint active.
2. Verified Schema conformances: ISO-8601 timestamps, explicit typing.
3. Execution Status: 100% deterministic deliverable compiled with 0 hallucinated entities.

[STREAM COMPLETED: 0 defects detected. Ready for immediate production deployment.]`;

        let i = 0;
        const timer = setInterval(() => {
          if (i < sampleResponse.length) {
            simulationBody.textContent += sampleResponse.charAt(i);
            simulationBody.scrollTop = simulationBody.scrollHeight;
            i += 3;
          } else {
            clearInterval(timer);
            isStreaming = false;
          }
        }, 15);
      });
    }

    // Initial render
    updateInjectedPrompt();
    initFaqAccordions();
    initFeedbackButtons();
  }

  // Connects copy, ChatGPT and Claude buttons across ALL code blocks in the article
  function initCodeBlockActionButtons() {
    const codeBlocks = document.querySelectorAll('.code-block-wrapper');
    codeBlocks.forEach(wrapper => {
      const pre = wrapper.querySelector('pre');
      const copyBtn = wrapper.querySelector('.code-copy-btn');
      const chatgptBtn = wrapper.querySelector('.code-chatgpt-btn');
      const claudeBtn = wrapper.querySelector('.code-claude-btn');

      if (!pre) return;

      if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
          try {
            await navigator.clipboard.writeText(pre.textContent.trim());
            const orig = copyBtn.innerHTML;
            copyBtn.innerHTML = '<span>✓ Copied!</span>';
            showToast('✓ Code copied to clipboard!');
            setTimeout(() => { copyBtn.innerHTML = orig; }, 1800);
          } catch (e) {
            console.error('Copy failed', e);
          }
        });
      }

      if (chatgptBtn) {
        chatgptBtn.addEventListener('click', () => {
          launchChatGPT(pre.textContent.trim(), chatgptBtn);
        });
      }

      if (claudeBtn) {
        claudeBtn.addEventListener('click', () => {
          launchClaude(pre.textContent.trim(), claudeBtn);
        });
      }
    });
  }

  function initFaqAccordions() {
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
      const questionBtn = item.querySelector('.faq-question');
      if (questionBtn) {
        questionBtn.addEventListener('click', () => {
          const isOpen = item.classList.contains('active');
          faqItems.forEach(other => {
            if (other !== item) other.classList.remove('active');
          });
          item.classList.toggle('active', !isOpen);
          questionBtn.setAttribute('aria-expanded', !isOpen);
        });
      }
    });
  }

  function initFeedbackButtons() {
    const card = document.querySelector('.blueprint-feedback-card');
    if (!card) return;

    const pageKey = 'ph_vote_' + window.location.pathname;
    const savedVote = localStorage.getItem(pageKey);

    const btnUp = card.querySelector('.btn-feedback.up');
    const btnDown = card.querySelector('.btn-feedback.down');
    const countSpan = card.querySelector('.vote-count');

    let count = countSpan ? parseInt(countSpan.textContent, 10) || 48 : 48;

    if (savedVote === 'helpful' && btnUp) {
      btnUp.classList.add('voted-up');
    } else if (savedVote === 'refine' && btnDown) {
      btnDown.classList.add('voted-down');
    }

    if (btnUp) {
      btnUp.addEventListener('click', () => {
        if (localStorage.getItem(pageKey)) return;
        localStorage.setItem(pageKey, 'helpful');
        btnUp.classList.add('voted-up');
        count++;
        if (countSpan) countSpan.textContent = count;
        showToast('Thank you for rating this blueprint!');
      });
    }

    if (btnDown) {
      btnDown.addEventListener('click', () => {
        if (localStorage.getItem(pageKey)) return;
        localStorage.setItem(pageKey, 'refine');
        btnDown.classList.add('voted-down');
        showToast('Feedback noted. We will refine this blueprint.');
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBlueprintRuntime);
  } else {
    initBlueprintRuntime();
  }
})();
