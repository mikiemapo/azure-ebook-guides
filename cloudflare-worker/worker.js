const AZ104_OBJECTIVES = {
  domains: [
    {
      id: "1",
      name: "Manage Azure Identities and Governance",
      weight: "20-25%",
      objectives: [
        { id: "1.1", name: "Manage Microsoft Entra users and groups", skills: ["Create users and groups", "Manage user and group properties", "Manage licenses in Microsoft Entra ID", "Manage external users", "Configure self-service password reset (SSPR)"] },
        { id: "1.2", name: "Manage access to Azure resources", skills: ["Manage built-in Azure roles", "Assign roles at different scopes", "Interpret access assignments"] },
        { id: "1.3", name: "Manage Azure subscriptions and governance", skills: ["Implement and manage Azure Policy", "Configure resource locks", "Apply and manage tags on resources", "Manage resource groups", "Manage subscriptions", "Manage costs by using alerts, budgets, and Azure Advisor recommendations", "Configure management groups"] }
      ]
    },
    {
      id: "2",
      name: "Implement and Manage Storage",
      weight: "15-20%",
      objectives: [
        { id: "2.1", name: "Configure access to storage", skills: ["Configure Azure Storage firewalls and virtual networks", "Create and use shared access signature (SAS) tokens", "Configure stored access policies", "Manage access keys", "Configure identity-based access for Azure Files"] },
        { id: "2.2", name: "Configure and manage storage accounts", skills: ["Create and configure storage accounts", "Configure Azure Storage redundancy", "Configure object replication", "Configure storage account encryption", "Manage data by using Azure Storage Explorer and AzCopy"] },
        { id: "2.3", name: "Configure Azure Files and Azure Blob Storage", skills: ["Create and configure a file share in Azure Storage", "Create and configure a container in Blob Storage", "Configure storage tiers", "Configure soft delete for blobs and containers", "Configure snapshots and soft delete for Azure Files", "Configure blob lifecycle management", "Configure blob versioning"] }
      ]
    },
    {
      id: "3",
      name: "Deploy and Manage Azure Compute Resources",
      weight: "20-25%",
      objectives: [
        { id: "3.1", name: "Automate deployment of resources by using ARM templates or Bicep files", skills: ["Interpret an Azure Resource Manager template or a Bicep file", "Modify an existing Azure Resource Manager template", "Modify an existing Bicep file", "Deploy resources by using an Azure Resource Manager template or a Bicep file", "Export a deployment as an Azure Resource Manager template or convert an Azure Resource Manager template to a Bicep file"] },
        { id: "3.2", name: "Create and configure virtual machines", skills: ["Create a virtual machine", "Configure Azure Disk Encryption", "Move a virtual machine to another resource group, subscription, or region", "Manage virtual machine sizes", "Manage virtual machine disks", "Deploy virtual machines to availability zones and availability sets", "Deploy and configure an Azure Virtual Machine Scale Sets"] },
        { id: "3.3", name: "Provision and manage containers in the Azure portal", skills: ["Create and manage an Azure container registry", "Provision a container by using Azure Container Instances", "Provision a container by using Azure Container Apps", "Manage sizing and scaling for containers, including Azure Container Instances and Azure Container Apps"] },
        { id: "3.4", name: "Create and configure Azure App Service", skills: ["Provision an App Service plan", "Configure scaling for an App Service plan", "Create an App Service", "Configure certificates and Transport Layer Security (TLS) for an App Service", "Map an existing custom DNS name to an App Service", "Configure backup for an App Service", "Configure networking settings for an App Service", "Configure deployment slots for an App Service"] }
      ]
    },
    {
      id: "4",
      name: "Implement and Manage Virtual Networking",
      weight: "15-20%",
      objectives: [
        { id: "4.1", name: "Configure and manage virtual networks in Azure", skills: ["Create and configure virtual networks and subnets", "Create and configure virtual network peering", "Configure public IP addresses", "Configure user-defined network routes", "Troubleshoot network connectivity"] },
        { id: "4.2", name: "Configure secure access to virtual networks", skills: ["Create and configure network security groups (NSGs) and application security groups", "Evaluate effective security rules in NSGs", "Implement Azure Bastion", "Configure service endpoints for Azure platform as a service (PaaS)", "Configure private endpoints for Azure PaaS"] },
        { id: "4.3", name: "Configure name resolution and load balancing", skills: ["Configure Azure DNS", "Configure an internal or public load balancer", "Troubleshoot load balancing"] }
      ]
    },
    {
      id: "5",
      name: "Monitor and Maintain Azure Resources",
      weight: "10-15%",
      objectives: [
        { id: "5.1", name: "Monitor resources by using Azure Monitor", skills: ["Configure and interpret metrics", "Configure Azure Monitor Logs", "Query and analyze logs", "Set up alerts and actions", "Configure monitoring of VMs, storage accounts, and networks by using VM insights"] },
        { id: "5.2", name: "Implement backup and recovery", skills: ["Create an Azure Recovery Services vault", "Create an Azure Backup vault", "Create and configure backup policy", "Perform backup and restore operations by using Azure Backup", "Configure Azure Site Recovery for Azure resources", "Perform failover to a secondary region by using Azure Site Recovery", "Configure and review backup reports"] }
      ]
    }
  ]
};

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
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Content-Type": "application/json"
  };
}

function generateCacheKey(concept) {
  return `cprs:${concept.toLowerCase().trim().replace(/\s+/g, '-')}`;
}

function generateUserId() {
  return 'user_' + crypto.randomUUID();
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
<<<<<<< HEAD
${rawText.slice(0, 4000)}`;
=======
${rawText.slice(0, 16000)}`;

    // Generate specific cache key for this text content
    const textHash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(rawText.slice(0, 1000))); // Hash first 1000 chars as proxy or hash all
    const hashArray = Array.from(new Uint8Array(textHash));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    const cacheKey = `concepts:text:${hashHex}`;

    if (env.CPRS_CACHE) {
      const cached = await env.CPRS_CACHE.get(cacheKey, { type: "json" });
      if (cached) {
        return new Response(JSON.stringify({ ...cached, cached: true }), { headers: corsHeaders(origin) });
      }
    }
>>>>>>> 8018936 (feat(sync): Migrate to Firebase and fix Worker limits)

    const result = await callOpenAI(env.OPENAI_API_KEY, [
      { role: "system", content: "You are an Azure certification expert who provides accurate, authoritative Azure facts for the AZ-104 exam. Always be precise and factual." },
      { role: "user", content: prompt }
    ]);

<<<<<<< HEAD
=======

>>>>>>> 8018936 (feat(sync): Migrate to Firebase and fix Worker limits)
    const allConceptNames = result.concepts ? result.concepts.map(c => c.name) : [];
    allConceptNames.push(...localConcepts);

    result.guide_references = findGuideReferences(allConceptNames);
    result.local_concepts = localConcepts;

<<<<<<< HEAD
=======
    if (env.CPRS_CACHE) {
      await env.CPRS_CACHE.put(cacheKey, JSON.stringify(result), { expirationTtl: 60 * 60 * 24 * 7 }); // Cache for 7 days
    }

>>>>>>> 8018936 (feat(sync): Migrate to Firebase and fix Worker limits)
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

    if (env.CPRS_CACHE) {
      const cacheKey = generateCacheKey(concept);
      const cached = await env.CPRS_CACHE.get(cacheKey, { type: "json" });
      if (cached) {
        cached.cached = true;
        cached.guide_references = guideRefs;
        return new Response(JSON.stringify(cached), { headers: corsHeaders(origin) });
      }
    }

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

    if (env.CPRS_CACHE) {
      const cacheKey = generateCacheKey(concept);
      await env.CPRS_CACHE.put(cacheKey, JSON.stringify(result), { expirationTtl: 60 * 60 * 24 * 30 });
    }

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

async function handleSyncGet(request, env) {
  const origin = request.headers.get("Origin");
  const url = new URL(request.url);
  const userId = url.searchParams.get("userId");

  if (!userId) {
    return new Response(JSON.stringify({ error: "userId required" }), {
      status: 400,
      headers: corsHeaders(origin)
    });
  }

  if (!env.DB) {
    return new Response(JSON.stringify({ error: "Database not configured" }), {
      status: 503,
      headers: corsHeaders(origin)
    });
  }

  try {
    const result = await env.DB.prepare(
      "SELECT data, updated_at FROM user_scores WHERE user_id = ?"
    ).bind(userId).first();

    if (!result) {
      return new Response(JSON.stringify({ found: false }), { headers: corsHeaders(origin) });
    }

    return new Response(JSON.stringify({
      found: true,
      data: JSON.parse(result.data),
      updatedAt: result.updated_at
    }), { headers: corsHeaders(origin) });

  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: corsHeaders(origin)
    });
  }
}

async function handleSyncPut(request, env) {
  const origin = request.headers.get("Origin");

  try {
    const body = await request.json();
    const { userId, data } = body;

    if (!userId || !data) {
      return new Response(JSON.stringify({ error: "userId and data required" }), {
        status: 400,
        headers: corsHeaders(origin)
      });
    }

    if (!env.DB) {
      return new Response(JSON.stringify({ error: "Database not configured" }), {
        status: 503,
        headers: corsHeaders(origin)
      });
    }

    const now = new Date().toISOString();
    await env.DB.prepare(
      `INSERT INTO user_scores (user_id, data, updated_at) 
       VALUES (?, ?, ?) 
       ON CONFLICT(user_id) DO UPDATE SET data = excluded.data, updated_at = excluded.updated_at`
    ).bind(userId, JSON.stringify(data), now).run();

    return new Response(JSON.stringify({ success: true, updatedAt: now }), { headers: corsHeaders(origin) });

  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: corsHeaders(origin)
    });
  }
}

async function handleCreateUser(request, env) {
  const origin = request.headers.get("Origin");
  const userId = generateUserId();

  return new Response(JSON.stringify({ userId }), { headers: corsHeaders(origin) });
}

async function handleGetAnkiDeck(request, env) {
  const origin = request.headers.get("Origin");
  const url = new URL(request.url);
  const deckName = url.pathname.replace("/api/anki-decks/", "");

  if (!deckName) {
    return new Response(JSON.stringify({ error: "Deck name required" }), {
      status: 400,
      headers: corsHeaders(origin)
    });
  }

  if (!env.ANKI_DECKS) {
    return new Response(JSON.stringify({ error: "R2 storage not configured" }), {
      status: 503,
      headers: corsHeaders(origin)
    });
  }

  try {
    const object = await env.ANKI_DECKS.get(deckName);
    
    if (!object) {
      return new Response(JSON.stringify({ error: "Deck not found" }), {
        status: 404,
        headers: corsHeaders(origin)
      });
    }

    return new Response(object.body, {
      headers: {
        "Content-Type": "application/octet-stream",
        "Content-Disposition": `attachment; filename="${deckName}"`,
        "Access-Control-Allow-Origin": origin || "*"
      }
    });

  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: corsHeaders(origin)
    });
  }
}

async function handleListAnkiDecks(request, env) {
  const origin = request.headers.get("Origin");

  if (!env.ANKI_DECKS) {
    return new Response(JSON.stringify({ error: "R2 storage not configured" }), {
      status: 503,
      headers: corsHeaders(origin)
    });
  }

  try {
    const listed = await env.ANKI_DECKS.list();
    const decks = listed.objects.map(obj => ({
      name: obj.key,
      size: obj.size,
      uploaded: obj.uploaded
    }));

    return new Response(JSON.stringify({ decks }), { headers: corsHeaders(origin) });

  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: corsHeaders(origin)
    });
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

    if (url.pathname === "/api/sync" && request.method === "GET") {
      return handleSyncGet(request, env);
    }

    if (url.pathname === "/api/sync" && request.method === "PUT") {
      return handleSyncPut(request, env);
    }

    if (url.pathname === "/api/user" && request.method === "POST") {
      return handleCreateUser(request, env);
    }

    if (url.pathname === "/api/anki-decks" && request.method === "GET") {
      return handleListAnkiDecks(request, env);
    }

    if (url.pathname.startsWith("/api/anki-decks/") && request.method === "GET") {
      return handleGetAnkiDeck(request, env);
    }

    return new Response(JSON.stringify({
      status: "AZ-104 Study Hub API",
      version: "2.0",
      endpoints: [
        "POST /api/extract-concepts",
        "POST /api/generate-cprs",
        "GET /api/sync?userId=xxx",
        "PUT /api/sync",
        "POST /api/user",
        "GET /api/anki-decks",
        "GET /api/anki-decks/:name"
      ],
      features: {
        kvCaching: !!env.CPRS_CACHE,
        d1Database: !!env.DB,
        r2Storage: !!env.ANKI_DECKS
      }
    }), { headers: corsHeaders(origin) });
  }
};
