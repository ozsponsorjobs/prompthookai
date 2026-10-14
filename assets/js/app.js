/**
 * PromptHook AI - Main Application & Instant Client-Side Search Engine
 * Zero-framework, zero-backend, 100% static client-side search across 1,960+ blueprints.
 * Latency: < 2ms.
 */
(function() {
  'use strict';

  let searchIndex = null;
  let isFetchingIndex = false;

  async function loadSearchIndex() {
    if (searchIndex || isFetchingIndex) return;
    isFetchingIndex = true;
    try {
      const response = await fetch('/assets/data/search-index.json');
      if (response.ok) {
        searchIndex = await response.json();
        const badge = document.getElementById('searchCountBadge');
        if (badge && searchIndex) {
          badge.textContent = `${searchIndex.length.toLocaleString()} Blueprints Indexed`;
        }
      }
    } catch (err) {
      console.warn('Could not load search index:', err);
    } finally {
      isFetchingIndex = false;
    }
  }

  function highlightMatches(text, query) {
    if (!query) return escapeHtml(text);
    const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedQuery})`, 'gi');
    return escapeHtml(text).replace(regex, '<mark>$1</mark>');
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function initApp() {
    const searchInput = document.getElementById('globalBlueprintSearch');
    const searchDropdown = document.getElementById('instantSearchResults');
    const filterPills = document.querySelectorAll('.pill-btn');
    const staticCards = document.querySelectorAll('.blueprint-card');
    const countBadge = document.getElementById('searchCountBadge');

    let selectedIndex = -1;

    // Preload index on hover or focus
    if (searchInput) {
      searchInput.addEventListener('focus', loadSearchIndex);
      searchInput.addEventListener('mouseenter', loadSearchIndex);

      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim().toLowerCase();
        handleSearch(query);
      });

      // Keyboard navigation
      searchInput.addEventListener('keydown', (e) => {
        if (!searchDropdown || searchDropdown.style.display === 'none') return;
        const items = searchDropdown.querySelectorAll('.search-result-item');
        if (!items.length) return;

        if (e.key === 'ArrowDown') {
          e.preventDefault();
          selectedIndex = (selectedIndex + 1) % items.length;
          updateSelected(items);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          selectedIndex = (selectedIndex - 1 + items.length) % items.length;
          updateSelected(items);
        } else if (e.key === 'Enter') {
          e.preventDefault();
          if (selectedIndex >= 0 && items[selectedIndex]) {
            items[selectedIndex].click();
          }
        } else if (e.key === 'Escape') {
          closeDropdown();
        }
      });
    }

    function updateSelected(items) {
      items.forEach((item, idx) => {
        if (idx === selectedIndex) {
          item.classList.add('selected');
          item.scrollIntoView({ block: 'nearest' });
        } else {
          item.classList.remove('selected');
        }
      });
    }

    function closeDropdown() {
      if (searchDropdown) {
        searchDropdown.style.display = 'none';
        searchDropdown.innerHTML = '';
        selectedIndex = -1;
      }
    }

    // Close dropdown on click outside
    document.addEventListener('click', (e) => {
      if (searchInput && searchDropdown) {
        if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
          closeDropdown();
        }
      }
    });

    async function handleSearch(query) {
      if (!query || query.length < 2) {
        closeDropdown();
        // Also show all static featured cards
        staticCards.forEach(c => c.style.display = '');
        if (countBadge && searchIndex) {
          countBadge.textContent = `${searchIndex.length.toLocaleString()} Blueprints Indexed`;
        }
        return;
      }

      if (!searchIndex) {
        await loadSearchIndex();
      }

      if (!searchIndex || !searchDropdown) return;

      const terms = query.split(/\s+/).filter(Boolean);
      const matches = [];

      for (let i = 0; i < searchIndex.length; i++) {
        const item = searchIndex[i];
        const titleLower = item.t.toLowerCase();
        const urlLower = item.u.toLowerCase();
        const catLower = item.c.toLowerCase();

        // Must match all query terms
        let matchAll = true;
        for (let j = 0; j < terms.length; j++) {
          const t = terms[j];
          if (!titleLower.includes(t) && !urlLower.includes(t) && !catLower.includes(t)) {
            matchAll = false;
            break;
          }
        }

        if (matchAll) {
          matches.push(item);
        }
      }

      // Sort: Flagship items first, then exact start matches
      matches.sort((a, b) => {
        if (a.f !== b.f) return b.f - a.f;
        const aStarts = a.t.toLowerCase().startsWith(query);
        const bStarts = b.t.toLowerCase().startsWith(query);
        if (aStarts && !bStarts) return -1;
        if (!aStarts && bStarts) return 1;
        return 0;
      });

      selectedIndex = -1;
      renderDropdown(matches, query);
    }

    function renderDropdown(matches, query) {
      if (!searchDropdown) return;

      if (matches.length === 0) {
        searchDropdown.innerHTML = `
          <div class="search-no-results">
            <p>No blueprints found matching "<strong>${escapeHtml(query)}</strong>"</p>
            <span style="font-size: 0.8rem; color: var(--text-muted);">Try terms like: Python, Agents, SEO, React, Docker, SQL, or Gemini</span>
          </div>
        `;
        searchDropdown.style.display = 'block';
        return;
      }

      const totalMatches = matches.length;
      const displayLimit = 25;
      const displayItems = matches.slice(0, displayLimit);

      let html = `
        <div class="search-results-header">
          <span>FOUND ${totalMatches.toLocaleString()} MATCHING BLUEPRINTS</span>
          <span>Showing top ${displayItems.length} &bull; Use ↑↓ to navigate</span>
        </div>
      `;

      displayItems.forEach(item => {
        const highlightedTitle = highlightMatches(item.t, query);
        html += `
          <a href="${item.u}" class="search-result-item">
            <div class="search-item-info">
              <span class="search-item-title">${highlightedTitle}</span>
              <span class="search-item-url">${escapeHtml(item.u)}</span>
            </div>
            <span class="search-item-badge">${escapeHtml(item.c)}</span>
          </a>
        `;
      });

      searchDropdown.innerHTML = html;
      searchDropdown.style.display = 'block';

      if (countBadge) {
        countBadge.textContent = `${totalMatches} matching`;
      }
    }

    // Category Filter Pills on Homepage
    if (filterPills.length > 0) {
      filterPills.forEach(pill => {
        pill.addEventListener('click', async () => {
          filterPills.forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          const cat = pill.getAttribute('data-filter') || 'all';

          if (cat === 'all') {
            staticCards.forEach(c => c.style.display = '');
            closeDropdown();
          } else {
            if (!searchIndex) await loadSearchIndex();
            if (searchIndex && searchInput) {
              searchInput.value = '';
              // Filter index by category
              const catMatches = searchIndex.filter(item => item.cat_id === cat);
              renderDropdown(catMatches, '');
              if (searchDropdown) {
                const header = searchDropdown.querySelector('.search-results-header');
                if (header) {
                  header.innerHTML = `<span>CATEGORY SILO: ${catMatches.length} BLUEPRINTS</span><span>Showing top 25</span>`;
                }
              }
            }
          }
        });
      });
    }

    // Mobile nav toggle
    const mobileMenuBtn = document.getElementById('mobileMenuToggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileMenuBtn && navLinks) {
      mobileMenuBtn.addEventListener('click', () => {
        const isOpen = navLinks.style.display === 'flex';
        navLinks.style.display = isOpen ? 'none' : 'flex';
        navLinks.style.flexDirection = 'column';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '100%';
        navLinks.style.left = '0';
        navLinks.style.right = '0';
        navLinks.style.backgroundColor = 'rgba(9, 13, 22, 0.98)';
        navLinks.style.padding = '1.5rem';
        navLinks.style.borderBottom = '1px solid var(--border-color)';
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();
