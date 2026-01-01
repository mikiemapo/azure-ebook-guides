const GUIDE_INDEX = {
  "Azure AD": { file: "azure_ad_overview.html", section: "Azure Active Directory" },
  "Entra ID": { file: "azure_ad_overview.html", section: "Microsoft Entra ID" },
  "RBAC": { file: "azure_rbac_guide.html", section: "Role-Based Access Control" },
  "Azure Policy": { file: "azure_policy_guide.html", section: "Azure Policy" },
  "Management Groups": { file: "azure_management_groups.html", section: "Management Groups" },
  "Subscriptions": { file: "azure_subscriptions_guide.html", section: "Subscriptions" },
  "Resource Groups": { file: "azure_resource_groups.html", section: "Resource Groups" },
  "Storage Accounts": { file: "azure_storage_accounts.html", section: "Storage Accounts" },
  "Blob Storage": { file: "azure_blob_storage.html", section: "Blob Storage" },
  "Azure Files": { file: "azure_files_guide.html", section: "Azure Files" },
  "Storage Replication": { file: "azure_storage_replication.html", section: "Storage Replication" },
  "Virtual Machines": { file: "azure_vm_guide.html", section: "Virtual Machines" },
  "VM Scale Sets": { file: "azure_vmss_guide.html", section: "VM Scale Sets" },
  "Availability Sets": { file: "azure_availability_sets.html", section: "Availability Sets" },
  "Azure App Service": { file: "azure_app_service.html", section: "App Service" },
  "Azure Container Instances": { file: "azure_aci_guide.html", section: "Container Instances" },
  "Azure Kubernetes Service": { file: "azure_aks_guide.html", section: "AKS" },
  "Virtual Networks": { file: "azure_vnet_guide.html", section: "Virtual Networks" },
  "VNet Peering": { file: "azure_vnet_peering.html", section: "VNet Peering" },
  "Network Security Groups": { file: "azure_nsg_guide.html", section: "NSGs" },
  "Azure Load Balancer": { file: "azure_load_balancer.html", section: "Load Balancer" },
  "Application Gateway": { file: "azure_app_gateway.html", section: "Application Gateway" },
  "Azure DNS": { file: "azure_dns_guide.html", section: "Azure DNS" },
  "VPN Gateway": { file: "azure_vpn_gateway.html", section: "VPN Gateway" },
  "ExpressRoute": { file: "azure_expressroute.html", section: "ExpressRoute" },
  "Azure Monitor": { file: "azure_monitor_guide.html", section: "Azure Monitor" },
  "Log Analytics": { file: "azure_log_analytics.html", section: "Log Analytics" },
  "Azure Backup": { file: "azure_backup_guide.html", section: "Azure Backup" },
  "Azure Site Recovery": { file: "azure_site_recovery.html", section: "Site Recovery" },
  "Azure Alerts": { file: "azure_alerts_guide.html", section: "Alerts" }
};

const AZURE_KEYWORDS = [
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
];

function findGuideReferences(concepts) {
  const refs = [];
  for (const concept of concepts) {
    const conceptLower = concept.toLowerCase();
    for (const [key, value] of Object.entries(GUIDE_INDEX)) {
      if (key.toLowerCase().includes(conceptLower) || conceptLower.includes(key.toLowerCase())) {
        refs.push({
          concept: concept,
          guide: value.file,
          section: value.section
        });
        break;
      }
    }
  }
  return refs;
}

function extractConceptsFromText(text) {
  const found = [];
  const textLower = text.toLowerCase();
  for (const keyword of AZURE_KEYWORDS) {
    if (textLower.includes(keyword.toLowerCase())) {
      found.push(keyword);
    }
  }
  return [...new Set(found)];
}

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin || "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Content-Type": "application/json"
  };
}

async function callOpenAI(apiKey, messages, maxTokens = 2000) {
  const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "gpt-4o",
      messages: messages,
      response_format: { type: "json_object" },
      max_tokens: maxTokens
    })
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`OpenAI API error: ${response.status} - ${error}`);
  }

  const data = await response.json();
  return JSON.parse(data.choices[0].message.content);
}

async function handleExtractConcepts(request, env) {
  const origin = request.headers.get("Origin");
  
  try {
    const data = await request.json();
    if (!data || !data.text) {
      return new Response(JSON.stringify({ error: "No text provided" }), {
        status: 400,
        headers: corsHeaders(origin)
      });
    }

    const rawText = data.text;
    const localConcepts = extractConceptsFromText(rawText);
    const guideRefs = findGuideReferences(localConcepts);

    if (!env.OPENAI_API_KEY) {
      return new Response(JSON.stringify({
        fallback: true,
        fallback_reason: "OpenAI API key not configured",
        local_concepts: localConcepts,
        guide_references: guideRefs,
        concepts: [],
        summary: "AI analysis unavailable - using keyword extraction mode."
      }), { headers: corsHeaders(origin) });
    }

    const prompt = `You are an Azure certification expert using the CPRS (Concept-Pathway Reinforcement System) methodology.

Analyze the following quiz review content where the student got questions wrong.

For each concept mentioned, apply the CPRS framework:
1. FOUNDATION: What problem does this concept solve?
2. DEFINITION: Precise one-sentence definition
3. DIFFERENTIATION: How is it different from commonly confused services?
4. WHY WRONG: Why the student's answer was incorrect
5. COMPRESSION: One-sentence memory hook for instant recall
6. The AZ-104 exam objective it relates to (e.g., 1.2, 3.3)

Format your response as JSON with this structure:
{
    "concepts": [
        {
            "name": "concept name",
            "foundation": "the root purpose/problem it solves",
            "definition": "precise one-sentence definition",
            "differentiation": "how it differs from similar services",
            "correct_fact": "the accurate Azure fact",
            "why_wrong": "brief explanation of the misconception",
            "compression": "one-sentence memory hook",
            "objective": "X.X"
        }
    ],
    "summary": "A 2-3 sentence NotebookLM-ready summary using CPRS structure focusing on the weak areas"
}

Quiz review content:
${rawText.slice(0, 4000)}`;

    const result = await callOpenAI(env.OPENAI_API_KEY, [
      { role: "system", content: "You are an Azure certification expert who provides accurate, authoritative Azure facts for the AZ-104 exam. Always be precise and factual." },
      { role: "user", content: prompt }
    ]);

    const allConceptNames = result.concepts ? result.concepts.map(c => c.name) : [];
    allConceptNames.push(...localConcepts);

    result.guide_references = findGuideReferences(allConceptNames);
    result.local_concepts = localConcepts;

    return new Response(JSON.stringify(result), { headers: corsHeaders(origin) });

  } catch (e) {
    const localConcepts = [];
    return new Response(JSON.stringify({
      error: e.message,
      fallback: true,
      local_concepts: localConcepts,
      guide_references: [],
      concepts: [],
      summary: "AI analysis failed - using keyword extraction mode."
    }), { headers: corsHeaders(origin) });
  }
}

async function handleGenerateCPRS(request, env) {
  const origin = request.headers.get("Origin");

  try {
    const data = await request.json();
    if (!data || !data.concept) {
      return new Response(JSON.stringify({ error: "No concept provided" }), {
        status: 400,
        headers: corsHeaders(origin)
      });
    }

    const concept = data.concept.trim();
    if (!concept) {
      return new Response(JSON.stringify({ error: "Concept cannot be empty" }), {
        status: 400,
        headers: corsHeaders(origin)
      });
    }

    const guideRefs = findGuideReferences([concept]);

    if (!env.OPENAI_API_KEY) {
      return new Response(JSON.stringify({
        fallback: true,
        fallback_reason: "OpenAI API key not configured",
        concept: concept,
        guide_references: guideRefs,
        questions: []
      }), { headers: corsHeaders(origin) });
    }

    const prompt = `You are an Azure certification expert using the CPRS (Concept-Pathway Reinforcement System) methodology.

Generate 6 SEPARATE multiple-choice questions (MCQ) for: "${concept}"

Each question MUST have 4 options (A, B, C, D) and one correct answer.

QUESTION 1 - FOUNDATION (Root Purpose):
Test understanding of what problem ${concept} solves.
Example angle: "Which scenario best describes the primary use case for ${concept}?"

QUESTION 2 - DEFINITION (Textbook Clarity):
Test knowing the precise definition of ${concept}.
Example angle: "Which statement correctly defines ${concept}?"

QUESTION 3 - DIFFERENTIATION (Compare Similar Services):
Test distinguishing ${concept} from commonly confused Azure services.
Example angle: "A company needs [scenario]. Which service should they use: ${concept} or [similar service]?"

QUESTION 4 - SCENARIO (Exam-Style Application):
A realistic AZ-104 exam question applying ${concept} to a business scenario.
Include subtle misdirection like Microsoft uses. All options must sound plausible.

QUESTION 5 - ANTI-CONFUSION (Trap Recognition):
Test recognizing why wrong answers are wrong.
Example angle: "Which statement about ${concept} is FALSE?" or "Which scenario would NOT be appropriate for ${concept}?"

QUESTION 6 - COMPRESSION (Memory Hook):
Test the core takeaway that summarizes ${concept}.
Example angle: "Which one-sentence summary best captures the essence of ${concept}?"

Format your response as JSON with ALL 6 questions as MCQs:
{
    "concept": "${concept}",
    "questions": [
        {
            "type": "Foundation",
            "question": "the MCQ question text",
            "options": {"A": "option A", "B": "option B", "C": "option C", "D": "option D"},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        },
        {
            "type": "Definition",
            "question": "the MCQ question text",
            "options": {"A": "option A", "B": "option B", "C": "option C", "D": "option D"},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        },
        {
            "type": "Differentiation",
            "question": "the MCQ question text",
            "options": {"A": "option A", "B": "option B", "C": "option C", "D": "option D"},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        },
        {
            "type": "Scenario",
            "question": "the MCQ question text",
            "options": {"A": "option A", "B": "option B", "C": "option C", "D": "option D"},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        },
        {
            "type": "Anti-Confusion",
            "question": "the MCQ question text",
            "options": {"A": "option A", "B": "option B", "C": "option C", "D": "option D"},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        },
        {
            "type": "Compression",
            "question": "the MCQ question text",
            "options": {"A": "option A", "B": "option B", "C": "option C", "D": "option D"},
            "correct": "A/B/C/D",
            "explanation": "why this is correct"
        }
    ],
    "objective": "X.X (the AZ-104 exam objective code)"
}`;

    const result = await callOpenAI(env.OPENAI_API_KEY, [
      { role: "system", content: "You are an Azure certification expert. Generate accurate, exam-ready content following the CPRS methodology. All Azure facts must be authoritative and current." },
      { role: "user", content: prompt }
    ], 3000);

    result.guide_references = guideRefs;

    return new Response(JSON.stringify(result), { headers: corsHeaders(origin) });

  } catch (e) {
    return new Response(JSON.stringify({
      error: e.message,
      fallback: true,
      concept: "",
      guide_references: [],
      questions: []
    }), { headers: corsHeaders(origin) });
  }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin");

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(origin) });
    }

    if (url.pathname === "/api/extract-concepts" && request.method === "POST") {
      return handleExtractConcepts(request, env);
    }

    if (url.pathname === "/api/generate-cprs" && request.method === "POST") {
      return handleGenerateCPRS(request, env);
    }

    return new Response(JSON.stringify({
      status: "AZ-104 Study Hub API",
      endpoints: ["/api/extract-concepts", "/api/generate-cprs"]
    }), { headers: corsHeaders(origin) });
  }
};
