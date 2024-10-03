use jenkins-deployment-config.yml in config folder to customise the run

#config file documentation

environment: which env the URLs would be pointed to
globalActionEnabled: use this to run all the services with a single action mentioned in "globalAction"
globalAction: use this to provide the action which would be used globally for all services
baseurl: base url of jenkins site
J_USERNAME: username of jenkins
J_PASS: pass for jenkins
successMsg: msg which would be searched for in jenkins console
maxTimeForTab: max time to wait in 1 tab in 1 loop
maxTimeForWholeRun: max time for script to get executed
sleepBeforeEachCycleStart: wait time before each new tab opens



deployment:
  pricing-order: service name used in jenkins
    url:  URL of jenkins pipeline
    deploy: if the service needs to be deployed, this flag should be true, irrespective of globalActionEnabled
    action: if globalActionEnabled is false, this action would have priority
    version: version to be used in deployment