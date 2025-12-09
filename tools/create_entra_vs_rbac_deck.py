#!/usr/bin/env python3
"""Generate Anki deck from Entra ID vs RBAC cheat sheet."""
import genanki

MODEL_ID = 2025120701
DECK_ID = 2025120707

model = genanki.Model(
    MODEL_ID,
    "Tutorials Dojo Cheat Sheet Model",
    fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Tags"}],
    templates=[{"name": "Card 1", "qfmt": "{{Question}}", "afmt": "{{Answer}}"}],
    css=".card { font-family: Arial, sans-serif; font-size: 18px; line-height: 1.4; color: #222; background-color: #fff; padding: 16px; }",
)

deck = genanki.Deck(DECK_ID, "AZ-104 Cheat Sheets::Entra ID vs RBAC (Tutorials Dojo)")

cards = [
    ("What is the primary focus of Microsoft Entra ID?", "An identity and access management service that helps access internal and external resources.", "comparison,entra"),
    ("What is the primary focus of Azure RBAC?", "An authorization system that manages user access to Azure resources, what they can do, and what areas they can access.", "comparison,rbac"),
    ("At what scope does Microsoft Entra ID operate?", "Tenant level.", "comparison,scope"),
    ("At what scopes can Azure RBAC be specified?", "Multiple levels: management group, subscription, resource group, and resource.", "comparison,scope"),
    ("Name three key Entra ID built-in roles.", "Global Administrator (manage all Entra resources), User Administrator (create/manage users and groups), Billing Administrator (manage subscriptions, support, purchases, service health).", "comparison,roles"),
    ("Name the four fundamental Azure RBAC built-in roles.", "Owner (full access), Contributor (create/manage all resources), Reader (view only), User Access Administrator (manage user access to all resources).", "comparison,roles"),
    ("Do Entra ID and Azure RBAC support custom roles?", "Yes, both support custom roles (RBAC custom roles in P1 and P2 licenses for Entra).", "comparison,roles"),
    ("Where can you access Entra ID role information?", "Azure Portal, Entra admin center, Microsoft 365 admin center, Microsoft Graph, Microsoft Graph PowerShell.", "comparison,access"),
    ("Where can you access Azure RBAC role information?", "Azure Portal, CLI, PowerShell, Resource Manager templates, REST API.", "comparison,access"),
    ("What is the pricing model for Microsoft Entra?", "Free, P1 (monthly charge), P2 (monthly charge).", "comparison,pricing"),
    ("Is Azure RBAC free?", "Yes, RBAC is free and included in your Azure subscription.", "comparison,pricing"),
]

for q, a, tags in cards:
    note = genanki.Note(model=model, fields=[q, a, tags])
    deck.add_note(note)

out_file = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_EntraID_vs_RBAC_TD.apkg"
if __name__ == "__main__":
    genanki.Package(deck).write_to_file(out_file)
    print(f"✅ {out_file}")
