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
- `server.py` - Simple Python HTTP server for development

## Running the Project
The project runs a Python HTTP server that serves the `docs/` directory on port 5000:
```bash
python server.py
```

## Deployment
Configured as a static site deployment serving the `docs/` directory.

## Key Features
- Interactive collapsible cards with CSS animations
- Color-coded sections using CSS custom properties
- Responsive mobile-first design
- Font Awesome icons
- Anchor navigation for deep-linking
- Quiz integration with instant feedback
- Local Anki Deck Builder (anki-deck-builder.html) for CSV to .apkg conversion
- Anki Deck Library (anki-deck-library.html) with 11 pre-built AZ-104 decks

## Architecture Notes
- Pure static HTML/CSS/JS - no build step required
- Uses CDN-hosted Font Awesome for icons
- Cache-Control headers disabled for development

## Data Contracts (localStorage)
- **mergedQuizScores**: Domain scores with capitalized keys (Identities, Storage, Compute, Networking, Monitoring, App Service & Containers) containing {correct, total}
- **domainScoreMetadata**: Per-domain metadata with {lastUpdated, source, quizName}
- **mergedQuizHistory**: v2 versioned snapshots with {version, takenAt, source, merged, summary}
- **sourceRotationData**: Per-domain tracking of lastStudy/lastTest sources and dates

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

### Source Rotation Tracker
Prevents memorizing answers by tracking which source you last used:
- **Per-domain tracking**: Shows "Last Study" and "Last Test" source for each domain
- **Smart suggestions**: Recommends which source to use next based on rotation rule
- **Quick Log Session**: One-click logging of study/test activity per domain
- **Rotation Rule**: Study with Whizlabs → Test with Tutorials Dojo (or vice versa)
- **localStorage key**: `sourceRotationData`

### Weak Point Extractor
Converts quiz review PDFs into NotebookLM-ready Focus Briefs:
- **Paste Box**: Copy wrong answers from quiz review and paste
- **Concept Parser**: Extracts Azure keywords and concepts automatically
- **Focus Brief Generator**: Creates structured prompt for NotebookLM critique audio
- **Copy Button**: One-click copy to clipboard for pasting into NotebookLM
- **Supported formats**: Q:/Your Answer:/Correct:/Explanation: prefixes

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
