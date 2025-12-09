#!/usr/bin/env python3
"""
Generate Azure CLI Labs Reinforcement Deck
Covers: VM Basics, Bastion, ACR (Bicep), AKS
Format: MCQ + Yes/No with 2-sentence explainers
Matches AZ-104 Master Deck styling (#4CAF50 green)
"""
import genanki

# Match exact model from approved format
cli_model = genanki.Model(
    1607392322,
    'Azure CLI Labs Reinforcement Model',
    fields=[
        {'name': 'Question'},
        {'name': 'QuestionWithAnswer'},
        {'name': 'Answer'},
        {'name': 'Tags'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{QuestionWithAnswer}}<style>.choice.correct { background-color: #4CAF50 !important; color: white !important; border-color: #45a049 !important; font-weight: bold; }</style><hr><div style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; font-size: 16px;">{{Answer}}</div>',
        },
    ],
    css="""
.card {
    font-family: Arial, sans-serif;
    font-size: 18px;
    line-height: 1.6;
    color: black;
    background-color: white;
    padding: 20px;
}

.choice {
    background-color: #f9f9f9;
    border: 2px solid #cccccc;
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 8px;
    display: block;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    color: #333333;
    font-weight: normal;
}
    """
)

deck = genanki.Deck(
    2091607892,
    'AZ-104 Study Guide::CLI Labs Reinforcement'
)

def create_cli_deck():
    # (Question, ChoiceA, ChoiceB, ChoiceC, ChoiceD, Correct, Explanation, Tags)
    questions = [
        # VM BASICS - SSH & Networking
        ("What does the flag -o StrictHostKeyChecking=no do in the SSH command: ssh -o StrictHostKeyChecking=no azureuser@<ip>?",
         "Enforces strict SSL certificate validation",
         "Bypasses SSH host key verification to avoid the known_hosts prompt on first connection",
         "Disables password authentication completely",
         "Forces use of private key instead of password",
         "B",
         "Correct: B - Bypasses host key verification so you don't get the 'Are you sure?' prompt when connecting to a new VM. Useful for labs but should be avoided in production for security reasons.",
         "CLI,SSH,VM,Networking"),
        
        ("When you create an Azure VM, which networking component connects the VM to a VNet?",
         "Public IP address",
         "Network Security Group (NSG)",
         "Network Interface Card (NIC)",
         "Virtual Network Gateway",
         "C",
         "Correct: C - The NIC is the bridge connecting your VM to the VNet. The NIC gets assigned to a subnet and can have public/private IPs attached to it.",
         "CLI,VM,Networking,NIC"),
        
        ("True or False: A VM can exist without a public IP but still communicate within its VNet using a private IP.",
         "True",
         "False",
         "",
         "",
         "A",
         "Correct: A - VMs use private IPs for internal VNet communication. Public IPs are only needed for internet access—Azure Bastion proves this by connecting to VMs with no public IP.",
         "CLI,VM,Networking,IP"),
        
        ("What is the purpose of running sudo apt-get update after SSH-ing into a Linux VM?",
         "Installs all available security patches immediately",
         "Refreshes the package manager's repository index so you can install the latest versions of software",
         "Updates the VM's kernel to the latest version",
         "Configures automatic updates for the VM",
         "B",
         "Correct: B - Updates the package list from repositories so apt knows what packages are available. It does NOT install updates—that's what apt-get upgrade does.",
         "CLI,Linux,VM,Admin"),
        
        # AZURE BASTION
        ("What is the minimum subnet size required for AzureBastionSubnet?",
         "/28 (16 IPs)",
         "/27 (32 IPs)",
         "/26 (64 IPs)",
         "/24 (256 IPs)",
         "C",
         "Correct: C - AzureBastionSubnet requires /26 or larger. Azure reserves 5 IPs in any subnet, so /26 provides 64 IPs with 59 usable addresses for Bastion infrastructure.",
         "CLI,Bastion,Networking,Subnet"),
        
        ("True or False: Azure Bastion requires the target VM to have a public IP address.",
         "True",
         "False",
         "",
         "",
         "B",
         "Correct: B - Bastion connects to VMs using their private IPs only. This is the whole point—secure access without exposing VMs to the internet via public IPs.",
         "CLI,Bastion,Security,Networking"),
        
        ("How does Azure Bastion provide secure VM access?",
         "Creates a VPN tunnel from your laptop to Azure",
         "Uses HTML5 browser session to connect to VMs via private IP without requiring public IP on VM",
         "Automatically rotates SSH keys every 24 hours",
         "Encrypts all traffic using Azure Key Vault",
         "B",
         "Correct: B - Bastion acts as a jump box in your VNet, using browser-based RDP/SSH sessions. Traffic stays within Azure network—no public IPs, no VPN client needed.",
         "CLI,Bastion,Security,Architecture"),
        
        ("When using Azure Bastion with SSH private key authentication, where do you upload the private key file?",
         "Directly to the VM during creation",
         "Azure Key Vault for secure storage",
         "Azure Portal Bastion connection blade when initiating the SSH session",
         "Cloud Shell before connecting",
         "C",
         "Correct: C - You upload the .pem private key file in the Azure Portal when connecting via Bastion. Bastion uses it to authenticate without the key ever leaving your browser session.",
         "CLI,Bastion,SSH,Authentication"),
        
        # AZURE CONTAINER REGISTRY (ACR) - BICEP
        ("In Bicep syntax, what does the param keyword define?",
         "A variable that is calculated during deployment",
         "An input parameter that can be passed when deploying the template",
         "A resource output that can be referenced by other templates",
         "A dependency between resources",
         "B",
         "Correct: B - param defines inputs that must be provided at deployment time. This makes templates reusable—same template, different parameter values for different environments.",
         "CLI,Bicep,IaC,Parameters"),
        
        ("What is the structure of a Bicep resource block?",
         "resource <symbolic-name> = { properties }",
         "resource <symbolic-name> '<type>@<api-version>' = { properties }",
         "resource <type> { name: <symbolic-name>, properties }",
         "resource { type: <type>, name: <symbolic-name> }",
         "B",
         "Correct: B - Format is: resource symbolicName 'resourceType@apiVersion' = { name: 'actualName', properties }. Symbolic name is for referencing in template; actual name is deployed to Azure.",
         "CLI,Bicep,IaC,Syntax"),
        
        ("Which Azure CLI command deploys a Bicep template to a resource group?",
         "az bicep deploy --template-file main.bicep --resource-group <rg>",
         "az deployment group create --resource-group <rg> --template-file main.bicep",
         "az group deployment create --template-file main.bicep",
         "az bicep create --file main.bicep --resource-group <rg>",
         "B",
         "Correct: B - az deployment group create is the correct command. The --template-file flag accepts .bicep files directly—Azure CLI automatically transpiles to ARM JSON.",
         "CLI,Bicep,Deployment,Azure-CLI"),
        
        ("What are the three ACR SKU tiers?",
         "Free, Standard, Premium",
         "Basic, Standard, Premium",
         "Developer, Standard, Enterprise",
         "Shared, Dedicated, Isolated",
         "B",
         "Correct: B - ACR offers Basic (small teams, dev/test), Standard (production workloads), Premium (geo-replication, content trust, private endpoints). Each tier adds features and performance.",
         "CLI,ACR,Container-Registry,SKU"),
        
        ("True or False: When you set adminUserEnabled: false in ACR Bicep config, you must use Azure AD authentication for registry access.",
         "True",
         "False",
         "",
         "",
         "A",
         "Correct: A - Disabling admin user forces use of Azure AD (service principals, managed identities, or user accounts). This is best practice for security—admin credentials are shared secrets.",
         "CLI,ACR,Security,Authentication"),
        
        ("What is the purpose of the output block in a Bicep template?",
         "Validates the template syntax before deployment",
         "Returns values from deployed resources that can be used by other templates or displayed after deployment",
         "Logs deployment events to Azure Monitor",
         "Defines which properties should be exported to CSV",
         "B",
         "Correct: B - Outputs let you return values like resource IDs, FQDNs, or connection strings after deployment. These can be consumed by other templates or displayed to users.",
         "CLI,Bicep,IaC,Outputs"),
        
        ("In the command: az deployment group create --template-file main.bicep --parameters acrName=myacr location=eastus, what are acrName and location?",
         "Bicep variables calculated at runtime",
         "Parameter values being passed to override the template's default param values",
         "Resource properties automatically detected by Azure",
         "Output values from a previous deployment",
         "B",
         "Correct: B - These are parameter values provided at deployment time using --parameters flag. They override or provide values for params defined in the Bicep template.",
         "CLI,Bicep,Parameters,Azure-CLI"),
        
        # AKS CLUSTER
        ("What does autoscale configuration do for an AKS cluster?",
         "Automatically scales pod replicas based on CPU usage",
         "Dynamically adjusts the number of nodes in the cluster based on resource demand (min/max node count)",
         "Scales VM size up or down based on workload",
         "Automatically upgrades Kubernetes version",
         "B",
         "Correct: B - Cluster autoscaler adds/removes nodes based on pending pods that can't be scheduled. Node-level scaling, not pod-level (that's Horizontal Pod Autoscaler).",
         "CLI,AKS,Kubernetes,Autoscaling"),
        
        ("What is the purpose of the command: az aks get-credentials --resource-group <rg> --name <cluster-name>?",
         "Creates a new service principal for the cluster",
         "Downloads the kubeconfig file to your local machine so kubectl can authenticate with the AKS cluster",
         "Retrieves the cluster admin password",
         "Exports all cluster logs to your local machine",
         "B",
         "Correct: B - Merges AKS cluster credentials into ~/.kube/config file. This configures kubectl to point to your AKS cluster with proper authentication context.",
         "CLI,AKS,Kubernetes,Authentication"),
        
        ("Why might az aks get-credentials fail with AuthorizationFailed error in a lab environment?",
         "The AKS cluster is not running",
         "The user account lacks RBAC permissions for listClusterUserCredential action",
         "The cluster is in a different region",
         "kubectl is not installed",
         "B",
         "Correct: B - Sandbox/lab environments often restrict RBAC permissions. listClusterUserCredential/action is required to download kubeconfig—admins in production have it, lab users often don't.",
         "CLI,AKS,RBAC,Troubleshooting"),
        
        ("True or False: In Azure, quota limits can prevent AKS autoscaling beyond a certain node count even if you configure higher max-nodes.",
         "True",
         "False",
         "",
         "",
         "A",
         "Correct: A - Quota limits (e.g., 10 cores remaining) can block node scaling. Azure won't provision nodes that exceed subscription quota—autoscaler fails silently until quota is increased.",
         "CLI,AKS,Quota,Autoscaling"),
        
        ("What does the error 'Autoscaling may fail above 5 nodes due to quota restrictions' indicate?",
         "AKS cluster is misconfigured",
         "Your Azure subscription has insufficient core quota to support more than 5 nodes of the configured VM size",
         "AKS Basic tier only supports 5 nodes maximum",
         "The cluster requires a manual upgrade",
         "B",
         "Correct: B - Each node requires cores (e.g., 2 cores/node). If you have 10 cores remaining and 2-core VMs, you can only add 5 nodes before hitting quota limits.",
         "CLI,AKS,Quota,Azure-Limits"),
        
        # CLI VERB-NOUN PATTERNS
        ("In Azure CLI, what is the standard command structure pattern?",
         "az <verb> <noun> <parameters>",
         "az <noun> <verb> <parameters>",
         "az <resource-type> <action> <flags>",
         "az <action> <resource> <options>",
         "B",
         "Correct: B - Azure CLI follows the pattern: az <noun> <verb>. Example: az vm create (vm is noun, create is verb). This differs from imperative kubectl style.",
         "CLI,Azure-CLI,Syntax,Patterns"),
        
        ("Which command creates a resource group in Azure CLI?",
         "az group create --name <rg> --location <region>",
         "az resource-group create --name <rg> --location <region>",
         "az rg create --name <rg> --location <region>",
         "az create group --name <rg> --location <region>",
         "A",
         "Correct: A - Follows az <noun> <verb> pattern: az group create. --name and --location are required parameters for the resource group.",
         "CLI,Azure-CLI,Resource-Groups,Syntax"),
        
        ("True or False: In Azure CLI, flags can be abbreviated if they are unambiguous (e.g., -g for --resource-group).",
         "True",
         "False",
         "",
         "",
         "A",
         "Correct: A - Azure CLI supports short flags for common parameters: -g (resource group), -n (name), -l (location). Improves typing speed but reduces readability in scripts.",
         "CLI,Azure-CLI,Flags,Syntax"),
        
        ("What does the --template-file flag specify in az deployment group create?",
         "The name of the deployed resource",
         "The path to the Bicep or ARM JSON template file to deploy",
         "The output file where deployment results are saved",
         "The parameter file containing template inputs",
         "B",
         "Correct: B - Points to the IaC template file (.bicep or .json). Azure CLI reads this file to understand what resources to deploy.",
         "CLI,Azure-CLI,Bicep,Deployment"),
        
        # CONCEPTUAL REINFORCEMENT
        ("Why is it important to understand private vs public IP addressing in Azure VMs?",
         "Public IPs are free, private IPs have hourly costs",
         "Private IPs enable VNet communication; public IPs expose VMs to internet—understanding this is critical for security architecture",
         "Private IPs are faster than public IPs",
         "Only premium VMs support private IPs",
         "B",
         "Correct: B - Private IPs allow internal Azure networking without internet exposure. Public IPs open attack surface—services like Bastion eliminate public IP requirements.",
         "CLI,Networking,Security,Concepts"),
        
        ("What is the relationship between a resource group and Azure resources?",
         "Resource groups are billing containers only",
         "Resource groups are logical containers for managing and organizing related Azure resources with shared lifecycle",
         "Each resource can belong to multiple resource groups",
         "Resource groups only apply to VMs",
         "B",
         "Correct: B - Resource groups are management containers—all resources in a group can be deployed, updated, or deleted together. Each resource belongs to exactly one RG.",
         "CLI,Resource-Groups,Azure-Fundamentals,Concepts"),
        
        ("Why is Infrastructure as Code (Bicep/Terraform) preferred over manual Azure Portal deployments?",
         "Portal deployments are deprecated",
         "IaC provides repeatability, version control, and automation—manual deployments are error-prone and non-reproducible",
         "Portal deployments cost more",
         "IaC is required for production environments",
         "B",
         "Correct: B - IaC templates are declarative, version-controlled, and repeatable. Portal clicks can't be audited or replicated—IaC is essential for DevOps and enterprise governance.",
         "CLI,IaC,Bicep,DevOps"),
        
        ("What security principle does Azure Bastion demonstrate?",
         "Defense in depth",
         "Zero-trust networking—no public IPs on VMs, access through secure managed jump box",
         "Role-based access control",
         "Encryption at rest",
         "B",
         "Correct: B - Bastion eliminates public IPs and RDP/SSH exposure to internet. All access flows through Bastion's managed infrastructure—reduces attack surface dramatically.",
         "CLI,Bastion,Security,Zero-Trust"),
    ]
    
    for q_text, choice_a, choice_b, choice_c, choice_d, correct, explanation, tags in questions:
        # Build front (no highlighting)
        if choice_c == "" and choice_d == "":  # True/False question
            question_front = f'{q_text}\n\n<div class="choice">A) {choice_a}</div>\n<div class="choice">B) {choice_b}</div>'
        else:
            question_front = f'{q_text}\n\n<div class="choice">A) {choice_a}</div>\n<div class="choice">B) {choice_b}</div>\n<div class="choice">C) {choice_c}</div>\n<div class="choice">D) {choice_d}</div>'
        
        # Build back (correct answer highlighted)
        if choice_c == "" and choice_d == "":  # True/False
            question_back = f'{q_text}\n\n'
            question_back += f'<div class="choice{"" if correct != "A" else " correct"}">A) {choice_a}</div>\n'
            question_back += f'<div class="choice{"" if correct != "B" else " correct"}">B) {choice_b}</div>'
        else:
            question_back = f'{q_text}\n\n'
            question_back += f'<div class="choice{"" if correct != "A" else " correct"}">A) {choice_a}</div>\n'
            question_back += f'<div class="choice{"" if correct != "B" else " correct"}">B) {choice_b}</div>\n'
            question_back += f'<div class="choice{"" if correct != "C" else " correct"}">C) {choice_c}</div>\n'
            question_back += f'<div class="choice{"" if correct != "D" else " correct"}">D) {choice_d}</div>'
        
        note = genanki.Note(
            model=cli_model,
            fields=[question_front, question_back, explanation, tags]
        )
        deck.add_note(note)

if __name__ == '__main__':
    create_cli_deck()
    output_path = '/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_CLI_Labs_Reinforcement.apkg'
    genanki.Package(deck).write_to_file(output_path)
    print(f'✅ CLI Labs Reinforcement Deck created: {output_path}')
    print(f'📊 Total cards: {len(deck.notes)}')
