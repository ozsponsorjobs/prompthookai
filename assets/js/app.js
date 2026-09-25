/**
 * PromptHook AI - Main Application Controller
 * High-performance instant live filtering, keyword search, and responsive navigation.
 */
(function() {
  'use strict';

  function initApp() {
    const searchInput = document.getElementById('globalBlueprintSearch');
    const filterPills = document.querySelectorAll('.pill-btn');
    const cards = document.querySelectorAll('.blueprint-card');
    const countBadge = document.getElementById('searchCountBadge');
    const noResultsMsg = document.getElementById('noResultsState');

    let activeCategory = 'all';
    let searchQuery = '';

    function filterBlueprints() {
      let visibleCount = 0;
      const normalizedQuery = searchQuery.trim().toLowerCase();

      cards.forEach(card => {
        const cardCategory = card.getAttribute('data-category') || '';
        const cardTitle = (card.querySelector('.card-title')?.textContent || '').toLowerCase();
        const cardDesc = (card.querySelector('.card-description')?.textContent || '').toLowerCase();
        const cardTags = (card.getAttribute('data-tags') || '').toLowerCase();

        const matchesCategory = (activeCategory === 'all' || cardCategory === activeCategory);
        const matchesQuery = !normalizedQuery || 
          cardTitle.includes(normalizedQuery) || 
          cardDesc.includes(normalizedQuery) || 
          cardTags.includes(normalizedQuery);

        if (matchesCategory && matchesQuery) {
          card.style.display = '';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (countBadge) {
        countBadge.textContent = `${visibleCount} blueprints found`;
      }

      if (noResultsMsg) {
        noResultsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
      }
    }

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        searchQuery = e.target.value;
        filterBlueprints();
      });
    }

    if (filterPills.length > 0) {
      filterPills.forEach(pill => {
        pill.addEventListener('click', () => {
          filterPills.forEach(p => p.classList.remove('active'));
          pill.classList.add('active');
          activeCategory = pill.getAttribute('data-filter') || 'all';
          filterBlueprints();
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
