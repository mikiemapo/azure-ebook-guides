terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.75.0"
    }
  }

  required_version = ">= 1.1.0"
}

variable "subscription_id" {
  type = string
  description = "Azure Subscription ID"
}

variable "resource_group_name" {
  type = string
  description = "Resource group to deploy the resources into"
}

variable "location" {
  type    = string
  default = "East US"
}

provider "azurerm" {
  features {}
  subscription_id                  = var.subscription_id
  use_cli                          = true
  resource_provider_registrations = "none"
}

resource "azurerm_virtual_network" "vnet1" {
  name                = "vnet-eastus"
  location            = var.location
  resource_group_name = var.resource_group_name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet1" {
  name                 = "subnet-eastus"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet1.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_virtual_network" "vnet2" {
  name                = "vnet-westeurope"
  location            = "West Europe"
  resource_group_name = var.resource_group_name
  address_space       = ["10.1.0.0/16"]
}

resource "azurerm_subnet" "subnet2" {
  name                 = "subnet-westeurope"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet2.name
  address_prefixes     = ["10.1.1.0/24"]
}

resource "azurerm_virtual_network_peering" "peering1" {
  name                         = "vnet1-to-vnet2"
  resource_group_name          = var.resource_group_name
  virtual_network_name         = azurerm_virtual_network.vnet1.name
  remote_virtual_network_id    = azurerm_virtual_network.vnet2.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false
  use_remote_gateways          = false
}

resource "azurerm_virtual_network_peering" "peering2" {
  name                         = "vnet2-to-vnet1"
  resource_group_name          = var.resource_group_name
  virtual_network_name         = azurerm_virtual_network.vnet2.name
  remote_virtual_network_id    = azurerm_virtual_network.vnet1.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false
  use_remote_gateways          = false
}