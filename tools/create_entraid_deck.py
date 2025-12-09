#!/usr/bin/env python3
"""Generate Anki deck from Microsoft Entra ID cheat sheet."""
import genanki

MODEL_ID = 2025120701
DECK_ID = 2025120706

model = genanki.Model(
    MODEL_ID,
    "Tutorials Dojo Cheat Sheet Model",
    fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Tags"}],
    templates=[{"name": "Card 1", "qfmt": "{{Question}}", "afmt": "{{Answer}}"}],
    css=".card { font-family: Arial, sans-serif; font-size: 18px; line-height: 1.4; color: #222; background-color: #fff; padding: 16px; }",
)

deck = genanki.Deck(DECK_ID, "AZ-104 Cheat Sheets::Microsoft Entra ID (Tutorials Dojo)")

cards = [
    ("What is Microsoft Entra ID?", "An identity and access management service helping you access internal and external resources.", "entra,concepts"),
    ("List Microsoft Entra licenses.", "Free, Premium P1, Premium P2, Pay-as-you-go (B2C).", "entra,licensing"),
    ("What features does Entra Free license provide?", "User and group management in on-premises directory.", "entra,licensing"),
    ("What does Entra Premium P1 provide?", "Access to both on-premises and cloud resources.", "entra,licensing"),
    ("What extra feature does Entra Premium P2 provide?", "Microsoft Entra Identity Protection in addition to P1 features.", "entra,licensing"),
    ("What does Entra Pay-as-you-go license provide?", "Azure AD B2C feature.", "entra,licensing"),
    ("Name Entra authentication features.", "Self-service password reset, MFA, custom banned password list, smart lockout.", "entra,auth"),
    ("What is Azure AD B2B?", "Managing external identities for business-to-business scenarios.", "entra,b2b"),
    ("What is Azure AD B2C?", "Business-to-customer identity service allowing control over user sign-up, sign-in, and profile management.", "entra,b2c"),
    ("What is Conditional Access in Entra?", "Manage access to cloud apps based on conditions.", "entra,conditional"),
    ("What does Microsoft Entra admin center do?", "Allows managing and configuring device identities.", "entra,device"),
    ("What is Microsoft Entra Domain Services?", "Manage domain services like domain join, group policy, and authentication.", "entra,domain"),
    ("What is Identity Governance?", "Ensures only authorized people have right access to specific resources.", "entra,governance"),
    ("What does Entra support for hybrid identity?", "Supports hybrid identity to access resources in cloud or on-premises.", "entra,hybrid"),
    ("What is Microsoft Entra Permissions Management?", "Cloud Infrastructure entitlement management (CIEM) for comprehensive visibility/control over permissions for any identity or resource across Azure, AWS, GCP.", "entra,permissions"),
    ("What is Microsoft Entra Workload ID?", "Workload identity assigned to software workloads (apps, APIs, scripts, containers) for authentication and accessing services/resources.", "entra,workload"),
]

for q, a, tags in cards:
    note = genanki.Note(model=model, fields=[q, a, tags])
    deck.add_note(note)

out_file = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_EntraID_TD.apkg"
if __name__ == "__main__":
    genanki.Package(deck).write_to_file(out_file)
    print(f"✅ {out_file}")
