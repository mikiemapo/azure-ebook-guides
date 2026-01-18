window.AZ104_OBJECTIVES = {
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
};
