#!/usr/bin/env python3
"""Generate Anki deck from Azure App Service cheat sheet."""
import genanki

MODEL_ID = 2025120701
DECK_ID = 2025120705

model = genanki.Model(
    MODEL_ID,
    "Tutorials Dojo Cheat Sheet Model",
    fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Tags"}],
    templates=[{"name": "Card 1", "qfmt": "{{Question}}", "afmt": "{{Answer}}"}],
    css=".card { font-family: Arial, sans-serif; font-size: 18px; line-height: 1.4; color: #222; background-color: #fff; padding: 16px; }",
)

deck = genanki.Deck(DECK_ID, "AZ-104 Cheat Sheets::Azure App Service (Tutorials Dojo)")

cards = [
    ("What is Azure App Service?", "A fully managed PaaS platform for building, deploying, and scaling web apps. Automatically patches and maintains OS and language frameworks.", "appservice,concepts"),
    ("List the main types of App Service.", "Web Apps, Web Apps for Containers, API Apps.", "appservice,types"),
    ("What languages does App Service support?", ".NET, .NET Core, Java, Ruby, Node.js, PHP, Python, and Ubuntu-powered runtimes.", "appservice,runtimes"),
    ("What is an App Service plan?", "A collection of compute resources needed for web app to run, consisting of region, number/size of VMs, and pricing tier.", "appservice,plan"),
    ("Name the three pricing tiers for App Service.", "Shared Compute (Free/Shared—no scale-out), Dedicated (Basic/Standard/Premium/PremiumV2—scale-out), Isolated (dedicated VM—max scale-out).", "appservice,pricing"),
    ("What is Shared Compute tier?", "Free and Shared tiers allocate CPU quotas per app on shared resources; cannot scale-out.", "appservice,pricing"),
    ("What is Dedicated Compute tier?", "Basic, Standard, Premium, PremiumV2 tiers; higher tiers have more VMs for scale-out.", "appservice,pricing"),
    ("What is Isolated tier?", "Dedicated virtual machine providing maximum scale-out capabilities.", "appservice,pricing"),
    ("What is Web Apps for Containers?", "Deploy and run containerized applications in Azure.", "appservice,containers"),
    ("Does App Service support auto-scaling?", "Yes, auto-scaling and load balancing for resilience and high availability.", "appservice,scaling"),
]

for q, a, tags in cards:
    note = genanki.Note(model=model, fields=[q, a, tags])
    deck.add_note(note)

out_file = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_AppService_TD.apkg"
if __name__ == "__main__":
    genanki.Package(deck).write_to_file(out_file)
    print(f"✅ {out_file}")
