#!/usr/bin/env python3
"""
Generate AZ104_Compute_Decision_DeepDive.csv from transcript
20 CPRS questions on IaaS vs PaaS vs Serverless decision frameworks
"""
import csv
import os

OUTPUT_DIR = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/AZ-104-Critical-Priorities-Study-Deck/Topic-Based-Decks"

def generate_compute_decision_questions():
    """20 CPRS Compute Decision questions"""
    return [
        ("What is the fundamental difference between IaaS (VMs) and PaaS (App Service) regarding resource management?",
         "Both are identical cloud models","IaaS = you manage VM/OS/runtime (control). PaaS = Azure manages OS/runtime, you manage code (simplicity)","IaaS is cheaper than PaaS","PaaS only works for web apps","B","IaaS = Infrastructure as a Service (control). PaaS = Platform as a Service (simplicity). Trade-off: IaaS flexibility vs PaaS ease. Choose based on control requirements.","Compute,IaaS,PaaS,Decision"),
        
        ("When should you choose IaaS (VMs) over PaaS (App Service)?",
         "Always choose IaaS for better performance","Need OS-level control (kernel tuning, custom drivers) or non-standard runtime stacks not in Azure PaaS","PaaS is always more expensive","IaaS is for databases only","B","IaaS wins when: custom OS config, exotic dependencies, legacy applications. App Service forces Azure runtime ecosystem; non-standard apps = VMs needed.","IaaS,Control,CustomOS"),
        
        ("Your app: standard Node.js + PostgreSQL on Linux. IaaS or PaaS?",
         "IaaS (more control)","PaaS (App Service Linux with PostgreSQL) = simpler, cheaper, Azure patches OS/runtime","Both equally suitable","Serverless only","B","Standard tech stacks = PaaS sweet spot. App Service Linux supports Node natively. Azure patches OS/runtime. Cheaper TCO than VMs. PaaS wins; save IaaS for non-standard workloads.","PaaS,StandardStack,Decision"),
        
        ("Critical: .NET Framework 4.8 app deployment. What's the HARD constraint?",
         "Both IaaS and PaaS work equally",".NET Framework = Windows-only at platform level. PaaS = Windows plan required (automatic OS). IaaS = manual Windows VM setup.","Linux plan option exists","Framework support is coming to Linux","B",".NET Framework is Windows-exclusive (no Linux). PaaS Windows plan = automatic OS management. IaaS Windows VM = manual setup. PaaS simpler for Framework. For .NET 5+, use PaaS Linux.","PaaS,OSConstraint,Framework"),
        
        ("Why can't you deploy .NET Framework app to Linux App Service plan?",
         "It's a cost restriction",".NET Framework (pre-.NET 5) is Windows-exclusive; Linux incompatibility is absolute; OS choice is immutable after plan creation","Requires containerization workaround","Linux support coming soon","B","OS choice is HARD constraint on PaaS (immutable after creation). .NET Framework needs Windows. Create wrong plan = deployment blocked. Workaround: Docker + Linux to containerize Framework app.","PaaS,OSImmutable,Framework"),
        
        ("You have custom C++ library dependency for your app. Code deploy or Docker?",
         "Code deploy (App Service includes it)","Docker (package entire environment with custom library in container image; code deploy relies on Azure standard runtime stack)","Custom OS image on VMs","Both work equally","B","Code deployment = rely on Azure's pre-built runtime stacks (standard libraries only). Non-standard dependencies = Docker required. Build locally with all deps, push to ACR, deploy. Docker = total portability.","PaaS,Docker,Dependencies"),
        
        ("Two apps (e-commerce + reporting batch) on same App Service plan. Black Friday spike: what happens?",
         "Both continue unaffected (isolated)","Reporting starves for CPU (resource contention on shared plan; spike consumes 95% = batch timeout)","System auto-scales reporting to separate plan","Plan throttles e-commerce to fairness","B","Sharing a plan = cost efficiency but contention risk. Both apps fight for CPU/RAM. Spike starves other app. Solution: separate plans by performance criticality.","PaaS,ResourceContention,Planning"),
        
        ("When is Serverless (Functions) the right choice over VMs or App Service?",
         "Never; serverless is marketing",". Sporadic event-driven workloads (file upload triggers processing); billed per execution; scale 0 when idle","Serverless is cheaper for 24/7 workloads","Serverless works for databases","B","Serverless = event-driven + scale-to-zero. Perfect for file processors, webhooks, scheduled tasks. NOT for 24/7 (costs skyrocket). Cost = execution count + memory-time.","Serverless,Functions,EventDriven"),
        
        ("Multi-container app (API + Redis + PostgreSQL). Deploy on Azure where?",
         "App Service (all containers)","Azure Kubernetes Service (AKS) for full orchestration (service discovery, auto-scaling, rolling updates, multi-container management)","Single App Service plan with compose","Individual VMs per container","B","App Service limited to single-container. Multi-service = AKS (orchestration, networking, scaling). AKS handles lifecycle. App Service = simpler for single container.","Containers,AKS,Orchestration"),
        
        ("App needs 10→10,000 requests/sec. Manual VMs, App Service autoscale, or AKS?",
         "Manual VMs (provision new ones)","App Service autoscale (monitor CPU/memory; spin instances on demand) or AKS (pod auto-scaling); both eliminate manual ops","App Service can't handle that","Manual VM scaling fastest","B","Autoscaling eliminates manual ops. App Service scales plan instances (horizontal). AKS scales pods. Both detect load, provision capacity, clean up demand drops.","Scaling,Autoscale,Operations"),
        
        ("POC: small app, uncertain traffic, 3-month experiment. Minimize cost strategy?",
         "Premium IaaS high SKU","App Service Free tier (free plan, shared hardware, 1GB disk, zero cost for POC; perfect for experiments)","AKS cluster (minimum cost)","Serverless Functions (always cheaper)","B","Free tier = zero cost experimentation. Shared hardware acceptable for POC. Graduate to Shared/Basic/Standard when hitting limits. Free tier strategic for risk-free onboarding.","CostOptimization,POC,AppService"),
        
        ("Web app must connect to private database inside VNet. Which compute + tier?",
         "App Service Free tier","App Service Standard+ tier with VNet integration (Free/Shared/Basic don't support VNet)","Any tier supports VNet","Functions don't support VNet","B","VNet integration = Standard minimum tier requirement. Feature locked to paid tiers. Ensure plan and VNet in same region. Private DB access = app needs network path.","VNet,AppService,Networking"),
        
        ("On-prem legacy app + cloud expansion. Which Azure compute bridges hybrid?",
         "App Service alone","VMs in Azure (direct parity with on-prem; network through VPN/Express Route; migrate incrementally)","Serverless Functions","Only containerization works","B","Hybrid cloud = VMs bridge legacy + cloud. Create Azure VMs with same OS/config as on-prem, use site-to-site VPN. App Service/AKS = cloud-first (requires refactor). VMs = lift-and-shift.","Hybrid,VMs,Migration"),
        
        ("Golden Rule of App Service scaling: what do you scale—the plan or apps?",
         "Individual applications","The App Service plan (compute block); plan = billing unit providing CPU/RAM; apps are tenants on it","The runtime stack","The container registry","B","GOLDEN RULE: Plan = compute boundary. Apps don't scale independently; plan scales. Resize plan SKU (Basic→Standard→Premium). Scale plan, not app. Forget this = phantom performance issues.","PaaS,Scaling,Concept"),
        
        ("Use this decision tree: IaaS if ____ control. PaaS if ____ stack. Serverless if ____ workload.",
         "OS; app; periodic","OS-level; standard runtime; event-driven","standard; custom; 24/7","database; security; scheduled","B","Decision Tree: IaaS (OS control) = custom kernel/drivers/legacy. PaaS (standard runtime) = Node/Python/.NET in Azure ecosystem. Serverless (event-driven) = webhooks/uploads/tasks. Mnemonic: 'Control vs Convenience vs Hands-off'.","Decision,Mnemonic,Compute"),
        
        ("EXAM TRAP: VNet-integrated app deployed to App Service Free tier. What happens?",
         "Deployment succeeds; VNet works fine","Deployment fails; VNet integration NOT available on Free/Shared/Basic tiers","Free tier auto-upgrades to Standard","Add VNet after deployment (free)","B","Tier Lock Trap: Feature availability tier-dependent. Free = no VNet integration. Attempting integration = error. Must provision Standard+ first. Catches exam takers forgetting tier constraints.","PaaS,Tier,ExamTrap"),
        
        ("EXAM TRAP: Create Windows App Service plan, then realize app only runs on Linux. Cost of fixing?",
         "Flip OS setting (free)","Delete plan, create new Linux plan, redeploy (old plan unusable; OS immutable at creation; costs: new plan, downtime, IP changes, DNS updates)","Migrate within same plan (free)","Use scripts to change OS","B","OS Immutability Trap: Plan OS locked at creation. Windows = Windows forever. Cannot change to Linux without new plan. Costs: new plan, downtime, IP changes, DNS updates. Know OS requirements before creating.","PaaS,OSImmutable,ExamTrap"),
        
        ("Complex decision: 24/7 web app + scheduled batch + real-time API. Compute mix?",
         "Single VMs for everything","App Service (24/7 web + API) + Serverless Functions (scheduled batch); hybrid approach matching workload characteristics","AKS only","Serverless for all","B","Mixed workloads = mixed compute. 24/7 API = App Service (always-on cost). Scheduled batch = Serverless (pay per execution). Use right tool per job. App Service API + Function scheduler = cost-optimal.","Compute,Architecture,Decision"),
        
        ("What separates a competent architect from a mid-level engineer in compute decisions?",
         "Architects use more expensive resources","Competent architects model TCO (3-year total cost) across IaaS/PaaS/Serverless mixes. Mid-level thinks single-service. Architect thinks 'right tool per workload component'.","Architects always recommend PaaS","Architects avoid Serverless","B","Architectural maturity: Single-service thinking = trap. Multi-service architecture (App Service + Functions + VMs) = right tool per component. Competent architect models 3-year TCO, not just upfront.","Architecture,Maturity,Decision"),
    ]

def write_csv(output_file, questions, batch_name):
    """Write CSV in Anki format"""
    output_path = os.path.join(OUTPUT_DIR, output_file)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'ChoiceA', 'ChoiceB', 'ChoiceC', 'ChoiceD', 'Correct', 'Explanation', 'Tags', 'Source', 'Batch'])
        
        for q, ca, cb, cc, cd, correct, expl, tags in questions:
            writer.writerow([q, ca, cb, cc, cd, correct, expl, tags, "Deep Dive Transcript", batch_name])
    
    print(f"✅ {output_file} ({len(questions)} questions)")

# Generate
qs = generate_compute_decision_questions()
write_csv("AZ104_Compute_Decision_DeepDive.csv", qs, "Compute Decision Deep Dive Batch")
print(f"✨ Done!")
