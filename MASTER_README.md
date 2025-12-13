## AZ-104 Study Assets (Master Index)

- Purpose: single index pointing to all project READMEs and deck workflows; keep this short and link out for details.

### Key Docs (link-first, one-liners)

- [docs/README.md](docs/README.md) — HTML study guides: structure, CSS system, live site links.
- [Anki-Decks/README.md](Anki-Decks/README.md) — Anki import rules, deterministic card template, MCQ/TF format, folder policy; home of the documented questioning method.
- [Anki-Decks/generate_azure_monitor_mcq_apkg.py](Anki-Decks/generate_azure_monitor_mcq_apkg.py) — source of the **main template**: `main_front_template`, `main_back_template`, and `main_css_style` are the canonical card/layout/CSS for all MCQ decks; reuse these when adding new generators.
- [Anki-Decks/TEMPLATES_REFERENCE.md](Anki-Decks/TEMPLATES_REFERENCE.md) — snapshot of the canonical front/back HTML, CSS, fields list, and generator boilerplate for quick reuse across decks.
- [AZ-104-Critical-Priorities-Study-Deck/README.md](AZ-104-Critical-Priorities-Study-Deck/README.md) — master deck content, batch rules, CSV format, rebuild steps (deterministic; auto-randomized workflow deprecated).
- [AZ-104-Critical-Priorities-Study-Deck/TRANSCRIPT_AUTOMATION_README.md](AZ-104-Critical-Priorities-Study-Deck/TRANSCRIPT_AUTOMATION_README.md) — transcript watcher, cron setup, manual extraction workflow.
- [AZ-104-Critical-Priorities-Study-Deck/README_VMSS_STYLE_WORKFLOW.md](AZ-104-Critical-Priorities-Study-Deck/README_VMSS_STYLE_WORKFLOW.md) — deterministic VMSS-style workflow: naming pattern, scenario checklist, CSV template, rebuild steps.
- [TRANSCRIPT_PIPELINE_README.md](TRANSCRIPT_PIPELINE_README.md) — transcript-to-QA pipeline, dedupe, merge steps.
- [CLI_LABS_DECK_README.md](CLI_LABS_DECK_README.md) — CLI labs reinforcement deck rules and card caps.

### Deep Dive Decks (current)

- Outputs: `.apkg` files under `Anki-Decks/` with deterministic answer order and two-sentence explanations.
- Included topics (latest rebuild): VPN Gateway, Storage Tiers RPO/RTO, Azure Monitor Ops, App Service, Container Apps Ingress, Deep Storage Mastery, Hybrid Azure Mastery, Resilience & DR, Storage Identity Resilience, VABRF Operational Resilience, VMSS, Disaster Recovery Advanced, Azure File Security Deep Dive.
- **Question Cap: 20 per CSV file** (high quality over quantity). Example: Azure Monitor = 19q, Disaster Recovery = 19q.

Hierarchy for Deep Dive children:
- Deck path format: `AZ-104 Study Guide::Deep Dive Segments::<Topic Name> Deep Dive`
- Example: Azure File Security Deep Dive — [Anki-Decks/AZURE_FILE_SECURITY_DEEP_DIVE.apkg](Anki-Decks/AZURE_FILE_SECURITY_DEEP_DIVE.apkg) built from [AZ-104-Critical-Priorities-Study-Deck/Deep Dive Segment/Azure File Security Deep Dive.csv](AZ-104-Critical-Priorities-Study-Deck/Deep%20Dive%20Segment/Azure%20File%20Security%20Deep%20Dive.csv)
- Example: Entra ID vs AD DS Deep Dive — [Anki-Decks/ENTRA_ID_vs_AD_DS_DEEP_DIVE.apkg](Anki-Decks/ENTRA_ID_vs_AD_DS_DEEP_DIVE.apkg) built from [AZ-104-Critical-Priorities-Study-Deck/Deep Dive Segment/Entra ID vs AD DS.csv](AZ-104-Critical-Priorities-Study-Deck/Deep%20Dive%20Segment/Entra%20ID%20vs%20AD%20DS.csv)

### Work in Progress

- New transcript conversions (from `AZ-104-Critical-Priorities-Study-Deck/Text files/`) to be added iteratively; ensure non-obvious distractors and keep explanations to two sentences.
- When adding a new Deep Dive: create CSV in `Topic-Based-Decks/`, add to generator config, rebuild `.apkg`, and note the card count.

### House Rules (from linked READMEs)

- MCQ by default; True/False only for binary always/never rules.
- Explanations max two sentences; keep answers non-obvious.
- **20 questions per CSV file** — balance between depth and quality. Each question should be a high-quality Contoso-style scenario with clear learning objective.
- Import .apkg files **only** from `Anki-Decks/`; do not create new folders there.
