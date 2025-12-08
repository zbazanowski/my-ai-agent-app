@description('Base name for monitoring resources')
param appName string

@description('Region for monitoring resources')
param location string = resourceGroup().location

@description('Retention for Log Analytics workspace (30–730 days)')
@allowed([30, 60, 90, 120, 180, 365, 550, 730])
param logRetentionDays int = 30

// -----------------------------------------
// 1. Log Analytics Workspace
// -----------------------------------------
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${appName}-law'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: logRetentionDays
    features: {
      legacy: 0
    }
  }
}

// -----------------------------------------
// 2. Application Insights
// -----------------------------------------
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${appName}-ai'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    DisableIpMasking: true
  }
}

// -----------------------------------------
// Outputs
// -----------------------------------------
output logAnalyticsName string = logAnalytics.name
output logAnalyticsId string = logAnalytics.id

output applicationInsightsName string = appInsights.name
output applicationInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output applicationInsightsConnectionString string = appInsights.properties.ConnectionString

