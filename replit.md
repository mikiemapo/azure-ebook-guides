# AZ-104 Study Hub

## Overview
This project is a static HTML website offering 86+ interactive study guides for the Microsoft Azure Administrator (AZ-104) certification exam. Its primary purpose is to provide a comprehensive, engaging, and personalized learning experience to help users prepare for and pass the AZ-104 exam. Key capabilities include interactive study cards, quizzes with instant feedback, flashcards, CLI labs, scenario sorters, and AI-powered study tools. The project aims to consolidate all necessary study materials into a single, accessible hub, leveraging a "Single Source of Truth Pattern" for consistent data management. The long-term vision is to become the go-to resource for AZ-104 preparation by offering adaptive learning paths, real-time progress tracking, and smart recommendations.

## User Preferences
I want to interact with the AI using clear, concise language. I prefer iterative development, with explanations provided for major changes or new features. Please ask before making significant architectural decisions or adding new external dependencies. I value transparency in how AI-powered features utilize data and APIs.

## System Architecture
The application is structured as a pure static HTML/CSS/JS website, requiring no build step, ensuring lightweight and fast deployment.

**UI/UX Decisions:**
- **Interactive Collapsible Cards:** Utilizes CSS animations for an engaging user experience.
- **Color-Coded Sections:** Employs CSS custom properties for thematic organization.
- **Responsive Design:** Mobile-first approach for accessibility across devices.
- **Persistent Navigation Bar:** A dynamically injected `shared-navbar.js` provides consistent navigation, search functionality, and quick links across all pages. It also offers personalized search suggestions based on user's weak domains.
- **RAG Color-Coding:** Red, Amber, Green system for displaying progress and priority.

**Technical Implementations & Feature Specifications:**
- **Study Guides:** HTML files with embedded interactive elements like quizzes and flashcards.
- **Quiz Integration:** Provides instant feedback and tracks scores locally.
- **Anki Deck Builder:** A client-side tool (anki-deck-builder.html) for converting CSV data into Anki flashcard decks (`.apkg` files). Supports various column formats and MCQ card models with professional dark theme styling.
- **Personalized Review Guide:** Acts as the "single source of truth" for all score inputs and metadata, driving personalized recommendations.
- **Study Workflow Loop Checklist:** An interactive 11-step checklist to guide users through a structured study process (e.g., NotebookLM, Dual Quiz, Weak Point Extraction, Anki MCQ).
- **Source Rotation Tracker:** Per-domain tracking of study and test sources to prevent rote memorization and suggest optimal study methods.
- **Weak Point Extractor:** Converts quiz review content into "Focus Briefs" for NotebookLM. It supports both client-side keyword extraction (Quick Extract) and AI-powered extraction (AI Extract) for more detailed analysis, including CPRS (Concept-Pathway Reinforcement System) output fields.
- **CPRS Question Generator:** Generates six types of exam-style Multiple Choice Questions (MCQs) for any given Azure concept, covering Foundation, Definition, Differentiation, Scenario, Anti-Confusion, and Compression aspects.
- **Study Activity Tracking System:**
    - **Next Steps Tracker:** Dynamically identifies the weakest and second weakest domains, providing prioritized study recommendations.
    - **Study Activity Stats:** Tracks quizzes per week, days since last quiz, and the number of exam-ready domains.
    - **Day Consolidation System:** Ensures accurate study frequency by counting multiple saves on the same day as a single day of activity.
    - **Stale Warning System:** Highlights domains not updated within 14 days.
- **Dynamic Exam Readiness Prediction:** Estimates the completion date for reaching 75%+ in all domains based on the user's study pace, adapting dynamically with new score inputs.
- **Retention Trends:** Visualizes progress using day-consolidated sparklines and trend indicators (e.g., score delta).

**System Design Choices:**
- **Local Storage:** Used for `mergedQuizScores`, `domainScoreMetadata`, `mergedQuizHistory`, `sourceRotationData`, `az104SyncUserId`, and `studyWorkflowChecklist` to persist user data and enable offline functionality.
- **API Endpoints (Flask Server/Cloudflare Worker):**
    - `GET /`, `GET /<path>`: Static file serving.
    - `POST /api/extract-concepts`: AI-powered concept extraction.
    - `POST /api/generate-cprs`: Generates CPRS-based MCQs.
    - `POST /api/user`, `GET /api/sync`, `PUT /api/sync`: User synchronization and quiz score management.
    - `GET /api/anki-decks`, `GET /api/anki-decks/:name`: Anki deck management.
    - `GET /api/objectives`: Provides official AZ-104 exam objectives.

## External Dependencies
- **OpenAI API:** Utilized for AI-powered features such as concept extraction (`/api/extract-concepts`) and CPRS question generation (`/api/generate-cprs`). Requires `OPENAI_API_KEY`.
- **Cloudflare KV Namespace (CPRS_CACHE):** Caches CPRS responses to reduce OpenAI API costs.
- **Cloudflare D1 Database (az104-study-db):** Stores user sync data for cross-device score synchronization.
- **Cloudflare R2 Bucket (az104-anki-decks):** Hosts pre-built Anki `.apkg` files with zero egress fees.
- **Font Awesome:** CDN-hosted for icons.
- **Client-side Libraries for Anki Deck Builder:** PapaParse, sql.js, JSZip, CryptoJS for in-browser CSV processing and Anki deck generation.