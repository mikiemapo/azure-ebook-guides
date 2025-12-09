# Azure AZ-104 Study Guides - HTML Repository

**Repository:** [azure-ebook-guides](https://github.com/mikiemapo/azure-ebook-guides)  
**Live Site:** https://mikiemapo.github.io/azure-ebook-guides/  
**Last Updated:** November 22, 2025

---

## 📚 Repository Overview

This repository contains **86 interactive HTML study guides** for the Microsoft Azure Administrator (AZ-104) certification exam. All guides are deployed via GitHub Pages and synced to iCloud (Readdle Documents) for offline mobile access.

**Questioning Method (for all decks):** We use the standardized MCQ/True-False style documented in `Anki-Decks/README.md` (see "Questioning Method (Documented System)"). Default to MCQ; use True/False only for binary, always/never rules.

### Key Features

- ✅ **Interactive collapsible cards** with toggle animations
- ✅ **Color-coded sections** using CSS custom properties (`:root` variables)
- ✅ **Responsive design** with mobile-first approach
- ✅ **Font Awesome icons** for visual hierarchy
- ✅ **Anchor navigation** for deep-linking to specific sections
- ✅ **Mind maps & diagrams** for visual learning
- ✅ **Quick jump menus** for rapid navigation
- ✅ **Quiz integration** with instant feedback

---

## 🏗️ Architecture & Structure

### File Organization

```
docs/
├── index.html                          # Main study hub (navigation center)
├── azure_app_service_guide.html        # App Service deep dive
├── azure_aci_container_groups_guide.html # Container Instances
├── azure_vms_deep_dive_guide.html      # Virtual Machines
├── azure_storage_replication_rto_rpo_guide.html # Storage RTO/RPO
├── azure_personalized_review_guide.html # Weak spot tracker
├── [80+ other guides]
├── media_catalog.csv                   # Media file index (deprecated)
└── embedded_media_function.js          # Media loader (deprecated)
```

### Guide Categories

1. **Critical Study Priorities** (3 guides)

   - Storage RTO/RPO Replication Strategy
   - Compute Domain (Fault/Update Domains)
   - App Service & Containers

2. **Core Azure Services** (60+ guides)

   - Compute (VMs, VMSS, App Services, ACI, AKS)
   - Networking (VNets, NSGs, Load Balancers, VPN, DNS)
   - Storage (Blobs, Files, Replication, Lifecycle)
   - Identity (Entra ID, RBAC, Key Vault)
   - Governance (Policy, ARM, Terraform)
   - Monitoring (Azure Monitor, Network Watcher)

3. **Interactive Tools** (12 guides)
   - Scenario sorters (drag-and-drop)
   - Quizzes (multiple choice)
   - Flashcards (spaced repetition)
   - CLI labs (hands-on practice)

---

## 🎨 CSS Architecture

### Design System (CSS Custom Properties)

All guides use a **consistent `:root` variable system** for theming and maintainability:

```css
:root {
  /* Core Azure Brand Colors */
  --azure-blue: #0078d4;
  --azure-blue-dark: #005a9e;
  --azure-bg-light: #f0f4f8;

  /* Text & UI Colors */
  --text-dark: #323130;
  --text-light: #ffffff;
  --border-color: #d1d1d1;
  --card-bg: #ffffff;
  --diagram-bg: #f8f9fa;
  --shadow-color: rgba(0, 0, 0, 0.1);

  /* Semantic Colors */
  --success-color: #107c10;
  --warning-color: #d83b01;
  --info-color: #005a9e;

  /* Domain-Specific Colors (vary by guide) */
  --appservice-color: #107c10; /* Green for App Service */
  --security-color: #a4262c; /* Red for Security */
  --networking-color: #2874a6; /* Blue for Networking */
  --storage-color: #8e44ad; /* Purple for Storage */
  --compute-color: #f39c12; /* Orange for Compute */
}
```

### Critical CSS Patterns

#### 1. **Collapsible Card System**

The core interactive pattern used across all guides:

```css
/* Hidden checkbox controls the toggle state */
.card-toggle {
  display: none;
}

/* Clickable header with color-coded background */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  background-color: var(--appservice-color);
  color: var(--text-light);
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid #0d6a0d;
}

/* Hover effect for interactivity feedback */
.card-header:hover {
  background-color: #0d6a0d;
}

/* Toggle icon rotation animation */
.card-header .toggle-icon {
  font-size: 1.1em;
  transition: transform 0.3s ease;
}

/* Content starts hidden with max-height: 0 */
.card-content {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  padding: 0 18px;
  transition: max-height 0.4s ease-out, opacity 0.3s ease-in,
    padding 0.4s ease-out;
  background-color: var(--card-bg);
}

/* When checkbox is checked, expand content */
.card-toggle:checked + .card-header .toggle-icon {
  transform: rotate(180deg);
}

.card-toggle:checked ~ .card-content {
  max-height: 2500px; /* ⚠️ IMPORTANT: Adjust per guide */
  opacity: 1;
  padding: 15px 18px;
  overflow-y: auto;
}
```

**⚠️ KNOWN ISSUE - `max-height` Struggles:**

- **Problem:** Different guides have varying content lengths, requiring manual `max-height` adjustments
- **Symptom:** Content gets cut off if `max-height` is too small, or animation looks sluggish if too large
- **Current Values Used:**
  - Standard guides: `2500px`
  - CLI/Lab guides: `3000px` (longer command outputs)
  - Quiz guides: `3500px` (many questions)
- **Why Not `max-height: none`?** Breaks the CSS transition animation
- **Workaround:** Use `overflow-y: auto` to allow scrolling within cards
- **Future Fix:** Consider JavaScript-based dynamic height calculation

#### 2. **HTML Structure Pattern**

Every collapsible card follows this exact structure:

```html
<div class="card">
  <!-- Hidden checkbox (id must be unique) -->
  <input type="checkbox" id="unique-card-id" class="card-toggle" />

  <!-- Clickable header (label for the checkbox) -->
  <label for="unique-card-id" class="card-header">
    <h2><i class="fas fa-icon"></i> Card Title</h2>
    <span class="toggle-icon">
      <i class="fas fa-chevron-down"></i>
    </span>
  </label>

  <!-- Hidden content (revealed when checkbox is checked) -->
  <div class="card-content">
    <!-- Guide content here -->
  </div>
</div>
```

**⚠️ CRITICAL:** The `for` attribute in `<label>` **must match** the `id` in `<input>`. Mismatches break the toggle functionality.

#### 3. **Color-Coded Headers**

Different card types use different header colors:

```css
/* Default green for App Service */
.card-header {
  background-color: var(--appservice-color);
}

/* Blue for networking concepts */
.card-header.networking-header {
  background-color: var(--networking-color);
  border-bottom-color: #1a5276;
}

/* Red for security topics */
.card-header.security-header {
  background-color: var(--security-color);
  border-bottom-color: #7c1c22;
}

/* Purple for storage */
.card-header.storage-header {
  background-color: var(--storage-color);
  border-bottom-color: #6c3483;
}
```

**Pattern:** Use `.card-header.<domain>-header` classes for semantic color coding.

---

## 🔗 Navigation & Anchor System

### Deep Linking Strategy

All major sections have anchor IDs for direct navigation from `index.html`:

```html
<!-- In azure_app_service_guide.html -->
<div id="appservice-container-security-toggle" class="card">
  <!-- Content -->
</div>

<div id="vnet-integration" class="card">
  <!-- Content -->
</div>

<div id="deployment-slots" class="card">
  <!-- Content -->
</div>
```

### Index.html Navigation Links

```html
<!-- Links from index.html directly open specific guide sections -->
<a href="azure_app_service_guide.html#appservice-container-security-toggle">
  🔒 Container Security Pipeline
</a>

<a href="azure_app_service_guide.html#vnet-integration">
  🔐 VNet + SQL Security
</a>
```

**⚠️ Common Mistake:** Forgetting to add `id` attributes to anchor targets. Links work but don't scroll to the section.

---

## 🎯 Recent Updates (November 2025)

### App Service & Container Guides Enhancement

**Guides Updated:**

- `azure_app_service_guide.html`
- `azure_aci_container_groups_guide.html`

**New Sections Added:**

1. **Container Security** (#appservice-container-security-toggle)

   - 3-layer approach: Microsoft Defender → ACR Tasks → Azure Policy
   - Vulnerability scanning and compliance

2. **VSFDT Mnemonic** (#vnet-integration)

   - **V**Net Integration
   - **S**ervice Endpoints
   - **F**irewall Rules
   - **D**isable Public Access
   - **T**LS/SSL Enforcement

3. **Auto-Swap Deployment** (#deployment-slots)

   - Prerequisite warning: Requires staging slot creation first
   - Fail-safe benefits explanation

4. **Wildcard SSL Certificates** (#ssl-certificates)

   - `*.example.com` coverage details
   - SNI vs IP-based SSL binding
   - Limitations and use cases

5. **Traffic Manager Scaling** (#aci-scaling-traffic-manager)
   - Why Load Balancer doesn't work (VNet-bound, regional)
   - Traffic Manager routing methods: Performance, Weighted, Priority, Geographic

### Index.html Critical Priorities Section

Added visual indicators for new content:

- **Blue dot (●)** badges on NEW section title
- **Blue dots** on all 5 navigation buttons
- **Blue separator line** after NEW section

---

## 📱 Mobile & Offline Access

### iCloud Sync (Readdle Documents)

All guides auto-sync to `/Readdle/Documents/EBOOK/docs/` for offline iPad/iPhone access via Readdle Documents app.

**Sync Command (in git hooks):**

```bash
rsync -av --delete /path/to/docs/ /path/to/Readdle/iCloud/folder/
```

### Responsive Design

All guides use mobile-first CSS:

```css
/* Mobile default: Single column */
.card-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .card-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: 3 columns */
@media (min-width: 1200px) {
  .card-container {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## 🧪 JavaScript Patterns

### Auto-Expand First Card

Most guides auto-expand the first card for immediate context:

```javascript
document.addEventListener("DOMContentLoaded", () => {
  const firstToggle = document.querySelector(".card-toggle");
  if (firstToggle) {
    firstToggle.checked = true;
  }
});
```

### Hash-Based Navigation

Open specific cards via URL hash:

```javascript
window.addEventListener("DOMContentLoaded", () => {
  const hash = window.location.hash.substring(1);
  if (hash) {
    const targetCard = document.getElementById(hash);
    if (targetCard && targetCard.classList.contains("card-toggle")) {
      targetCard.checked = true;
      targetCard.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }
});
```

---

## 🐛 Known Issues & Workarounds

### 1. **CSS `max-height` Content Clipping**

**Issue:** Fixed `max-height` values cause content to be cut off in long cards.

**Affected Guides:**

- `azure_vms_deep_dive_guide.html` (Update/Fault Domains section)
- `az104_vnet_peering_cli_lab_guide.html` (CLI output sections)
- All quiz guides with 20+ questions

**Current Workaround:**

```css
.card-toggle:checked ~ .card-content {
  max-height: 3000px; /* Increased from 2500px */
  overflow-y: auto; /* Allows scrolling if still too small */
}
```

**Why This Happens:**

- CSS transitions require a numeric `max-height` value
- `max-height: auto` breaks the animation
- Content length varies wildly between guides

**Potential Solutions:**

1. Use JavaScript to calculate actual content height dynamically
2. Remove transition and use `display: none/block` (loses animation)
3. Implement a "Show More" button for very long sections

### 2. **Anchor Link Not Scrolling to Section**

**Issue:** Clicking navigation link opens guide but doesn't scroll to target section.

**Root Cause:** Missing `id` attribute on target element.

**Fix:**

```html
<!-- ❌ Wrong: No id attribute -->
<div class="card">
  <input type="checkbox" id="container-security-toggle" class="card-toggle" />
  <!-- Content -->
</div>

<!-- ✅ Correct: id on the card container -->
<div id="appservice-container-security-toggle" class="card">
  <input type="checkbox" id="container-security-toggle" class="card-toggle" />
  <!-- Content -->
</div>
```

**Verification Command:**

```bash
# Check if anchor exists in guide
grep -n 'id="target-anchor-name"' azure_app_service_guide.html
```

### 3. **Font Awesome Icons Not Loading**

**Issue:** Icons show as squares (□) instead of symbols.

**Root Cause:** CDN link missing or blocked.

**Fix:** Ensure this is in `<head>`:

```html
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
  integrity="sha512-iecdLmaskl7CVkqkXNQ/ZH/XLlvWZOJyj7Yy7tcenmpD1ypASozpmT/E0iPtmFIB46ZmdtAc9eNBvH0H/ZpiBw=="
  crossorigin="anonymous"
  referrerpolicy="no-referrer"
/>
```

### 4. **Index.html Duplicate Sections**

**Issue:** "Critical Study Priorities" appearing twice on index page.

**Root Cause:** Both static HTML and JavaScript rendering the same content.

**Fix:** Remove from `studyTopics` array if already in static HTML:

```javascript
// ❌ Remove these if already in static HTML
const studyTopics = [
  // {
  //   id: "guide-app-service-containers-critical",
  //   title: "🆕 NEW: App Service & Containers",
  //   category: "Critical Study Priorities",
  // },

  // ✅ Keep other categories
  {
    id: "guide-personalized-review",
    title: "Personalized Review",
    category: "Personalized Study Tools",
  },
  // ...
];
```

---

## 🔧 Editing Guidelines

### Adding a New Guide

1. **Copy an existing guide** with similar structure (e.g., `azure_app_service_guide.html`)
2. **Update `:root` variables** for your domain colors
3. **Add unique IDs** to all card containers for anchor linking
4. **Update `index.html`** to add navigation link:
   ```javascript
   const studyTopics = [
     // ... existing topics
     {
       id: "guide-your-new-topic",
       title: "Your New Topic",
       filename: "azure_your_new_topic_guide.html",
       category: "Azure Core & Governance",
       icon: "fas fa-icon-name",
       type: "guide",
     },
   ];
   ```
5. **Test collapsible cards** work correctly
6. **Verify anchor links** scroll to correct sections

### Updating Card Content

1. **Read current content** to understand context
2. **Locate the card** by searching for unique text or `id`
3. **Edit within `.card-content`** div (never touch `.card-toggle` or `.card-header` structure)
4. **Check `max-height`** if adding substantial content
5. **Test on mobile** (use browser dev tools responsive mode)

### CSS Variable Changes

**⚠️ WARNING:** Changing `:root` variables affects the ENTIRE guide.

**Safe to change:**

- `--appservice-color`, `--security-color`, etc. (domain-specific)
- `--diagram-bg` (visual preference)

**DO NOT change (breaks layout):**

- `--azure-blue`, `--azure-blue-dark` (Azure brand colors)
- `--text-dark`, `--text-light` (accessibility)
- `--shadow-color` (depth perception)

---

## 🚀 Deployment

### GitHub Pages

**URL:** https://mikiemapo.github.io/azure-ebook-guides/

**Auto-deploys** on push to `main` branch.

**Build time:** 1-2 minutes after push.

### Git Workflow

```bash
# Navigate to docs folder
cd "/path/to/EBOOK/docs"

# Stage changes
git add index.html azure_app_service_guide.html

# Commit with descriptive message
git commit -m "Add Container Security section to App Service guide"

# Push to GitHub (triggers auto-deployment)
git push

# Syncs to iCloud automatically via git hook
```

### Cache Busting

**Issue:** Browser shows old content after update.

**Fix:** Hard refresh

- Chrome/Firefox: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
- Safari: `Cmd + Option + R`

---

## 📊 Companion Anki Deck

**Repository:** [AZ-104-Study-Deck](https://github.com/mikiemapo/AZ-104-Critical-Priorities-Study-Deck)

**Current Status:**

- 294 flashcards across 16 batches
- 2-sentence explanation format enforced
- Synced with guide content (updated Nov 2025)

**Cross-Reference:**

- All Anki cards reference specific guide sections
- Guide sections link back to relevant card batches
- MS Learn documentation linked in README

---

## 🎓 Study Workflow

### Recommended Path

1. **Start at index.html** → Identify weak areas
2. **Critical Priorities** → Focus on Storage RTO/RPO, App Service/Containers
3. **Deep Dive Guides** → Read full context on weak topics
4. **Practice with Anki** → Reinforce with spaced repetition
5. **Hands-on Labs** → Apply knowledge with CLI exercises
6. **Quizzes** → Test understanding
7. **Scenario Sorters** → Practice decision-making

### Navigation Tips

- Use **Quick Jump menus** at top of guides for fast section access
- **Bookmark** frequently used guides in browser
- **Download for offline** via browser "Save As" → "Webpage, Complete"
- **Print to PDF** for annotation (maintains hyperlinks)

---

## 🤝 Contributing

This is a personal study repository, but suggestions welcome!

**Contact:** Create an issue in the GitHub repo

---

## 📝 License & Usage

**Personal use only.** Created for AZ-104 exam preparation.

Microsoft, Azure, and related trademarks are property of Microsoft Corporation.

---

## 🔖 Quick Reference

### Most Used Guides

- [Index Hub](https://mikiemapo.github.io/azure-ebook-guides/)
- [App Service Guide](https://mikiemapo.github.io/azure-ebook-guides/azure_app_service_guide.html)
- [Virtual Machines Deep Dive](https://mikiemapo.github.io/azure-ebook-guides/azure_vms_deep_dive_guide.html)
- [Storage RTO/RPO](https://mikiemapo.github.io/azure-ebook-guides/azure_storage_replication_rto_rpo_guide.html)
- [Personalized Review](https://mikiemapo.github.io/azure-ebook-guides/azure_personalized_review_guide.html)

### Key Files

- `index.html` - Navigation hub
- `azure_app_service_guide.html` - Recently updated (Nov 2025)
- `azure_aci_container_groups_guide.html` - Recently updated (Nov 2025)
- `azure_personalized_review_guide.html` - Weak spot tracker

---

**Last Updated:** November 22, 2025  
**Total Guides:** 86 HTML files  
**Repository Status:** Active, exam prep in progress
