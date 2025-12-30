import os
import json
import re
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user

app = Flask(__name__, static_folder='docs')
CORS(app)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

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
        prompt = f"""You are an Azure certification expert. Analyze the following quiz review content where the student got questions wrong.

For each concept mentioned, provide:
1. The correct Azure fact (authoritative, accurate)
2. A brief explanation of why the wrong answer was incorrect
3. The AZ-104 exam objective it relates to (e.g., 1.2, 3.3)

Format your response as JSON with this structure:
{{
    "concepts": [
        {{
            "name": "concept name",
            "correct_fact": "the accurate Azure fact",
            "why_wrong": "brief explanation of the misconception",
            "objective": "X.X"
        }}
    ],
    "summary": "A 2-3 sentence NotebookLM-ready summary focusing on the weak areas"
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
