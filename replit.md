# AZ-104 Study Hub

## Overview
This is a static HTML website containing 86+ interactive study guides for the Microsoft Azure Administrator (AZ-104) certification exam. The guides include collapsible cards, quizzes, flashcards, CLI labs, and scenario sorters.

## Project Structure
- `docs/` - Main content directory containing all HTML study guides
  - `index.html` - Main study hub navigation page
  - `*.html` - Individual topic guides (Azure VMs, Storage, Networking, etc.)
  - `Anki-Decks/` - Anki flashcard decks (.apkg files, served by the web server)
- `tools/` - Python scripts for deck generation
- `reports/` - Analysis and tracking reports
- `server.py` - Flask server with API endpoints and static file serving
- `cloudflare-worker/` - Serverless API for GitHub Pages deployment
  - `worker.js` - Cloudflare Worker with /api/extract-concepts and /api/generate-cprs
  - `wrangler.toml` - Worker configuration
- `DEPLOYMENT.md` - Step-by-step GitHub Pages deployment guide

## Running the Project
The project runs a Flask server that serves the `docs/` directory on port 5000 and provides API endpoints:
```bash
python server.py
```

## API Endpoints
- `GET /` - Serves index.html
- `GET /<path>` - Serves static files from docs/
- `POST /api/extract-concepts` - AI-powered concept extraction for Weak Point Extractor
  - Input: `{"text": "quiz review content"}`
  - Output: Concepts with Azure facts, study guide references, and NotebookLM summary
  - Requires: `OPENAI_API_KEY` environment secret
- `POST /api/generate-cprs` - Generate 6 MCQ questions using CPRS methodology
  - Input: `{"concept": "Azure concept name"}`
  - Output: 6 exam-style MCQs (Foundation, Definition, Differentiation, Scenario, Anti-Confusion, Compression)
  - Uses KV caching to reduce OpenAI API costs
- `POST /api/user` - Create new sync user ID
  - Output: `{"userId": "user_[uuid]"}`
- `GET /api/sync?userId=...` - Get synced quiz scores from cloud
- `PUT /api/sync` - Push quiz scores to cloud
  - Input: `{"userId": "user_...", "data": {...}}`
- `GET /api/anki-decks` - List available Anki decks from R2 storage
- `GET /api/anki-decks/:name` - Download specific Anki deck from R2

## Environment Secrets
- `OPENAI_API_KEY` - OpenAI API key for AI-powered concept extraction (optional - fallback mode works without it)

## Cloudflare Services (Production)
- **KV Namespace (CPRS_CACHE)**: Caches CPRS responses for 30 days, reduces OpenAI costs by 50%+
- **D1 Database (az104-study-db)**: Stores user sync data for cross-device score synchronization
- **R2 Bucket (az104-anki-decks)**: Stores pre-built Anki .apkg files with zero egress fees
- See `cloudflare-worker/CLOUDFLARE_SETUP.md` for setup instructions

## Deployment
Two deployment options available:

### Local Development (Replit)
- Flask server on port 5000 serves static files and API endpoints
- `api-config.js` has empty `baseUrl` to use local server

### GitHub Pages + Cloudflare Workers (Production)
- See `DEPLOYMENT.md` for complete setup instructions
- Static files deployed to GitHub Pages (free)
- API endpoints on Cloudflare Workers (free, 100K req/day)
- Update `docs/api-config.js` with Worker URL for production

## Key Features
- Interactive collapsible cards with CSS animations
- Color-coded sections using CSS custom properties
- Responsive mobile-first design
- Font Awesome icons
- Anchor navigation for deep-linking
- Quiz integration with instant feedback
- Local Anki Deck Builder (anki-deck-builder.html) for CSV to .apkg conversion
- Anki Deck Library (anki-deck-library.html) - CPRS workflow-based deck building
- **Persistent Navigation Bar** with search (shared-navbar.js) across all 88 pages
  - Personalized search suggestions based on weak domains from localStorage
  - On focus: Shows guides for your 2 weakest domains with score percentages
  - Guides tagged by domain for targeted recommendations

## Architecture Notes
- Pure static HTML/CSS/JS - no build step required
- Uses CDN-hosted Font Awesome for icons
- Cache-Control headers disabled for development
- **shared-navbar.js**: Dynamically injects persistent navbar with search on all pages
  - Sticky positioning at top of viewport
  - Search functionality for quick guide navigation
  - Quick links to Review, Builder, Library tools
  - Mobile responsive (icons-only on small screens)

## Data Contracts (localStorage)
- **mergedQuizScores**: Domain scores with capitalized keys (Identities, Storage, Compute, Networking, Monitoring, App Service & Containers) containing {correct, total}
- **domainScoreMetadata**: Per-domain metadata with {lastUpdated, source, quizName}
- **mergedQuizHistory**: v2 versioned snapshots with {version, takenAt, source, merged, summary}
- **sourceRotationData**: Per-domain tracking of lastStudy/lastTest sources and dates
- **az104SyncUserId**: Cloud sync user ID (format: `user_[UUID]`) for cross-device synchronization
- **studyWorkflowChecklist**: Array of completed step IDs [1-11] for the Study Workflow Loop

## Single Source of Truth Pattern
- Personalized Review Guide (azure_personalized_review_guide.html) owns all score input and metadata
- Main dashboard (index.html) is read-only and displays synced data from localStorage

## Anki Deck Builder (anki-deck-builder.html)
- Fully client-side CSV to .apkg converter (no server required)
- Uses CDN-hosted libraries: PapaParse, sql.js, JSZip, CryptoJS
- Features: CSV upload, template download, data preview, card preview, answer shuffling
- MCQ card model with professional dark theme styling
- Supports column formats: Question, A/B/C/D (or ChoiceA-D), Correct, Explanation, Tags, Source, Batch

---

## Study Workflow Loop Support

### Study Workflow Loop Checklist
Interactive checklist for the 11-step study workflow (based on Canva master document):
- **Personalized Review**: Full checklist with checkboxes, "Edit in Canva" button, reset button
- **Main Hub**: Summary view showing only remaining (unchecked) items
- **Steps tracked**: NotebookLM → Dual Quiz → Weak Point Extraction → Critique Audio → Anki MCQ → Rotate → Repeat
- **localStorage key**: `studyWorkflowChecklist` (array of completed step IDs)
- **Cross-tab sync**: Updates reflected via storage event listener
- **Canva link**: https://www.canva.com/design/DAG9I5NXsAc/

### Collapsible Domain Cards (Main Hub)
- Domain cards default to collapsed state (name + % + progress bar only)
- Click to expand for full details (quiz score, last updated, action buttons)
- Reduces scrolling on main dashboard significantly

### Source Rotation Tracker
Prevents memorizing answers by tracking which source you last used:
- **Per-domain tracking**: Shows "Last Study" and "Last Test" source for each domain
- **Smart suggestions**: Recommends which source to use next based on rotation rule
- **Quick Log Session**: One-click logging of study/test activity per domain
- **Rotation Rule**: Study with Whizlabs → Test with Tutorials Dojo (or vice versa)
- **localStorage key**: `sourceRotationData`

### Weak Point Extractor
Converts quiz review PDFs into NotebookLM-ready Focus Briefs with two modes:
- **Quick Extract**: Client-side keyword extraction (instant, no API needed)
- **AI Extract**: Server-side OpenAI analysis using CPRS methodology
- **CPRS Output Fields**:
  - Foundation: What problem does this concept solve?
  - Definition: Precise one-sentence definition
  - Differentiation: How it differs from similar services
  - Fact: The accurate Azure fact
  - Why Wrong: Explanation of the misconception
  - Memory Hook: One-sentence compression for recall
  - Objective: AZ-104 exam objective code
- **Fallback mode**: Works without OpenAI API credits
- **Supported formats**: Q:/Your Answer:/Correct:/Explanation: prefixes

### CPRS Question Generator
Generates 6 separate MCQ questions using the CPRS (Concept-Pathway Reinforcement System) methodology:
- **Input**: Any Azure concept (e.g., "VNet Peering", "Azure Policy")
- **Output**: 6 exam-style MCQs (A/B/C/D format), each testing a different mastery angle:
  1. **Foundation MCQ**: Tests understanding of what problem the concept solves
  2. **Definition MCQ**: Tests knowing the precise definition
  3. **Differentiation MCQ**: Tests distinguishing from similar Azure services
  4. **Scenario MCQ**: Realistic exam-style application question with misdirection
  5. **Anti-Confusion MCQ**: Tests recognizing why wrong answers are wrong (e.g., "Which is FALSE?")
  6. **Compression MCQ**: Tests the memory hook/key takeaway
- **Copy for Anki**: Exports all 6 MCQs as CSV rows with tags (objective code + question type)
- **API endpoint**: `POST /api/generate-cprs`

### AZ-104 Exam Objectives Reference
Official Microsoft exam objectives mapped to study domains:
- **1.x (15-20%)**: Manage Azure Identities and Governance → Identities domain
- **2.x (15-20%)**: Implement and Manage Storage → Storage domain
- **3.x (20-25%)**: Deploy and Manage Compute Resources → Compute + App Service domains
- **4.x (20-25%)**: Implement and Manage Virtual Networking → Networking domain
- **5.x (10-15%)**: Monitor and Maintain Azure Resources → Monitoring domain
- Use objective codes (e.g., `1.2`, `3.3`) for Anki card tagging

---

## Study Activity Tracking System

### Next Steps Tracker
- **Dual Priority Display**:
  - **#1 Priority (Weakest Point)**: Shows absolute lowest scoring domain - your most critical area
  - **Next Step**: Shows 2nd lowest domain - the actionable next focus area
- **Smart Priority Logic**: 
  - Domains ranked by score ascending (lowest first)
  - If all domains >= 50%: reorders by logical AZ-104 study sequence (Identities → Storage → Compute → Networking → Monitoring)
- **RAG Color-Coded Display**: Red (<50%), Amber (50-75%), Green (>75%)

### Study Activity Stats
- **Quizzes/Week (60d)**: Rolling 60-day window calculation of study frequency
- **Days Since Quiz**: How many days since last Score Editor save
- **Domains at 75%+**: Count of exam-ready domains
- **Refresh Button**: Click to reload and see updated stats
- **Status Badges**: Active (within 7 days), Cooling (8-14 days), Paused (14+ days), Inactive (no data)

### Day Consolidation System
Prevents inflated statistics from multiple Score Editor saves:
- **Multiple saves on same day → count as 1 day** of study activity
- Example: Save 10 times today → only counts as 1 day for rate calculation
- Ensures "Quizzes/Week" reflects actual study days, not save clicks
- Requires 2+ different days of activity to calculate a rate

### Stale Warning System
- 14-day threshold for marking domains as stale
- **NEW badge (red)**: Domains never updated
- **STALE badge (orange)**: Domains not updated in 14+ days
- Applies to both Personalized Review and main dashboard

---

## Dynamic Exam Readiness Prediction

### How It Works
- Uses your **actual study pace** from the rolling 60-day window
- Estimates points improvement per session based on your frequency
- Projects when all 6 domains will reach 75%+ threshold
- Adds 7-day consolidation buffer for knowledge retention

### Study Status Detection
| Status | Condition | Prediction |
|--------|-----------|------------|
| Active | Studied within 7 days | Shows projected date |
| Cooling | 8-14 days since last study | Shows date with caution |
| Paused | 14+ days gap | "Prediction unavailable" |
| Inactive | No quiz history | "Not enough data" |

### Adaptive Prediction Logic
- **If in slump**: Shows warning + encourages resuming study
- **If active**: Shows realistic date based on your pace
- **Pace scaling**: Points per session adjusted by study frequency (5-8 points)
- **Stale domain penalty**: Adds catch-up time for neglected domains

### Dynamic Adjustment
The prediction updates every time you save scores:
| Your Action | Effect on Prediction |
|-------------|---------------------|
| Study more frequently | Date moves closer |
| Study less frequently | Date moves further |
| Improve domain scores | Date moves closer |
| Stop studying (14+ days) | Shows "Prediction unavailable" |

---

## Retention Trends

### Day-Consolidated Sparklines
- Shows your progress over time per domain
- **Uses LAST entry per day only** - prevents artificial spikes
- Add/subtract corrections within same day → only final score shows
- Clean visualization of actual day-over-day progress

### Trend Indicators
- **▲ Delta**: Score improvement from first to last data point
- **Sparkline**: Visual trend line showing progress trajectory
- Moving average calculation for smoothed insights

---

## Score Editor Behavior

### What Updates When You Save
| Component | Updates? | Notes |
|-----------|----------|-------|
| Domain Scores | ✅ | Immediately reflected |
| Days Since Quiz | ✅ | Resets to 0 (today) |
| Study Status | ✅ | Shows "Active" |
| Quizzes/Week | ✅ | After 2+ different days |
| Retention Trends | ✅ | Last score of the day only |
| Metadata | ✅ | lastUpdated timestamp |

### Consolidation Examples
- Save 6 times today → 1 consolidated day
- Save on Monday + Friday → 2 days → rate can be calculated
- Multiple add/subtract cycles → only final score per day in trends
