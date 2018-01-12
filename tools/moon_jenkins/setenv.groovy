#!groovy

import jenkins.*
import jenkins.model.*
import hudson.*
import hudson.model.*

instance = Jenkins.getInstance()
globalNodeProperties = instance.getGlobalNodeProperties()

envVarsNodePropertyList = globalNodeProperties.getAll(hudson.slaves.EnvironmentVariablesNodeProperty.class)

newEnvVarsNodeProperty = null
envVars = null

if (envVarsNodePropertyList == null || envVarsNodePropertyList.size() == 0) {
    newEnvVarsNodeProperty = new hudson.slaves.EnvironmentVariablesNodeProperty();
    globalNodeProperties.add(newEnvVarsNodeProperty)
    envVars = newEnvVarsNodeProperty.getEnvVars()
} else {
    envVars = envVarsNodePropertyList.get(0).getEnvVars()
}

http_proxy = System.getenv()['http_proxy']
https_proxy = System.getenv()['https_proxy']

if (http_proxy) {
  envVars.put("http_proxy", System.getenv()['http_proxy'])
}
if (https_proxy) {
  envVars.put("https_proxy", System.getenv()['https_proxy'])
}

instance.save()
