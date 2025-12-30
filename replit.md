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

## Stale Warning System
- 14-day threshold for marking domains as stale
- NEW badge (red): Domains never updated
- STALE badge (orange): Domains not updated in 14+ days
- Applies to both Personalized Review and main dashboard

## Single Source of Truth Pattern
- Personalized Review Guide (azure_personalized_review_guide.html) owns all score input and metadata
- Main dashboard (index.html) is read-only and displays synced data from localStorage

## Anki Deck Builder (anki-deck-builder.html)
- Fully client-side CSV to .apkg converter (no server required)
- Uses CDN-hosted libraries: PapaParse, sql.js, JSZip, CryptoJS
- Features: CSV upload, template download, data preview, card preview, answer shuffling
- MCQ card model with professional dark theme styling
- Supports column formats: Question, A/B/C/D (or ChoiceA-D), Correct, Explanation, Tags, Source, Batch

## Next Steps Tracker (Enhanced)
- **Dual Priority Display**:
  - **#1 Priority (Weakest Point)**: Shows absolute lowest scoring domain - your most critical area
  - **Next Step**: Shows 2nd lowest domain - the actionable next focus area
- **Smart Priority Logic**: 
  - Domains ranked by score ascending (lowest first)
  - If all domains >= 50%: reorders by logical AZ-104 study sequence (Identities → Storage → Compute → Networking → Monitoring)
- **Study Activity Stats**: Updates/week rate (from quiz history), days since last update, domains at 75%+
- **Exam Readiness Prediction**: 
  - Calculates estimated exam date based on study rate
  - Uses 75% threshold for all domains + 7-day consolidation buffer
  - Adapts prediction based on actual quiz-taking frequency from mergedQuizHistory
- **RAG Color-Coded Display**: Red (<50%), Amber (50-75%), Green (>75%)

## Realistic Exam Prediction (v2)
- **Rolling Window**: Uses only last 60 days of activity for rate calculation
- **Median Interval**: Uses median (not average) for robustness against irregular patterns
- **Study Status Detection**:
  - Active: Quizzed within 7 days
  - Cooling: 8-14 days since last quiz
  - Slump/Paused: >14 days or >1.5x typical gap
  - Inactive: No quiz history
- **Stale Domain Tracking**: Flags domains not updated in 14+ days
- **Adaptive Prediction**:
  - If in slump: Shows warning + encourages resuming study (date faded/unreliable)
  - If active: Shows realistic date based on per-domain gap to 75% + typical pace
  - Adds catch-up time for stale domains
  - Points per session scaled by quiz frequency (5-8 points based on pace)
- **Status Badges**: Visual indicator (Active/Cooling/Paused/Inactive) in stats section

## Stale Warning System
- 14-day threshold for marking domains as stale
- NEW badge (red): Domains never updated
- STALE badge (orange): Domains not updated in 14+ days
- Applies to both Personalized Review and main dashboard

## Single Source of Truth Pattern
- Personalized Review Guide (azure_personalized_review_guide.html) owns all score input and metadata
- Main dashboard (index.html) is read-only and displays synced data from localStorage
