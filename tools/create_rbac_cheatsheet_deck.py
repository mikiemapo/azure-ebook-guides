#!/usr/bin/env python3
"""
Generate an Anki deck from the Azure RBAC Cheat Sheet (Tutorials Dojo).
This is a hand-curated flashcard set distilled from the cheat sheet content.
"""
import genanki

MODEL_ID = 2025120701
DECK_ID = 2025120702

model = genanki.Model(
    MODEL_ID,
    "Tutorials Dojo RBAC Model",
    fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Tags"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": "{{Answer}}",
        },
    ],
    css="""
.card {
    font-family: Arial, sans-serif;
    font-size: 18px;
    line-height: 1.4;
    color: #222;
    background-color: #fff;
    padding: 16px;
}
    """,
)

deck = genanki.Deck(DECK_ID, "AZ-104 Cheat Sheets::Azure RBAC (Tutorials Dojo)")

cards = [
    (
        "What is Azure Role-Based Access Control (RBAC) used for?",
        "An Azure Resource Manager authorization system that manages who can access Azure resources, what they can do, and which scopes they can access (fine-grained access management).",
        "rbac,concepts",
    ),
    (
        "Name the three parts of a role assignment (RBAC).",
        "Security principal (user/group/service principal/managed identity), role definition (permissions), and scope (where the permissions apply).",
        "rbac,concepts",
    ),
    (
        "What is a role assignment?",
        "Attaching a role definition to a security principal at a given scope to grant access. RBAC is additive; you can have multiple role assignments.",
        "rbac,concepts",
    ),
    (
        "Does Azure RBAC support deny assignments?",
        "Yes. Azure RBAC supports both allow and deny assignments.",
        "rbac,concepts",
    ),
    (
        "Classic subscription admin roles: how many Account Administrators per account and what can they do?",
        "One Account Administrator per Azure account; billing owner—can create/cancel subscriptions and manage billing/subscriptions.",
        "rbac,classic",
    ),
    (
        "Classic subscription admin roles: Service Administrator—how many and what access?",
        "One Service Administrator per subscription; full access to the Azure portal for that subscription and can assign Co-Administrators. Often the Account Administrator is also the Service Administrator for new subscriptions.",
        "rbac,classic",
    ),
    (
        "Classic subscription admin roles: Co-Administrator limits and privilege nuance?",
        "Up to 200 Co-Administrators per subscription; same privileges as Service Administrator except cannot change the directory association of the subscription.",
        "rbac,classic",
    ),
    (
        "List the four fundamental built-in Azure RBAC roles and their key capabilities.",
        "Owner: full access + delegate; Contributor: create/manage resources but cannot grant access; Reader: view only; User Access Administrator: manage access to resources.",
        "rbac,builtin",
    ),
    (
        "Which RBAC built-in role can grant access to others?",
        "Owner can delegate; User Access Administrator can manage access. Contributor cannot grant access.",
        "rbac,builtin",
    ),
    (
        "What can a Contributor do and not do?",
        "Can create and manage all resource types; cannot grant access to others.",
        "rbac,builtin",
    ),
    (
        "What is a User Access Administrator allowed to do?",
        "Manage access (role assignments) to all resource types, without having full data-plane permissions on those resources.",
        "rbac,builtin",
    ),
    (
        "What is the relationship between Microsoft Entra roles and Azure RBAC roles?",
        "Entra roles manage Entra (AAD) resources (users, groups, domains, licenses); Azure RBAC roles manage Azure resources. They are separate scopes.",
        "rbac,entra",
    ),
]

for q, a, tags in cards:
    note = genanki.Note(model=model, fields=[q, a, tags])
    deck.add_note(note)

out_file = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_RBAC_CheatSheet_TD.apkg"
if __name__ == "__main__":
    genanki.Package(deck).write_to_file(out_file)
    print(f"✅ Wrote deck: {out_file}")
