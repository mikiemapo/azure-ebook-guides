# AZ-104 Study Hub

## Overview
This is a static HTML website containing 86+ interactive study guides for the Microsoft Azure Administrator (AZ-104) certification exam. The guides include collapsible cards, quizzes, flashcards, CLI labs, and scenario sorters.

## Project Structure
- `docs/` - Main content directory containing all HTML study guides
  - `index.html` - Main study hub navigation page
  - `*.html` - Individual topic guides (Azure VMs, Storage, Networking, etc.)
- `Anki-Decks/` - Anki flashcard decks (.apkg files)
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
- External tool links (e.g., Anki Deck Builder) with support for `externalUrl` in studyTopics

## Architecture Notes
- Pure static HTML/CSS/JS - no build step required
- Uses CDN-hosted Font Awesome for icons
- Cache-Control headers disabled for development
