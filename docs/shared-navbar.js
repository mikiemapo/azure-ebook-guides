(function() {
  const guidePages = [
    { name: "ARM Templates", url: "arm_templates_guide.html", tags: "arm json deployment infrastructure" },
    { name: "Azure CLI & PowerShell", url: "azure_cli_ps_guide.html", tags: "cli powershell az commands" },
    { name: "Compute Options", url: "azure_compute_options_guide.html", tags: "vm vmss compute" },
    { name: "VNet Peering", url: "azure_vnet_peering_guide.html", tags: "networking peering virtual network" },
    { name: "Storage Accounts", url: "azure_storage_accounts_guide.html", tags: "storage blob file queue table" },
    { name: "Azure DNS", url: "azure_dns_services_guide.html", tags: "dns zones records" },
    { name: "Load Balancer", url: "azure_load_balancer_guide.html", tags: "lb networking traffic" },
    { name: "App Gateway", url: "azure_application_gateway_guide.html", tags: "waf layer7 gateway" },
    { name: "NSG & ASG", url: "azure_nsg_asg_guide.html", tags: "security rules firewall" },
    { name: "Azure Policy", url: "azure_policy_guide.html", tags: "governance compliance" },
    { name: "RBAC", url: "azure_rbac_guide.html", tags: "roles permissions access" },
    { name: "Azure Backup", url: "azure_backup_guide.html", tags: "backup recovery vault" },
    { name: "Azure Monitor", url: "azure_monitor_guide.html", tags: "monitoring logs alerts" },
    { name: "App Service", url: "azure_app_service_guide.html", tags: "webapp paas deployment" },
    { name: "Container Instances", url: "azure_aci_container_groups_guide.html", tags: "aci containers docker" },
    { name: "Docker Concepts", url: "azure_docker_concepts_guide.html", tags: "docker containers" },
    { name: "Disaster Recovery", url: "azure_disaster_recovery_comprehensive_guide.html", tags: "dr asr backup" },
    { name: "VM CLI Lab", url: "az104_vm_cli_lab_guide.html", tags: "vm lab cli" },
    { name: "VNet Peering Lab", url: "az104_vnet_peering_cli_lab_guide.html", tags: "vnet peering lab" },
    { name: "Identities Quiz", url: "azure_identities_vca_quiz.html", tags: "quiz identities entra" },
    { name: "Storage Quiz", url: "azure_storage_vca_quiz.html", tags: "quiz storage" },
    { name: "Compute Quiz", url: "azure_compute_vca_quiz.html", tags: "quiz compute vm" },
    { name: "Networking Quiz", url: "azure_networking_vca_quiz.html", tags: "quiz networking" }
  ];

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

    if (searchInput && searchResults) {
      searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        if (query.length < 2) {
          searchResults.classList.remove('active');
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
