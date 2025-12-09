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

deck_secondary = genanki.Deck(
    2091607893,
    'AZ-104 Study Guide::CLI Labs Reinforcement::CLI Labs Secondary'
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
         "resource &lt;symbolic-name&gt; = { properties }",
         "resource &lt;symbolic-name&gt; '&lt;type&gt;@&lt;api-version&gt;' = { properties }",
         "resource &lt;type&gt; { name: &lt;symbolic-name&gt;, properties }",
         "resource { type: &lt;type&gt;, name: &lt;symbolic-name&gt; }",
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
        
        ("What is the purpose of the command: az aks get-credentials --resource-group &lt;rg&gt; --name &lt;cluster-name&gt;?",
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
         "az &lt;resource-type&gt; &lt;action&gt; &lt;flags&gt;",
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


def create_cli_secondary_deck():
    """Create the secondary CLI deck (20 cards max)."""
    secondary_questions = [
        # FOUNDATION: RG & CONTEXT
        ("Create the RG baseline for a lab in eastus?",
         "az group create --name <rg> --location eastus",
         "az resource-group new --rg <rg> --region eastus",
         "az group new --location eastus --rg <rg>",
         "az group up --name <rg> eastus",
         "A",
         "az group create is the canonical pattern; keep location explicit to avoid default-region drift.",
         "CLI,Resource-Groups,Foundation"),

        # VM / BASTION / SSH
        ("Need a lab VM fast with SSH keys generated if missing?",
         "az vm create --name <vm> --resource-group <rg> --image UbuntuLTS --generate-ssh-keys",
         "az vm new --image UbuntuLTS --ssh auto",
         "az compute vm create --ssh-gen --image UbuntuLTS",
         "az vm create --ssh auto --image UbuntuLTS",
         "A",
         "--generate-ssh-keys only creates keys if absent and wires them to the VM—ideal for repeatable labs.",
         "CLI,VM,SSH"),

        ("Open HTTP quickly on a lab VM without hand-editing NSG rules?",
         "az vm open-port --port 80 --resource-group <rg> --name <vm>",
         "az network nsg rule add --port 80",
         "az vm expose --http",
         "az network rule create --http",
         "A",
         "az vm open-port patches the attached NSG for you—great for throwaway labs, not for production IaC.",
         "CLI,VM,NSG"),

        ("Bastion prerequisite that always trips people up?",
         "Dedicated subnet named AzureBastionSubnet sized /26 or larger",
         "Any /28 subnet with public IP",
         "GatewaySubnet with public IP",
         "NSG allowing 443 inbound",
         "A",
         "Azure Bastion demands AzureBastionSubnet /26+; without it, az network bastion create fails.",
         "Networking,Bastion,Concept"),

        # NETWORKING / NSG / VNET
        ("Which NSG is evaluated first for inbound traffic to a VM?",
         "NIC NSG then subnet NSG",
         "Subnet NSG then NIC NSG",
         "Route table then NSG",
         "DDoS plan then NSG",
         "B",
         "Subnet NSG evaluates first; NIC NSG can still block. Use az network nic show-effective-nsg to see the result.",
         "Networking,NSG,Diagnostics"),

        ("Check effective NSG outcome from CLI without guessing?",
         "az network nsg list-effective --nic <nic>",
         "az network nic show-effective-nsg --name <nic> --resource-group <rg>",
         "az network watcher show-nsg-flow-log",
         "az network nic show --include-nsg",
         "B",
         "show-effective-nsg merges subnet + NIC rules so you see the final allow/deny state.",
         "CLI,Networking,NSG"),

        # STORAGE
        ("Lock a storage account to private access only via CLI?",
         "az storage account update --name <sa> --resource-group <rg> --public-network-access Disabled",
         "az storage account set --disable-public true",
         "az storage network-rule add --deny-internet",
         "az storage account firewall off",
         "A",
         "--public-network-access Disabled forces private endpoints/trusted networks; align with exam security fundamentals.",
         "CLI,Storage,Security"),

        ("Grant a VM's managed identity read access to blobs (data plane) the CPRS way?",
         "az role assignment create --assignee <identity> --role Reader --scope &lt;sa-resource-id&gt;",
         "az role assignment create --assignee <identity> --role Storage Blob Data Reader --scope &lt;sa-resource-id&gt;",
         "az ad sp create --role BlobReader",
         "az storage account keys list | use key",
         "B",
         "Use data-plane role Storage Blob Data Reader at the storage scope; control-plane Reader is insufficient.",
         "CLI,Storage,RBAC"),

        # LOAD BALANCER
        ("Need zone-redundant inbound for a VM set—Basic or Standard LB?",
         "Basic LB with public IP",
         "Standard LB with zonal frontend",
         "Standard LB with zone-redundant frontend",
         "App Gateway",
         "C",
         "Zone redundancy needs Standard LB + zone-redundant frontend; Basic is single AZ and exam-favored trap.",
         "Load-Balancer,HA,Concept"),

        # ACR / CONTAINERS / BICEP
        ("Deploy ACR via Bicep from CLI matching the lab pattern?",
         "az deployment group create --resource-group <rg> --template-file main.bicep --parameters acrName=<acr> location=eastus",
         "az acr create --file main.bicep",
         "az bicep deploy --rg <rg> --acr main.bicep",
         "az group deployment create --bicep acrName=<acr>",
         "A",
         "Use az deployment group create; the template handles sku/adminUserEnabled. Mirrors the documented snippet.",
         "CLI,ACR,Bicep"),

        ("After disabling ACR admin user, how do you auth for docker push?",
         "Use admin creds from portal",
         "az acr login --name <acr> (uses Azure AD)",
         "docker login <acr>.azurecr.io with shared key",
         "Enable anonymous pull",
         "B",
         "With admin disabled, az acr login uses Azure AD token; no shared secrets needed.",
         "CLI,ACR,Auth"),

        ("Build/push without local docker engine in labs?",
         "az acr push --image app:1.0 --source .",
         "az acr build --registry <acr> --image app:1.0 .",
         "az docker build --acr <acr>",
         "az acr ci --image app:1.0 --local",
         "B",
         "az acr build runs the build in Azure and pushes automatically—perfect for student machines.",
         "CLI,ACR,Build"),

        # AKS
        ("Quota warning: autoscaler stops at 5 nodes; what’s happening?",
         "AKS Basic tier limit",
         "Region core quota exhausted for that VM size",
         "Kubelet bug",
         "Subnet IP exhaustion",
         "B",
         "Core quota caps scale-out. CLI hint: change size/region or request quota before retrying az aks nodepool scale.",
         "AKS,Quota,Troubleshooting"),

        ("RBAC block: az aks get-credentials returns AuthorizationFailed—fastest exam-safe takeaway?",
         "Cluster is stopped",
         "listClusterUserCredential/action denied to your account",
         "kubectl not installed",
         "Wrong region",
         "B",
         "Labs often restrict listClusterUserCredential; know the error so you pivot to portal deployment path.",
         "AKS,RBAC,Diagnostics"),

        # APP SERVICE / IDENTITY / FUNCTIONS
        ("Deploy a containerized Web App tied to ACR?",
         "az webapp create --resource-group <rg> --plan <plan> --name <app> --deployment-container-image-name <acr>.azurecr.io/app:1.0",
         "az appservice plan create --acr <acr> --app <app>",
         "az webapp up --acr <acr>",
         "az webapp create --acr --image app:1.0",
         "A",
         "Use deployment-container-image-name; pair with a Linux plan sized for containers.",
         "CLI,AppService,Containers"),

        ("Assign a system-assigned managed identity to an App Service?",
         "az webapp identity assign --name <app> --resource-group <rg>",
         "az webapp set-identity on",
         "az identity create --resource-group <rg> --name <app>",
         "Enable MSI in portal only",
         "A",
         "az webapp identity assign flips on system MSI so you can grant RBAC (e.g., Key Vault access).",
         "CLI,Identity,AppService"),

        ("Secure a Function app’s secrets with Key Vault the exam-proof way?",
         "Store secrets in app settings",
         "Use Key Vault references after granting MSI access",
         "Embed secrets in code",
         "Use public configuration file",
         "B",
         "Enable MSI then Key Vault references; aligns with Security Fundamentals + Serverless labs.",
         "Functions,KeyVault,Security"),

        # MONITOR / LOGS / DEVOPS
        ("Send platform logs to Log Analytics via CLI?",
         "az monitor diagnostic-settings create --resource <id> --logs '[{\\\"category\\\":\\\"AllLogs\\\"}]' --workspace <la>",
         "az monitor logs enable --workspace <la>",
         "az loganalytics connect --resource <id>",
         "az monitor metrics-push --workspace <la>",
         "A",
         "Diagnostic settings pipe resource logs/metrics to Log Analytics—core for Azure Monitor questions.",
         "CLI,Monitor,Diagnostics"),

        ("CLI pattern to grant RBAC at a scoped resource (e.g., Reader on a RG)?",
         "az ad user add-role --role Reader --resource-group <rg>",
         "az role assignment create --assignee <objId> --role Reader --scope $(az group show -n <rg> --query id -o tsv)",
         "az rbac set --role Reader --rg <rg>",
         "az group role add Reader <rg>",
         "B",
         "az role assignment create with explicit scope is the exam-ready pattern; Reader at RG is common.",
         "CLI,RBAC,Security"),

        ("CI/CD quick check: which Azure CLI command sets up a DevOps pipeline?",
         "az pipelines create",
         "az devops pipeline create --name <name> --repository <repo> --yaml-path <path>",
         "az ado pipeline new",
         "az pipelines up",
         "B",
         "az devops pipeline create (with org/project context) is the right verb-noun; others are distractors.",
         "CLI,DevOps,CI-CD"),

    ]

    for q_text, choice_a, choice_b, choice_c, choice_d, correct, explanation, tags in secondary_questions:
        if choice_c == "" and choice_d == "":
            question_front = f'{q_text}\n\n<div class="choice">A) {choice_a}</div>\n<div class="choice">B) {choice_b}</div>'
        else:
            question_front = f'{q_text}\n\n<div class="choice">A) {choice_a}</div>\n<div class="choice">B) {choice_b}</div>\n<div class="choice">C) {choice_c}</div>\n<div class="choice">D) {choice_d}</div>'

        if choice_c == "" and choice_d == "":
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
        deck_secondary.add_note(note)

if __name__ == '__main__':
    create_cli_deck()
    output_path = '/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_CLI_Labs_Reinforcement.apkg'
    genanki.Package(deck).write_to_file(output_path)
    print(f'✅ CLI Labs Reinforcement Deck created: {output_path}')
    print(f'📊 Total cards: {len(deck.notes)}')

    create_cli_secondary_deck()
    output_path_secondary = '/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/Anki-Decks/AZ104_CLI_Labs_Reinforcement_Secondary.apkg'
    genanki.Package(deck_secondary).write_to_file(output_path_secondary)
    print(f'✅ CLI Labs Secondary Deck created: {output_path_secondary}')
    print(f'📊 Total cards: {len(deck_secondary.notes)}')
