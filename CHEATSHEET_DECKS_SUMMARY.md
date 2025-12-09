# AZ-104 Tutorial Dojo Cheat Sheet Anki Decks

## Summary

Successfully created **6 comprehensive Anki flashcard decks** from Tutorial Dojo cheat sheets for AZ-104 exam preparation.

## Decks Generated

| Deck                            | File                                  | Cards | Topics                                                                                   |
| ------------------------------- | ------------------------------------- | ----- | ---------------------------------------------------------------------------------------- |
| **Azure RBAC**                  | `AZ104_RBAC_CheatSheet_TD.apkg`       | 12    | RBAC concepts, role assignments, classic/fundamental roles, delegation                   |
| **Azure Global Infrastructure** | `AZ104_Global_Infrastructure_TD.apkg` | 10    | Regions, Availability Zones, paired regions, bandwidth, disaster recovery                |
| **Azure Policy**                | `AZ104_Policy_TD.apkg`                | 10    | Policy effects, compliance, evaluation order, RBAC distinction                           |
| **Azure App Service**           | `AZ104_AppService_TD.apkg`            | 10    | PaaS platform, service types, pricing tiers, runtimes, auto-scaling                      |
| **Microsoft Entra ID**          | `AZ104_EntraID_TD.apkg`               | 16    | Licensing, authentication, B2B/B2C, conditional access, identity governance, workload ID |
| **Entra ID vs RBAC**            | `AZ104_EntraID_vs_RBAC_TD.apkg`       | 11    | Scope, focus, roles, pricing—direct comparison                                           |

**Total: 69 flashcards across 6 decks**

## Location

All `.apkg` files are in: `/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/`

## How to Use

1. Open Anki
2. Click **File → Import**
3. Select each `.apkg` file to import into your collection
4. Cards will appear with tags for easy filtering and review

## Card Format

- **Question side:** Clear, exam-focused questions
- **Answer side:** Concise, concept-focused answers
- **Tags:** Topic-based tags for filtering and review scheduling
- **Styling:** Clean, green-accented design for readability

## Script Reference

All deck generation scripts are in `/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/tools/`:

- `create_rbac_cheatsheet_deck.py`
- `create_global_infra_deck.py`
- `create_policy_deck.py`
- `create_appservice_deck.py`
- `create_entraid_deck.py`
- `create_entra_vs_rbac_deck.py`

Each script can be re-run independently to regenerate the `.apkg` file.

---

**Generated:** December 7, 2024
**Source:** Tutorial Dojo cheat sheets (PNG-to-PDF conversions)
