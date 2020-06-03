#!groovy

import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

def user = System.getenv()['jenkins_user']
def pass = System.getenv()['jenkins_password']
// Create user account
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount(user,pass)
instance.setSecurityRealm(hudsonRealm)

// Enable matrix auth strategy and set my_user as admin
def strategy = new GlobalMatrixAuthorizationStrategy()
strategy.add(Jenkins.ADMINISTER, user)
instance.setAuthorizationStrategy(strategy)

instance.save()
