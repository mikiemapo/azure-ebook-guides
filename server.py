import os
import json
import re
import uuid
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__, static_folder='docs')
CORS(app)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

SYNC_DATA_DIR = os.path.join(os.path.dirname(__file__), '.sync_data')
os.makedirs(SYNC_DATA_DIR, exist_ok=True)

AZ104_OBJECTIVES = {
    "domains": [
        {
            "id": "1",
            "name": "Manage Azure Identities and Governance",
            "weight": "20-25%",
            "objectives": [
                {"id": "1.1", "name": "Manage Microsoft Entra users and groups", "skills": ["Create users and groups", "Manage user and group properties", "Manage licenses in Microsoft Entra ID", "Manage external users", "Configure self-service password reset (SSPR)"]},
                {"id": "1.2", "name": "Manage access to Azure resources", "skills": ["Manage built-in Azure roles", "Assign roles at different scopes", "Interpret access assignments"]},
                {"id": "1.3", "name": "Manage Azure subscriptions and governance", "skills": ["Implement and manage Azure Policy", "Configure resource locks", "Apply and manage tags on resources", "Manage resource groups", "Manage subscriptions", "Manage costs by using alerts, budgets, and Azure Advisor recommendations", "Configure management groups"]}
            ]
        },
        {
            "id": "2",
            "name": "Implement and Manage Storage",
            "weight": "15-20%",
            "objectives": [
                {"id": "2.1", "name": "Configure access to storage", "skills": ["Configure Azure Storage firewalls and virtual networks", "Create and use shared access signature (SAS) tokens", "Configure stored access policies", "Manage access keys", "Configure identity-based access for Azure Files"]},
                {"id": "2.2", "name": "Configure and manage storage accounts", "skills": ["Create and configure storage accounts", "Configure Azure Storage redundancy", "Configure object replication", "Configure storage account encryption", "Manage data by using Azure Storage Explorer and AzCopy"]},
                {"id": "2.3", "name": "Configure Azure Files and Azure Blob Storage", "skills": ["Create and configure a file share in Azure Storage", "Create and configure a container in Blob Storage", "Configure storage tiers", "Configure soft delete for blobs and containers", "Configure snapshots and soft delete for Azure Files", "Configure blob lifecycle management", "Configure blob versioning"]}
            ]
        },
        {
            "id": "3",
            "name": "Deploy and Manage Azure Compute Resources",
            "weight": "20-25%",
            "objectives": [
                {"id": "3.1", "name": "Automate deployment of resources by using ARM templates or Bicep files", "skills": ["Interpret an Azure Resource Manager template or a Bicep file", "Modify an existing Azure Resource Manager template", "Modify an existing Bicep file", "Deploy resources by using an Azure Resource Manager template or a Bicep file", "Export a deployment as an Azure Resource Manager template or convert an Azure Resource Manager template to a Bicep file"]},
                {"id": "3.2", "name": "Create and configure virtual machines", "skills": ["Create a virtual machine", "Configure Azure Disk Encryption", "Move a virtual machine to another resource group, subscription, or region", "Manage virtual machine sizes", "Manage virtual machine disks", "Deploy virtual machines to availability zones and availability sets", "Deploy and configure an Azure Virtual Machine Scale Sets"]},
                {"id": "3.3", "name": "Provision and manage containers in the Azure portal", "skills": ["Create and manage an Azure container registry", "Provision a container by using Azure Container Instances", "Provision a container by using Azure Container Apps", "Manage sizing and scaling for containers, including Azure Container Instances and Azure Container Apps"]},
                {"id": "3.4", "name": "Create and configure Azure App Service", "skills": ["Provision an App Service plan", "Configure scaling for an App Service plan", "Create an App Service", "Configure certificates and Transport Layer Security (TLS) for an App Service", "Map an existing custom DNS name to an App Service", "Configure backup for an App Service", "Configure networking settings for an App Service", "Configure deployment slots for an App Service"]}
            ]
        },
        {
            "id": "4",
            "name": "Implement and Manage Virtual Networking",
            "weight": "15-20%",
            "objectives": [
                {"id": "4.1", "name": "Configure and manage virtual networks in Azure", "skills": ["Create and configure virtual networks and subnets", "Create and configure virtual network peering", "Configure public IP addresses", "Configure user-defined network routes", "Troubleshoot network connectivity"]},
                {"id": "4.2", "name": "Configure secure access to virtual networks", "skills": ["Create and configure network security groups (NSGs) and application security groups", "Evaluate effective security rules in NSGs", "Implement Azure Bastion", "Configure service endpoints for Azure platform as a service (PaaS)", "Configure private endpoints for Azure PaaS"]},
                {"id": "4.3", "name": "Configure name resolution and load balancing", "skills": ["Configure Azure DNS", "Configure an internal or public load balancer", "Troubleshoot load balancing"]}
            ]
        },
        {
            "id": "5",
            "name": "Monitor and Maintain Azure Resources",
            "weight": "10-15%",
            "objectives": [
                {"id": "5.1", "name": "Monitor resources by using Azure Monitor", "skills": ["Configure and interpret metrics", "Configure Azure Monitor Logs", "Query and analyze logs", "Set up alerts and actions", "Configure monitoring of VMs, storage accounts, and networks by using VM insights"]},
                {"id": "5.2", "name": "Implement backup and recovery", "skills": ["Create an Azure Recovery Services vault", "Create an Azure Backup vault", "Create and configure backup policy", "Perform backup and restore operations by using Azure Backup", "Configure Azure Site Recovery for Azure resources", "Perform failover to a secondary region by using Azure Site Recovery", "Configure and review backup reports"]}
            ]
        }
    ]
}

@app.route('/api/objectives', methods=['GET'])
def get_objectives():
    return jsonify(AZ104_OBJECTIVES)

GUIDE_INDEX = {
    "Azure AD": {"file": "azure_ad_overview.html", "section": "Azure Active Directory"},
    "Entra ID": {"file": "azure_ad_overview.html", "section": "Microsoft Entra ID"},
    "RBAC": {"file": "azure_rbac_guide.html", "section": "Role-Based Access Control"},
    "Azure Policy": {"file": "azure_policy_guide.html", "section": "Azure Policy"},
    "Management Groups": {"file": "azure_management_groups.html", "section": "Management Groups"},
    "Subscriptions": {"file": "azure_subscriptions_guide.html", "section": "Subscriptions"},
    "Resource Groups": {"file": "azure_resource_groups.html", "section": "Resource Groups"},
    "Storage Accounts": {"file": "azure_storage_accounts.html", "section": "Storage Accounts"},
    "Blob Storage": {"file": "azure_blob_storage.html", "section": "Blob Storage"},
    "Azure Files": {"file": "azure_files_guide.html", "section": "Azure Files"},
    "Storage Replication": {"file": "azure_storage_replication.html", "section": "Storage Replication"},
    "Virtual Machines": {"file": "azure_vm_guide.html", "section": "Virtual Machines"},
    "VM Scale Sets": {"file": "azure_vmss_guide.html", "section": "VM Scale Sets"},
    "Availability Sets": {"file": "azure_availability_sets.html", "section": "Availability Sets"},
    "Azure App Service": {"file": "azure_app_service.html", "section": "App Service"},
    "Azure Container Instances": {"file": "azure_aci_guide.html", "section": "Container Instances"},
    "Azure Kubernetes Service": {"file": "azure_aks_guide.html", "section": "AKS"},
    "Virtual Networks": {"file": "azure_vnet_guide.html", "section": "Virtual Networks"},
    "VNet Peering": {"file": "azure_vnet_peering.html", "section": "VNet Peering"},
    "Network Security Groups": {"file": "azure_nsg_guide.html", "section": "NSGs"},
    "Azure Load Balancer": {"file": "azure_load_balancer.html", "section": "Load Balancer"},
    "Application Gateway": {"file": "azure_app_gateway.html", "section": "Application Gateway"},
    "Azure DNS": {"file": "azure_dns_guide.html", "section": "Azure DNS"},
    "VPN Gateway": {"file": "azure_vpn_gateway.html", "section": "VPN Gateway"},
    "ExpressRoute": {"file": "azure_expressroute.html", "section": "ExpressRoute"},
    "Azure Monitor": {"file": "azure_monitor_guide.html", "section": "Azure Monitor"},
    "Log Analytics": {"file": "azure_log_analytics.html", "section": "Log Analytics"},
    "Azure Backup": {"file": "azure_backup_guide.html", "section": "Azure Backup"},
    "Azure Site Recovery": {"file": "azure_site_recovery.html", "section": "Site Recovery"},
    "Azure Alerts": {"file": "azure_alerts_guide.html", "section": "Alerts"},
}

def find_guide_references(concepts):
    refs = []
    for concept in concepts:
        concept_lower = concept.lower()
        for key, value in GUIDE_INDEX.items():
            if key.lower() in concept_lower or concept_lower in key.lower():
                refs.append({
                    "concept": concept,
                    "guide": value["file"],
                    "section": value["section"]
                })
                break
    return refs

def extract_concepts_from_text(text):
    azure_keywords = [
        "Azure AD", "Entra ID", "RBAC", "Azure Policy", "Management Groups",
        "Subscriptions", "Resource Groups", "Storage Accounts", "Blob Storage",
        "Azure Files", "File Sync", "Storage Replication", "LRS", "ZRS", "GRS",
        "Virtual Machines", "VM Scale Sets", "Availability Sets", "Availability Zones",
        "App Service", "Container Instances", "ACI", "Kubernetes", "AKS",
        "Virtual Networks", "VNet", "VNet Peering", "NSG", "Network Security Groups",
        "Load Balancer", "Application Gateway", "Azure DNS", "VPN Gateway",
        "ExpressRoute", "Azure Monitor", "Log Analytics", "Azure Backup",
        "Site Recovery", "Alerts", "Action Groups", "Metrics", "Diagnostic Settings",
        "ARM Templates", "Bicep", "Azure CLI", "PowerShell", "Cloud Shell",
        "Service Principal", "Managed Identity", "Key Vault", "SAS Token",
        "Access Tier", "Hot", "Cool", "Archive", "Lifecycle Management",
        "Private Endpoints", "Service Endpoints", "Azure Firewall", "WAF",
        "Traffic Manager", "Front Door", "CDN", "Azure Bastion"
    ]
    
    found = []
    text_lower = text.lower()
    for keyword in azure_keywords:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return list(set(found))

@app.route('/api/extract-concepts', methods=['POST'])
def extract_concepts():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    raw_text = data['text']
    local_concepts = extract_concepts_from_text(raw_text)
    guide_refs = find_guide_references(local_concepts)
    
    if not openai_client:
        return jsonify({
            "fallback": True,
            "fallback_reason": "OpenAI API key not configured",
            "local_concepts": local_concepts,
            "guide_references": guide_refs,
            "concepts": [],
            "summary": "AI analysis unavailable - using keyword extraction mode."
        }), 200
    
    try:
        prompt = f"""You are an Azure certification expert using the CPRS (Concept-Pathway Reinforcement System) methodology.

Analyze the following quiz review content where the student got questions wrong.

For each concept mentioned, apply the CPRS framework:
1. FOUNDATION: What problem does this concept solve?
2. DEFINITION: Precise one-sentence definition
3. DIFFERENTIATION: How is it different from commonly confused services?
4. WHY WRONG: Why the student's answer was incorrect
5. COMPRESSION: One-sentence memory hook for instant recall
6. The AZ-104 exam objective it relates to (e.g., 1.2, 3.3)

Format your response as JSON with this structure:
{{
    "concepts": [
        {{
            "name": "concept name",
            "foundation": "the root purpose/problem it solves",
            "definition": "precise one-sentence definition",
            "differentiation": "how it differs from similar services",
            "correct_fact": "the accurate Azure fact",
            "why_wrong": "brief explanation of the misconception",
            "compression": "one-sentence memory hook",
            "objective": "X.X"
        }}
    ],
    "summary": "A 2-3 sentence NotebookLM-ready summary using CPRS structure focusing on the weak areas"
}}

Quiz review content:
{raw_text[:4000]}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an Azure certification expert who provides accurate, authoritative Azure facts for the AZ-104 exam. Always be precise and factual."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        
        result = json.loads(response.choices[0].message.content)
        
        all_concept_names = [c['name'] for c in result.get('concepts', [])]
        all_concept_names.extend(local_concepts)
        
        guide_refs = find_guide_references(all_concept_names)
        
        result['guide_references'] = guide_refs
        result['local_concepts'] = local_concepts
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "fallback": True,
            "local_concepts": local_concepts,
            "guide_references": guide_refs,
            "concepts": [],
            "summary": "AI analysis failed - using keyword extraction mode."
        }), 200

@app.route('/api/generate-cprs', methods=['POST'])
def generate_cprs():
    data = request.get_json()
    if not data or 'concept' not in data:
        return jsonify({"error": "No concept provided"}), 400
    
    concept = data['concept'].strip()
    if not concept:
        return jsonify({"error": "Concept cannot be empty"}), 400
    
    guide_refs = find_guide_references([concept])
    
    if not openai_client:
        return jsonify({
            "fallback": True,
            "fallback_reason": "OpenAI API key not configured",
            "concept": concept,
            "guide_references": guide_refs,
            "questions": []
        }), 200
    
    try:
        prompt = f"""You are an Azure certification expert using the CPRS (Concept-Pathway Reinforcement System) methodology.

Generate 6 SEPARATE multiple-choice questions (MCQ) for: "{concept}"

Each question MUST have 4 options (A, B, C, D) and one correct answer.

QUESTION 1 - FOUNDATION (Root Purpose):
Test understanding of what problem {concept} solves.
Example angle: "Which scenario best describes the primary use case for {concept}?"

QUESTION 2 - DEFINITION (Textbook Clarity):
Test knowing the precise definition of {concept}.
Example angle: "Which statement correctly defines {concept}?"

QUESTION 3 - DIFFERENTIATION (Compare Similar Services):
Test distinguishing {concept} from commonly confused Azure services.
Example angle: "A company needs [scenario]. Which service should they use: {concept} or [similar service]?"

QUESTION 4 - SCENARIO (Exam-Style Application):
A realistic AZ-104 exam question applying {concept} to a business scenario.
Include subtle misdirection like Microsoft uses. All options must sound plausible.

QUESTION 5 - ANTI-CONFUSION (Trap Recognition):
Test recognizing why wrong answers are wrong.
Example angle: "Which statement about {concept} is FALSE?" or "Which scenario would NOT be appropriate for {concept}?"

QUESTION 6 - COMPRESSION (Memory Hook):
Test the core takeaway that summarizes {concept}.
Example angle: "Which one-sentence summary best captures the essence of {concept}?"

Format your response as JSON with ALL 6 questions as MCQs:
{{
    "concept": "{concept}",
    "questions": [
        {{
            "type": "Foundation",
            "question": "the MCQ question text",
            "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        }},
        {{
            "type": "Definition",
            "question": "the MCQ question text",
            "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        }},
        {{
            "type": "Differentiation",
            "question": "the MCQ question text",
            "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        }},
        {{
            "type": "Scenario",
            "question": "the MCQ question text",
            "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        }},
        {{
            "type": "Anti-Confusion",
            "question": "the MCQ question text",
            "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        }},
        {{
            "type": "Compression",
            "question": "the MCQ question text",
            "options": {{"A": "option A", "B": "option B", "C": "option C", "D": "option D"}},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        }}
    ],
    "objective": "X.X (the AZ-104 exam objective code)"
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an Azure certification expert. Generate accurate, exam-ready content following the CPRS methodology. All Azure facts must be authoritative and current."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=3000
        )
        
        result = json.loads(response.choices[0].message.content)
        result['guide_references'] = guide_refs
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "fallback": True,
            "concept": concept,
            "guide_references": guide_refs,
            "questions": []
        }), 200

@app.route('/api/user', methods=['POST'])
def create_user():
    user_id = f"user_{uuid.uuid4()}"
    return jsonify({"userId": user_id})

@app.route('/api/sync', methods=['GET'])
def get_sync():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({"error": "userId required"}), 400
    
    file_path = os.path.join(SYNC_DATA_DIR, f"{user_id}.json")
    if not os.path.exists(file_path):
        return jsonify({"found": False})
    
    try:
        with open(file_path, 'r') as f:
            sync_data = json.load(f)
        return jsonify({
            "found": True,
            "data": sync_data.get("data", {}),
            "updatedAt": sync_data.get("updatedAt", "")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sync', methods=['PUT'])
def put_sync():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user_id = data.get('userId')
    sync_data = data.get('data')
    
    if not user_id or not sync_data:
        return jsonify({"error": "userId and data required"}), 400
    
    file_path = os.path.join(SYNC_DATA_DIR, f"{user_id}.json")
    
    try:
        from datetime import datetime
        now = datetime.utcnow().isoformat() + "Z"
        with open(file_path, 'w') as f:
            json.dump({"data": sync_data, "updatedAt": now}, f)
        return jsonify({"success": True, "updatedAt": now})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    response = send_from_directory(app.static_folder, path)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
