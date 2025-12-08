// infra/main.bicep
targetScope = 'resourceGroup'

@description('Name of the application')
param appName string

@description('Location for all resources')
param location string = resourceGroup().location

module app 'modules/app.bicep' = {
  name: 'app'
  params: {
    appName: appName
    location: location
  }
}

module kv 'modules/kv.bicep' = {
  name: 'kv'
  params: {
    appName: appName
    location: location
    principalId: app.outputs.principalId
  }
}

module monitoring 'modules/monitor.bicep' = {
  name: 'monitor'
  params: {
    appName: appName
    location: location
  }
}

// Expose what azd + your app need
output APP_SERVICE_NAME string = app.outputs.appServiceName
output APP_URL string          = app.outputs.appUrl
output KEY_VAULT_NAME string   = kv.outputs.keyVaultName
