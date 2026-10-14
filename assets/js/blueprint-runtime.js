/**
 * PromptHook AI - Enterprise Blueprint Runtime Engine
 * Interactive Parameter Injection, Token Metric Calculation, 1-Click Copy,
 * ChatGPT/Claude 1-Click Export, Python/cURL Generators, Live Response Simulation,
 * and Community Feedback Rating.
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

    // Developer Action Buttons
    const btnOpenChatGPT = document.getElementById('btnOpenChatGPT');
    const btnOpenClaude = document.getElementById('btnOpenClaude');
    const btnCopyPython = document.getElementById('btnCopyPythonSnippet');
    const btnCopyCurl = document.getElementById('btnCopyCurlSnippet');
    const btnSimulate = document.getElementById('btnSimulateRun');
    const simulationBox = document.getElementById('simulationBox');
    const simulationBody = document.getElementById('simulationBody');

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

    // 1-Click Open in ChatGPT
    if (btnOpenChatGPT) {
      btnOpenChatGPT.addEventListener('click', () => {
        const text = promptStreamBox.textContent;
        const url = 'https://chatgpt.com/?q=' + encodeURIComponent(text);
        window.open(url, '_blank', 'noopener,noreferrer');
      });
    }

    // 1-Click Open in Claude
    if (btnOpenClaude) {
      btnOpenClaude.addEventListener('click', () => {
        const text = promptStreamBox.textContent;
        const url = 'https://claude.ai/new?q=' + encodeURIComponent(text);
        window.open(url, '_blank', 'noopener,noreferrer');
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
    initFeedbackButtons();
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
      });
    }

    if (btnDown) {
      btnDown.addEventListener('click', () => {
        if (localStorage.getItem(pageKey)) return;
        localStorage.setItem(pageKey, 'refine');
        btnDown.classList.add('voted-down');
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBlueprintRuntime);
  } else {
    initBlueprintRuntime();
  }
})();
