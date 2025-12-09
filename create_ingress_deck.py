#!/usr/bin/env python3
"""
Generate Container Apps Ingress DeepDive Deck
Matches AZ-104 Master Deck styling (#4CAF50 green, .choice CSS)
"""
import genanki

# Match exact model from create_master_deck.py
ingress_model = genanki.Model(
    1607392321,
    'Container Apps Ingress DeepDive Model',
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
    2091607891,
    'AZ-104 Study Guide::Deep Dive Segments::Container Apps Ingress'
)

def create_ingress_deck():
    # (Question, ChoiceA, ChoiceB, ChoiceC, ChoiceD, Correct, Explanation, Tags)
    questions = [
        ("GOLDEN RULE: The fundamental security principle of Azure Container Apps Ingress is:",
         "Internal apps automatically get external endpoints after 24 hours",
         "Ingress only exposes what you explicitly allow—Azure defaults to total denial",
         "Always enable external access for production apps",
         "Configure firewalls manually after deployment",
         "B",
         "Ingress only exposes what you explicitly allow—Azure defaults to total denial. The 'gated community' analogy: your environment is completely sealed by default, nothing reaches the outside world unless you affirmatively open that gate.",
         "Container_Apps,Ingress,Security,Deep_Dive"),
        
        ("What does 'Ingress = Internal Only' (or Ingress disabled) mean for a Container App?",
         "App requires VPN connection for all access",
         "App is only visible within the Container Apps environment—not reachable from internet, laptop, or different VNet",
         "App automatically scales based on internal traffic",
         "App is accessible from the internet with limited bandwidth",
         "B",
         "Internal Only means only 'neighbors' (other apps in same environment) can reach it. Cannot be reached from internet, your laptop, or even a VM in a different VNet—this isolation is a feature, not a bug.",
         "Container_Apps,Ingress,Networking,Deep_Dive"),
        
        ("The 'gated community' analogy for Container Apps environments means:",
         "External access requires purchasing additional licenses",
         "The environment is a high-security sealed boundary where apps are isolated by default unless Ingress is configured",
         "All apps share the same IP address",
         "Apps can only run in premium Azure regions",
         "B",
         "The entire Container Apps environment is like a high-security, completely sealed gated community where each app is a 'house'. Gates are locked shut by default—forces conscious security decisions and prevents accidental exposure.",
         "Container_Apps,Ingress,Security,Concepts,Deep_Dive"),
        
        ("What are the three core modes of Azure Container Apps Ingress configuration?",
         "Basic, Standard, Premium",
         "Public, Private, Hybrid",
         "Off/Internal Only, External Limited, External Anywhere",
         "Internal Only, External Limited, External Full",
         "C",
         "Three modes: Ingress Off (Internal Only) = app only visible within environment. External Limited = exposed to internet with restrictions. External Anywhere = full public access. Each mode controls who can reach your container.",
         "Container_Apps,Ingress,Configuration,Deep_Dive"),
        
        ("A microservice backend API should NEVER be hit from the public internet and only needs to serve other services in the same environment. Which Ingress mode?",
         "Hybrid mode with VPN",
         "Internal Only (Ingress disabled)",
         "External Limited mode",
         "External with IP restrictions",
         "B",
         "Internal Only mode is ideal for internal microservices, API-to-API calls, and backend workers. Keeps internal ecosystem secure and private—enforces zero-trust principles at infrastructure level.",
         "Container_Apps,Ingress,Architecture,Deep_Dive"),
        
        ("A Container App with Internal Only Ingress cannot be reached from your laptop. What should you check first?",
         "Restart the Container App to refresh network settings",
         "This is expected behavior—Internal Only apps are intentionally isolated and only accessible from within the Container Apps environment",
         "Check if the app service plan has enough capacity",
         "DNS configuration and firewall rules",
         "B",
         "This isolation is a feature, not a bug. Internal Only means only accessible within the environment—cannot hit from internet, laptop, or VM in different VNet. To enable external access, change Ingress to External mode.",
         "Container_Apps,Ingress,Troubleshooting,Deep_Dive"),
        
        ("Can you reach an Internal Only Container App from a VM in the same VNet but different Container Apps environment?",
         "Yes, after configuring VNet peering",
         "No—Internal Only means accessible only within the Container Apps environment boundary, not just the VNet",
         "Yes, but only with NSG rules configured",
         "Yes, as long as they're in the same VNet",
         "B",
         "No. Internal Only = accessible only within the environment boundary, not just VNet. Environment provides additional isolation beyond network topology—even same VNet but different environments are isolated unless External Ingress configured.",
         "Container_Apps,Ingress,Networking,Deep_Dive"),
        
        ("Why does Azure Container Apps use a 'deny by default' security model for Ingress?",
         "To improve application performance",
         "To minimize attack surface and prevent accidental exposure of internal services—forces conscious security decisions",
         "To comply with government regulations",
         "To reduce Azure infrastructure costs",
         "B",
         "Deny by default minimizes attack surface and prevents accidental exposure. Must explicitly enable external access, forcing conscious security decisions—prevents services from being unintentionally exposed to internet. Aligns with zero-trust architecture.",
         "Container_Apps,Ingress,Security,Deep_Dive"),
        
        ("What happens if you don't configure Ingress for a Container App?",
         "Azure enables basic HTTP access by default",
         "The app remains completely isolated—accessible only to other apps within the same Container Apps environment",
         "The app cannot start and shows an error",
         "Azure automatically assigns a public IP after 1 hour",
         "B",
         "App remains completely isolated—accessible only to other apps within same environment. No external traffic (internet, other VNets, local machine) can reach it. This is Azure's locked-down default posture.",
         "Container_Apps,Ingress,Configuration,Deep_Dive"),
        
        ("What level of network isolation exists between Container Apps environments?",
         "Isolation requires manual NSG configuration",
         "Complete isolation by default—apps in different environments cannot communicate unless External Ingress is configured",
         "Isolation only applies across different Azure regions",
         "None—apps in different environments can communicate freely if in the same VNet",
         "B",
         "Complete isolation by default. Apps in different environments cannot communicate unless you explicitly configure External Ingress and routing. Each environment is its own 'gated community'—true even if in same VNet.",
         "Container_Apps,Ingress,Networking,Deep_Dive"),
        
        ("Can a Container App with Internal Only Ingress communicate with other Container Apps in the same environment?",
         "Only with service mesh configuration",
         "Yes—apps within the same environment can communicate like neighbors in a gated community",
         "Only if they're in the same subnet",
         "No—Internal Only means completely isolated",
         "B",
         "Yes—Internal Only apps can communicate with other apps inside same environment. Like houses in gated community: residents can visit each other, but gates keep everyone else out. Enables secure internal microservices architecture.",
         "Container_Apps,Ingress,Networking,Deep_Dive"),
        
        ("What is a common architecture pattern using Internal Only Ingress?",
         "All services use Internal Only and access via VPN",
         "Frontend apps use External Ingress to serve users, backend services use Internal Only for service-to-service communication",
         "Database and APIs use External with firewall rules",
         "All services use External Ingress for simplicity",
         "B",
         "Backend microservices architecture: Frontend apps use External Ingress to serve users, while backend services (databases, APIs, workers) use Internal Only for service-to-service communication within environment. Minimizes attack surface while maintaining functionality.",
         "Container_Apps,Ingress,Architecture,Deep_Dive"),
        
        ("What is the difference between a Container Apps environment and a VNet in terms of isolation?",
         "Environment is only for billing purposes",
         "A Container Apps environment is a logical managed boundary (gated community); VNet is underlying infrastructure—environment provides additional isolation beyond VNet",
         "VNet provides stronger isolation than environment",
         "They provide the same level of isolation",
         "B",
         "Container Apps environment is a logical, managed boundary (gated community). VNet is underlying infrastructure. Even if apps in same VNet but different environments, they're isolated unless Ingress configured—environment provides additional isolation beyond network topology.",
         "Container_Apps,Networking,Architecture,Deep_Dive"),
        
        ("What happens when you enable External Ingress on a Container App?",
         "Azure automatically adds DDoS protection and WAF",
         "Azure provisions external endpoints and routing infrastructure, making the app accessible from outside the environment based on configuration",
         "The app requires manual DNS configuration before it's accessible",
         "The app is immediately exposed to all internet traffic without controls",
         "B",
         "Azure provisions external endpoints and routing infrastructure, making app accessible from outside the environment. Traffic can now reach it from internet, other VNets, or local machine—depending on specific Ingress configuration (Limited vs Anywhere).",
         "Container_Apps,Ingress,Configuration,Deep_Dive"),
        
        ("What Ingress mode would you use for a public-facing web API that needs internet access?",
         "Internal Only with Application Gateway",
         "External Ingress with 'Accepting traffic from anywhere' mode",
         "Hybrid mode with VPN gateway",
         "Internal Only with port forwarding",
         "B",
         "External Ingress with 'Accepting traffic from anywhere' mode. Exposes API to internet while maintaining Azure's security controls and allowing proper routing configuration. Configure appropriate ports and ensure app is listening correctly.",
         "Container_Apps,Ingress,Architecture,Deep_Dive"),
        
        ("How does Container Apps Ingress support zero-trust architecture?",
         "By logging all access attempts",
         "By defaulting to deny-all and requiring explicit allow rules—every service starts isolated, you consciously decide what to expose",
         "By requiring multi-factor authentication",
         "By automatically encrypting all traffic",
         "B",
         "By defaulting to deny-all and requiring explicit allow rules. Every service starts isolated, you consciously decide what to expose. Aligns with zero-trust principles of 'never trust, always verify'—no app accessible from outside unless External Ingress enabled.",
         "Container_Apps,Security,Zero-Trust,Deep_Dive"),
        
        ("AZ-104 EXAM: A Container App isn't reachable from Azure Portal. What's the most likely cause?",
         "DNS propagation hasn't completed",
         "Ingress is set to Internal Only or disabled—Azure Portal runs outside the Container Apps environment and requires External Ingress",
         "The app doesn't have enough memory allocated",
         "The app is deployed in the wrong region",
         "B",
         "Most likely Ingress is Internal Only or disabled. Azure Portal access requires External Ingress since portal runs outside the environment. Check Ingress configuration first before troubleshooting other issues—common exam trap.",
         "Container_Apps,Ingress,Troubleshooting,Exam,Deep_Dive"),
        
        ("AZ-104 EXAM: You need to secure a backend API so only other services in the environment can call it. How?",
         "Configure NSG rules to block external traffic",
         "Set Ingress to Internal Only (or disable Ingress)",
         "Use Azure Front Door with WAF",
         "Enable External Ingress with IP whitelist",
         "B",
         "Set Ingress to Internal Only (or disable Ingress). Ensures API only accessible to other Container Apps within same environment, preventing any external access including from other VNets. Simplest and most secure approach for internal microservices.",
         "Container_Apps,Ingress,Security,Exam,Deep_Dive"),
        
        ("AZ-104 EXAM: How do you expose a Container App to the internet for public access?",
         "Use Azure Load Balancer with public frontend",
         "Enable External Ingress and set to 'Accepting traffic from anywhere', configure appropriate port",
         "Create a public IP and attach to the environment",
         "Deploy to a public VNet",
         "B",
         "Enable External Ingress and set to 'Accepting traffic from anywhere'. Configure appropriate port and ensure app is listening on that port. Azure will provision public endpoints and routing automatically—standard approach for exposing Container Apps publicly.",
         "Container_Apps,Ingress,Configuration,Exam,Deep_Dive"),
        
        ("What does 'deny by default' mean in Container Apps Ingress context?",
         "Deployment is denied if quotas are exceeded",
         "All inbound traffic is blocked unless explicitly allowed through Ingress configuration—no app is accessible from outside its environment by default",
         "Azure denies access from suspicious IP addresses automatically",
         "Azure denies the first deployment until you verify ownership",
         "B",
         "All inbound traffic is blocked unless explicitly allowed through Ingress configuration. No app accessible from outside environment unless you intentionally enable External Ingress. Azure's locked-down security posture that forces conscious decisions about exposure.",
         "Container_Apps,Security,Ingress,Deep_Dive"),
    ]
    
    for q in questions:
        question_text, choice_a, choice_b, choice_c, choice_d, correct, explanation, tags = q
        
        # Front side - no highlighting
        full_question = "{}<br><br><div class=\"choice\">A) {}</div><div class=\"choice\">B) {}</div><div class=\"choice\">C) {}</div><div class=\"choice\">D) {}</div>".format(
            question_text, choice_a, choice_b, choice_c, choice_d)

        # Back side - with highlighting
        choice_a_class = "choice correct" if correct == "A" else "choice"
        choice_b_class = "choice correct" if correct == "B" else "choice"
        choice_c_class = "choice correct" if correct == "C" else "choice"
        choice_d_class = "choice correct" if correct == "D" else "choice"
        
        question_with_answer = "{}<br><br><div class=\"{}\">A) {}</div><div class=\"{}\">B) {}</div><div class=\"{}\">C) {}</div><div class=\"{}\">D) {}</div>".format(
            question_text, choice_a_class, choice_a, choice_b_class, choice_b, choice_c_class, choice_c, choice_d_class, choice_d)

        answer = "Correct: {} - {}".format(correct, explanation)
        
        note = genanki.Note(
            model=ingress_model,
            fields=[full_question, question_with_answer, answer, tags]
        )
        deck.add_note(note)
    
    output_file = "/Users/mike1macbook/Documents/MY STUFF DOCS AND ALL/EBOOK/AZ-104-Critical-Priorities-Study-Deck/Topic-Based-Decks/AZ104_Container_Apps_Ingress_DeepDive.apkg"
    genanki.Package([deck]).write_to_file(output_file)
    
    print(f"✅ Created Container Apps Ingress DeepDive deck")
    print(f"📂 Location: {output_file}")
    print(f"📊 Total cards: {len(questions)} MCQ questions")
    print(f"🎨 Styling: #4CAF50 green (matches master deck)")
    
    return output_file

if __name__ == "__main__":
    create_ingress_deck()
