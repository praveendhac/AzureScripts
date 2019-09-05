# Audit all NSG Rules in Azure Subscription
Read all NSGs and assocated rules in the NSG, look for rules open to Internet and update them to be accessible from Corporate environment (sourceAddressPrefixes)

## Understand config file(audit_rules.json)
`skip_aks` Don't audit NSG rules for AKS Clusters
`exclude_nsgs` Don't audit NSG names given in the array/list
`exclude_rgs` Don't audit resource groups (RG) names given in the array/list
`sourceAddressPrefixes` Corporate Public IP's to Whitelist
