provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

# --- Azure Landing Zone Foundation (Hub-Spoke) ---

resource "azurerm_virtual_network" "hub" {
  name                = "vnet-hub-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "firewall" {
  name                 = "AzureFirewallSubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.1.0/24"]
}

# --- Shared Governance Identity (Entra ID integration) ---

resource "azurerm_user_assigned_identity" "onboarding_agent" {
  name                = "id-onboarding-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# --- AWS Landing Zone Foundation (Control Tower Style) ---

resource "aws_organizations_organization" "org" {
  feature_set = "ALL"
}

resource "aws_organizations_organizational_unit" "data_domains" {
  name      = "DataDomains"
  parent_id = aws_organizations_organization.org.roots[0].id
}

# --- Global Observability Hub (Log Analytics) ---

resource "azurerm_log_analytics_workspace" "audit" {
  name                = "log-audit-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 365 # 1 year retention for compliance
}
