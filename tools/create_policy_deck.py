#!/usr/bin/env python3
"""Generate Anki deck from Azure Policy cheat sheet."""
import genanki

MODEL_ID = 2025120701
DECK_ID = 2025120704

model = genanki.Model(
    MODEL_ID,
    "Tutorials Dojo Cheat Sheet Model",
    fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Tags"}],
    templates=[{"name": "Card 1", "qfmt": "{{Question}}", "afmt": "{{Answer}}"}],
    css=".card { font-family: Arial, sans-serif; font-size: 18px; line-height: 1.4; color: #222; background-color: #fff; padding: 16px; }",
)

deck = genanki.Deck(DECK_ID, "AZ-104 Cheat Sheets::Azure Policy (Tutorials Dojo)")

cards = [
    ("What is Azure Policy used for?", "Ensure resources are compliant with a set of rules; manage policies in centralized location; assess compliance across organization.", "policy,concepts"),
    ("How does Policy differ from RBAC?", "Policy maintains compliance with resource state; RBAC controls user actions. Even if user has access, policy can block non-compliant resources.", "policy,concepts"),
    ("In what format are policies created?", "JSON format.", "policy,concepts"),
    ("What is the order of policy evaluation?", "Disabled, Append/Modify, Deny, Audit.", "policy,evaluation"),
    ("List Azure Policy effects (6 main).", "Append (add fields), Audit (warning for non-compliant), AuditIfNotExists (audit if condition met), Deny (prevent request), DeployIfNotExists (execute template if condition), Disabled (disable assignment), Modify (manage tags).", "policy,effects"),
    ("What is the Append effect in Azure Policy?", "Adds additional fields to requested resource.", "policy,effects"),
    ("What is the Deny effect in Azure Policy?", "Prevents the request before being sent to Resource Provider.", "policy,effects"),
    ("What is the DeployIfNotExists effect in Azure Policy?", "If the condition is met, allows you to execute a template deployment.", "policy,effects"),
    ("What is the Modify effect in Azure Policy?", "Manages tags of resources.", "policy,effects"),
    ("What determines how policy is applied to resources?", "Policy assignments determine assigned resources.", "policy,assignment"),
]

for q, a, tags in cards:
    note = genanki.Note(model=model, fields=[q, a, tags])
    deck.add_note(note)

out_file = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_Policy_TD.apkg"
if __name__ == "__main__":
    genanki.Package(deck).write_to_file(out_file)
    print(f"✅ {out_file}")
