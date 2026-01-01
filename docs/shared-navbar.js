(function() {
  const guidePages = [
    { name: "ARM Templates", url: "arm_templates_guide.html", tags: "arm json deployment infrastructure", domain: "Compute" },
    { name: "Azure CLI & PowerShell", url: "azure_cli_ps_guide.html", tags: "cli powershell az commands", domain: null },
    { name: "Compute Options", url: "azure_compute_options_guide.html", tags: "vm vmss compute scale sets", domain: "Compute" },
    { name: "VNet Deep Dive", url: "azure_vnet_deep_dive_guide.html", tags: "networking peering virtual network vnet", domain: "Networking" },
    { name: "Storage Architecture", url: "azure_storage_architecture_guide.html", tags: "storage blob file queue table", domain: "Storage" },
    { name: "Azure DNS", url: "azure_dns_services_guide.html", tags: "dns zones records networking", domain: "Networking" },
    { name: "Load Balancing", url: "azure_load_balancing_guide.html", tags: "lb networking traffic load balancer", domain: "Networking" },
    { name: "App Gateway", url: "azure_application_gateway_guide.html", tags: "waf layer7 gateway application", domain: "Networking" },
    { name: "NSG Guide", url: "azure_network_security_groups_guide.html", tags: "security rules firewall nsg asg", domain: "Networking" },
    { name: "Azure Policy", url: "azure_policy_guide.html", tags: "governance compliance policy", domain: "Identities" },
    { name: "Entra ID", url: "microsoft_entra_id_concepts_guide.html", tags: "entra id azure ad identity authentication rbac", domain: "Identities" },
    { name: "Disaster Recovery", url: "azure_disaster_recovery_comprehensive_guide.html", tags: "backup recovery vault dr asr", domain: "Monitoring" },
    { name: "Monitor Maintenance", url: "azure_monitor_maintenance_guide.html", tags: "monitoring logs alerts metrics", domain: "Monitoring" },
    { name: "App Service", url: "azure_app_service_guide.html", tags: "webapp paas deployment app service", domain: "App Service & Containers" },
    { name: "Container Instances", url: "azure_aci_container_groups_guide.html", tags: "aci containers docker", domain: "App Service & Containers" },
    { name: "Docker Concepts", url: "azure_docker_concepts_guide.html", tags: "docker containers", domain: "App Service & Containers" },
    { name: "VM CLI Lab", url: "az104_vm_cli_lab_guide.html", tags: "vm lab cli virtual machine", domain: "Compute" },
    { name: "VNet Peering Lab", url: "az104_vnet_peering_cli_lab_guide.html", tags: "vnet peering lab networking", domain: "Networking" },
    { name: "Compute Quiz", url: "azure_compute_vca_quiz.html", tags: "quiz compute vm scale sets", domain: "Compute" },
    { name: "Networking Quiz", url: "azure_networking_quiz.html", tags: "quiz networking vnet nsg", domain: "Networking" },
    { name: "Storage Replication", url: "azure_storage_replication_rto_rpo_guide.html", tags: "storage replication rto rpo lrs grs zrs", domain: "Storage" },
    { name: "Storage Lifecycle", url: "Azure_storage_lifecycle_tiers_guide.html", tags: "storage lifecycle tiers hot cool archive", domain: "Storage" },
    { name: "VMs Deep Dive", url: "azure_vms_deep_dive_guide.html", tags: "vm virtual machine compute", domain: "Compute" },
    { name: "VMSS Guide", url: "azure_vmss_guide.html", tags: "vmss scale sets compute", domain: "Compute" },
    { name: "VPN Gateway", url: "azure_vpn_gateway_guide.html", tags: "vpn gateway networking", domain: "Networking" },
    { name: "ExpressRoute", url: "azure_expressroute_guide.html", tags: "expressroute networking connectivity", domain: "Networking" },
    { name: "Azure Firewall", url: "azure_firewall_guide.html", tags: "firewall security networking", domain: "Networking" },
    { name: "Personalized Review", url: "azure_personalized_review_guide.html", tags: "review scores progress weak points", domain: null }
  ];

  function getWeakDomains() {
    try {
      const scores = JSON.parse(localStorage.getItem('mergedQuizScores') || '{}');
      const domainScores = [];
      for (const [domain, data] of Object.entries(scores)) {
        if (data && data.total > 0) {
          const pct = Math.round((data.correct / data.total) * 100);
          domainScores.push({ domain, pct, correct: data.correct, total: data.total });
        }
      }
      domainScores.sort((a, b) => a.pct - b.pct);
      return domainScores.slice(0, 2);
    } catch (e) {
      return [];
    }
  }

  function getPersonalizedSuggestions() {
    const weakDomains = getWeakDomains();
    if (weakDomains.length === 0) return [];
    
    const suggestions = [];
    for (const weak of weakDomains) {
      const domainGuides = guidePages.filter(g => g.domain === weak.domain).slice(0, 2);
      for (const guide of domainGuides) {
        suggestions.push({
          ...guide,
          reason: `${weak.domain} (${weak.pct}%)`,
          isPersonalized: true
        });
      }
    }
    return suggestions.slice(0, 4);
  }

  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  
  function getActiveClass(page) {
    if (currentPage === page) return 'active-tool';
    if (currentPage === 'index.html' && page === 'azure_personalized_review_guide.html') return '';
    return '';
  }

  const navbarHTML = `
    <nav class="az104-shared-navbar" id="az104-shared-navbar">
      <div class="navbar-brand">
        <a href="index.html">
          <i class="fas fa-graduation-cap"></i>
          <span>AZ-104 Hub</span>
        </a>
      </div>
      <div class="navbar-search">
        <div class="search-container">
          <i class="fas fa-search search-icon"></i>
          <input type="text" id="navbar-search-input" placeholder="Search guides..." autocomplete="off">
          <div class="search-results" id="navbar-search-results"></div>
        </div>
      </div>
      <div class="navbar-tools">
        <a href="azure_personalized_review_guide.html" class="navbar-tool-btn ${getActiveClass('azure_personalized_review_guide.html')}">
          <i class="fas fa-bullseye"></i>
          <span>Review</span>
        </a>
        <a href="anki-deck-builder.html" class="navbar-tool-btn ${getActiveClass('anki-deck-builder.html')}">
          <i class="fas fa-hammer"></i>
          <span>Builder</span>
        </a>
        <a href="anki-deck-library.html" class="navbar-tool-btn ${getActiveClass('anki-deck-library.html')}">
          <i class="fas fa-layer-group"></i>
          <span>Library</span>
        </a>
        <button class="navbar-tool-btn theme-toggle-nav" id="navbar-theme-toggle" title="Toggle dark/light mode">
          <i class="fas fa-moon"></i>
        </button>
      </div>
    </nav>
  `;

  const navbarCSS = `
    <style id="az104-navbar-styles">
      .az104-shared-navbar {
        position: sticky;
        top: 0;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 16px;
        background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        flex-wrap: wrap;
        gap: 10px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      }
      .az104-shared-navbar * { box-sizing: border-box; }
      .navbar-brand a {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #fff;
        text-decoration: none;
        font-weight: 700;
        font-size: 1em;
      }
      .navbar-brand i { color: #60a5fa; font-size: 1.1em; }
      .navbar-search { flex: 1; max-width: 300px; min-width: 150px; }
      .search-container {
        position: relative;
        width: 100%;
      }
      .search-icon {
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        color: rgba(255,255,255,0.5);
        font-size: 12px;
        pointer-events: none;
      }
      #navbar-search-input {
        width: 100%;
        padding: 8px 12px 8px 32px;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 6px;
        background: rgba(255,255,255,0.1);
        color: #fff;
        font-size: 13px;
        outline: none;
        transition: all 0.2s;
      }
      #navbar-search-input::placeholder { color: rgba(255,255,255,0.5); }
      #navbar-search-input:focus {
        background: rgba(255,255,255,0.15);
        border-color: #60a5fa;
      }
      .search-results {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: #1e3a5f;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 6px;
        margin-top: 4px;
        max-height: 300px;
        overflow-y: auto;
        display: none;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      }
      .search-results.active { display: block; }
      .search-result-item {
        padding: 10px 12px;
        color: #fff;
        text-decoration: none;
        display: block;
        font-size: 13px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        transition: background 0.2s;
      }
      .search-result-item:hover { background: rgba(255,255,255,0.1); }
      .search-result-item:last-child { border-bottom: none; }
      .search-result-item i { margin-right: 8px; color: #60a5fa; }
      .search-result-item.personalized { border-left: 3px solid #f59e0b; }
      .search-result-item .result-reason { font-size: 11px; color: #f59e0b; margin-left: 8px; }
      .search-section-header { padding: 8px 12px; font-size: 11px; color: #f59e0b; text-transform: uppercase; font-weight: 600; background: rgba(245,158,11,0.1); }
      .no-results {
        padding: 12px;
        color: rgba(255,255,255,0.6);
        font-size: 13px;
        text-align: center;
      }
      .navbar-tools {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .navbar-tool-btn {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 7px 12px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 6px;
        color: #fff;
        text-decoration: none;
        font-size: 12px;
        font-weight: 500;
        transition: all 0.2s;
        white-space: nowrap;
      }
      .navbar-tool-btn:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-1px);
      }
      .navbar-tool-btn.active-tool {
        background: #0078d4;
        border-color: #0078d4;
      }
      .navbar-tool-btn i { font-size: 12px; }
      @media (max-width: 600px) {
        .az104-shared-navbar { padding: 8px 10px; }
        .navbar-tool-btn span { display: none; }
        .navbar-tool-btn { padding: 8px; }
        .navbar-tool-btn i { font-size: 14px; }
        .navbar-search { order: 3; flex-basis: 100%; max-width: 100%; }
        .navbar-brand span { display: none; }
      }
    </style>
  `;

  function initNavbar() {
    if (document.getElementById('az104-shared-navbar')) return;
    
    document.head.insertAdjacentHTML('beforeend', navbarCSS);
    document.body.insertAdjacentHTML('afterbegin', navbarHTML);

    const searchInput = document.getElementById('navbar-search-input');
    const searchResults = document.getElementById('navbar-search-results');

    // Theme toggle functionality
    const themeToggle = document.getElementById('navbar-theme-toggle');
    if (themeToggle) {
      function updateThemeIcon() {
        const isDark = document.body.classList.contains('dark-mode');
        themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
      }
      
      themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        localStorage.setItem('az104-theme', isDark ? 'dark' : 'light');
        updateThemeIcon();
      });
      
      // Initialize from localStorage
      const savedTheme = localStorage.getItem('az104-theme');
      if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
      }
      updateThemeIcon();
    }

    if (searchInput && searchResults) {
      function showPersonalizedSuggestions() {
        const personalized = getPersonalizedSuggestions();
        if (personalized.length > 0) {
          let html = '<div class="search-section-header"><i class="fas fa-bullseye"></i> Focus on weak areas</div>';
          html += personalized.map(page => 
            `<a href="${page.url}" class="search-result-item personalized">
              <i class="fas fa-fire"></i>${page.name}<span class="result-reason">${page.reason}</span>
            </a>`
          ).join('');
          searchResults.innerHTML = html;
          searchResults.classList.add('active');
        } else {
          searchResults.innerHTML = '';
          searchResults.classList.remove('active');
        }
      }

      searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        if (query.length < 2) {
          showPersonalizedSuggestions();
          return;
        }

        const matches = guidePages.filter(page => 
          page.name.toLowerCase().includes(query) || 
          page.tags.toLowerCase().includes(query)
        ).slice(0, 8);

        if (matches.length > 0) {
          searchResults.innerHTML = matches.map(page => 
            `<a href="${page.url}" class="search-result-item">
              <i class="fas fa-file-alt"></i>${page.name}
            </a>`
          ).join('');
        } else {
          searchResults.innerHTML = '<div class="no-results">No guides found</div>';
        }
        searchResults.classList.add('active');
      });

      searchInput.addEventListener('blur', function() {
        setTimeout(() => searchResults.classList.remove('active'), 200);
      });

      searchInput.addEventListener('focus', function() {
        if (this.value.length >= 2) {
          searchResults.classList.add('active');
        } else {
          showPersonalizedSuggestions();
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNavbar);
  } else {
    initNavbar();
  }
})();
