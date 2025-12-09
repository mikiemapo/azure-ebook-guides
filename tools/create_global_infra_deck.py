#!/usr/bin/env python3
"""Generate Anki deck from Azure Global Infrastructure cheat sheet."""
import genanki

MODEL_ID = 2025120701
DECK_ID = 2025120703

model = genanki.Model(
    MODEL_ID,
    "Tutorials Dojo Cheat Sheet Model",
    fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Tags"}],
    templates=[{"name": "Card 1", "qfmt": "{{Question}}", "afmt": "{{Answer}}"}],
    css=".card { font-family: Arial, sans-serif; font-size: 18px; line-height: 1.4; color: #222; background-color: #fff; padding: 16px; }",
)

deck = genanki.Deck(DECK_ID, "AZ-104 Cheat Sheets::Azure Global Infrastructure (Tutorials Dojo)")

cards = [
    ("What is an Azure region?", "A group of data centers deployed in a latency-defined perimeter and connected via dedicated regional low-latency network. Each region has multiple data centers.", "infra,regions"),
    ("Name three criteria for choosing an Azure region.", "Location (minimize latency), Features (availability varies by region), Price (costs vary by region).", "infra,regions"),
    ("What is an Azure region pair?", "Each region is paired with another region in the same geographic area for failover and replication; if primary region has outage, failover to secondary.", "infra,regions"),
    ("What are the two unique Azure regions and their restrictions?", "Azure Government Cloud (only US federal/state/local/tribal govs + partners); China Region (data center physically in China, no external connections).", "infra,regions"),
    ("What is an Availability Zone?", "A physical location within a region composed of one or more data centers with independent power, cooling, and networking.", "infra,az"),
    ("What are the two categories of Azure services for Availability Zones?", "Zonal services (pinned to specific zone); Zone-redundant services (auto-replicate across zones).", "infra,az"),
    ("What is bandwidth in Azure infrastructure terms?", "Data moving in/out of Azure data centers or between Azure data centers.", "infra,bandwidth"),
    ("Which data transfers are free in Azure?", "Data transfer TO Azure is always free; data transfer within same AZ is free.", "infra,bandwidth"),
    ("Which data transfers are NOT free in Azure?", "Data transfer between Availability Zones, between regions, and to other continents.", "infra,bandwidth"),
    ("What is Azure Site Recovery?", "Azure's disaster recovery as a service (DRaaS) for minimizing recovery issues and keeping applications available from on-premises to Azure or between regions during outages.", "infra,dr"),
]

for q, a, tags in cards:
    note = genanki.Note(model=model, fields=[q, a, tags])
    deck.add_note(note)

out_file = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_Global_Infrastructure_TD.apkg"
if __name__ == "__main__":
    genanki.Package(deck).write_to_file(out_file)
    print(f"✅ {out_file}")
