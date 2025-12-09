# Azure CLI Labs Reinforcement Deck

## 🎯 Overview

**Comprehensive CLI reinforcement deck** covering completed Azure labs with focus on CLI syntax, verb-noun patterns, and conceptual understanding.

**Questioning Method:** Follows the standard MCQ/True-False system in `Anki-Decks/README.md` (see "Questioning Method (Documented System)"). Default to MCQ; use True/False only for binary, always/never rules.

## 📦 Deck Details

- **File:** `AZ104_CLI_Labs_Reinforcement.apkg`
- **Location:** `/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/`
- **Total Cards:** 28
- **Card cap:** Keep new additions to **20 cards per batch/import** per user limit.
- **Format:** MCQ + True/False with 2-sentence explainers
- **Styling:** #4CAF50 green highlighting (matches AZ-104 Master Deck format)

## 📚 Content Coverage

### Lab 1: Azure VM Basics (7 cards)

- SSH syntax and flags (`-o StrictHostKeyChecking=no`)
- NIC and VNet relationships
- Private vs Public IP architecture
- Linux admin basics (`sudo apt-get update`)
- Resource group concepts

### Lab 2: Azure Bastion (4 cards)

- AzureBastionSubnet sizing requirements (/26 minimum)
- Private IP connectivity (no public IP needed)
- Browser-based HTML5 sessions
- SSH private key authentication workflow
- Zero-trust security principles

### Lab 3: Azure Container Registry - Bicep (7 cards)

- Bicep `param` keyword and input parameters
- Resource block syntax structure
- `az deployment group create` command
- ACR SKU tiers (Basic/Standard/Premium)
- `adminUserEnabled: false` authentication
- Output blocks and their purpose
- Parameter passing with `--parameters` flag

### Lab 4: Azure Kubernetes Service (5 cards)

- Cluster autoscaling configuration
- `az aks get-credentials` and kubeconfig
- RBAC permission troubleshooting
- Azure quota limits and autoscaling restrictions
- Core quota calculations

### CLI Fundamentals (5 cards)

- Azure CLI verb-noun pattern (`az <noun> <verb>`)
- Resource group creation syntax
- Flag abbreviations (`-g`, `-n`, `-l`)
- `--template-file` flag usage
- IaC benefits over manual deployments

## 🎴 Card Format

**Front (Question):**

```
What does the flag -o StrictHostKeyChecking=no do in SSH command?

A) Enforces strict SSL certificate validation
B) Bypasses SSH host key verification to avoid known_hosts prompt
C) Disables password authentication completely
D) Forces use of private key instead of password
```

**Back (Answer Revealed):**

```
[Same question with choice B highlighted in GREEN]

────────────────────────────────
✓ Correct: B - Bypasses host key verification so you don't get
the 'Are you sure?' prompt when connecting to a new VM. Useful
for labs but should be avoided in production for security reasons.
[GREEN BOX with explanation]
```

## 🏷️ Tag Structure

Cards tagged by category for filtered study:

- `CLI` - All CLI-related cards
- `SSH`, `VM`, `Networking` - VM basics
- `Bastion`, `Security`, `Zero-Trust` - Bastion topics
- `Bicep`, `IaC`, `ACR`, `Deployment` - Container Registry
- `AKS`, `Kubernetes`, `Autoscaling`, `RBAC` - AKS cluster
- `Azure-CLI`, `Syntax`, `Patterns` - CLI fundamentals
- `Troubleshooting`, `Quota`, `Authentication` - Problem-solving

## 💡 Question Types

- **MCQ (Multiple Choice):** 23 cards with 4 choices (A-D)
- **True/False:** 5 cards for yes/no concepts
- **All cards:** 2-sentence explainer (150 char max per README spec)

## 🎯 Learning Objectives

This deck reinforces:

1. **CLI Syntax Mastery** - Understand verb-noun patterns and flag usage
2. **Conceptual Understanding** - Why commands work, not just what they do
3. **Security Principles** - Bastion, private IPs, zero-trust architecture
4. **IaC Foundations** - Bicep syntax, parameters, deployment workflows
5. **Troubleshooting Skills** - RBAC errors, quota limits, authentication failures
6. **Best Practices** - When to use Bastion vs public IPs, IaC vs Portal

## 🔄 Reinforcement Strategy

**Spaced Repetition Focus:**

- Review deck after each new lab completion
- Use tags to focus on specific technologies
- Mark difficult cards for extra review
- Combine with Tutorial Dojo cheat sheet decks for comprehensive coverage

## 📝 Future Expansion

Ready to add cards for upcoming labs:

- Azure Storage Accounts
- Azure Load Balancer
- VNet Peering and NSGs
- Azure Monitor + Log Analytics
- Azure DevOps CI/CD Pipelines
- Key Vault and Defender for Cloud

---

## 🧪 Secondary CLI Reinforcement Batch (Testing)

**Status:** In Development  
**Purpose:** Test deck variants and reinforce advanced CLI patterns

### Deck Details

- **File:** `AZ104_CLI_Labs_Reinforcement_Secondary.apkg` (planned)
- **Location:** `/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/`
- **Planned Cards:** 25–30
- **Format:** MCQ + True/False with 2-sentence explainers (matching primary batch)
- **Styling:** #4CAF50 green highlighting (consistent with master deck)

### Content Focus (Planned)

### Lab 5: Advanced Networking Patterns (8 cards)

- NSG rules and precedence
- Service Endpoints vs Private Endpoints
- UDRs (User-Defined Routes) behavior
- Network Watcher diagnostics
- VNet-to-VNet peering troubleshooting

### Lab 6: Storage Account Security (7 cards)

- Storage Account authentication methods
- Shared Access Signatures (SAS) token types
- Managed identity integration with storage
- Encryption at rest and in transit
- Network isolation strategies

### Lab 7: IaC Patterns with Bicep (7 cards)

- Bicep modules and composition
- Parameter files and defaults
- Output references between resources
- Conditional deployments and loops
- Best practices for reusable templates

### Lab 8: Troubleshooting CLI Workflows (5 cards)

- Using `az cli` diagnostic output flags
- Common authentication errors and fixes
- Debugging deployment failures
- Rate limiting and retry strategies
- Log analysis for CLI operations

### Questioning Method

Follows the same **MCQ/True-False** approach as the primary batch (see "Questioning Method (Documented System)" in `../Anki-Decks/README.md`).

### Purpose of Secondary Batch

- **Test variant deck structure** under hierarchical parent (AZ-104 Study Guide → CLI Labs Reinforcement → CLI Labs Secondary)
- **Reinforce advanced patterns** not covered in primary batch
- **Compare spaced repetition** effectiveness across multiple related decks
- **Validate deck generation** script with larger secondary deck structure

### Import Instructions (When Ready)

1. Open Anki
2. Click **File → Import**
3. Select: `AZ104_CLI_Labs_Reinforcement_Secondary.apkg`
4. Cards will appear in deck: **AZ-104 Study Guide::CLI Labs Reinforcement::CLI Labs Secondary**

### Status Tracking

- [ ] Generate 25–30 questions from planned labs
- [ ] Append to CSV with batch category: `CLI Labs Reinforcement Secondary`
- [ ] Generate .apkg file using `create_cli_labs_deck.py` (script may need modification)
- [ ] Import and validate hierarchical deck structure
- [ ] Compare learning outcomes with primary batch
- [ ] Document findings in this section

**Next Review:** December 16, 2025

## 🚀 Import Instructions

1. Open Anki
2. Click **File → Import**
3. Select: `AZ104_CLI_Labs_Reinforcement.apkg`
4. Cards will appear in deck: **AZ-104 Study Guide::CLI Labs Reinforcement**

---

**Created:** December 8, 2024  
**Script:** `/tools/create_cli_labs_deck.py`  
**Format:** Matches approved AZ-104 Master Deck styling
