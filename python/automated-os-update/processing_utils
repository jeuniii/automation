import subprocess
import file_utils
import shell_utils
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('osPatch')

def checkServices(ip, id, hostname):
    services = ['redis-server', 'kube-apiserver', 'haproxy', 'kubelet', 'efm', 'mongod', 'elasticsearch', 'tyk-gateway', 'vault']
    for svc in services:
        commandOutput = shell_utils.runCommandOnRemoteHost(ip, "pgrep -fa %s" % svc)
        if not commandOutput:
            logger.debug(svc + "process was not found on " + hostname + "/" + ip)
        else:
            if svc == 'vault':
                logger.debug("Checking Vault type on " + hostname + "/" + ip)
                svc = checkVaultType(ip)
                file_utils.writeToServiceFile("services.txt",svc,ip,id,'None', hostname)
            else:
                logger.info(svc + " found on " + hostname + "/" + ip)
                systemStatus = serviceDetails(ip,svc)
                file_utils.writeToServiceFile("services.txt",svc,ip,id,systemStatus, hostname)

def serviceDetails(ip,svc):
    if svc == 'redis-server':
       password = file_utils.getConfigInfo("config.secret", "REDIS_PASS")
       commandOutput = shell_utils.runCommandOnRemoteHost(ip, "redis-cli -a '%s' info replication | grep role | cut -d':' -f2" % password)
       try:
           result = commandOutput[0].decode('utf-8').strip()
       except(IndexError):
           pass
       try:
           return  result
       except(UnboundLocalError):
           pass

    elif svc == 'efm':
        commandOutput = shell_utils.runCommandOnRemoteHost(ip, "/usr/efm-2.0/bin/efm cluster-status efm | grep %s| head -1 | awk '{print $1}'" % ip)
        try:
            result = commandOutput[0].decode('utf-8').strip()
        except(IndexError):
            pass
        return  result

    elif svc == 'mongod':
        password = file_utils.getConfigInfo("config.secret", "MONGO_PASS")
        commandOutput = shell_utils.runCommandOnRemoteHost(ip, "mongo admin -u %s -p root --eval 'printjson(rs.status())' | grep -A 5 %s | grep stateStr | awk '{print $3}'| cut -d'\"' -f2" % (password, ip))
        try:
            result = commandOutput[0].decode('utf-8').strip()
        except(IndexError):
            pass
        try:
            return  result
        except(UnboundLocalError):
            logger.error("MongoDB passwors is incorrect. Please change password in config.secret file")

    elif svc == 'tyk-gateway':
        vip = file_utils.getConfigInfo("config.secret", "TYK_VIP")
        commandOutput = shell_utils.runCommandOnHost("curl --silent http://%s:8181 | grep %s | grep tyk_gateway |  grep '<td class=ac>Y</td><td class=ac>-</td>' | wc -l" % (vip, ip))
        result = commandOutput.decode('utf-8').strip()
        if result == "1":
            return "Active"
        else:
            return "Backup"

    elif svc == 'elasticsearch':
        commandOutput = shell_utils.runCommandOnRemoteHost(ip, "curl http://%s:9200/_cat/master | awk '{print $2}'" % ip)
        try:
            elasticSearchIp = commandOutput[0].decode('utf-8').strip()
        except(IndexError):
            pass
        try:
            if elasticSearchIp == ip:
               return "Master"
            else:
               return "Secondary"
        except(UnboundLocalError):
            pass
    else:
       print ("No sub service found")

def checkVaultType(ip):
    commandOutput = shell_utils.runCommandOnRemoteHost(ip, "pgrep -af vault | awk '{print $2}'")
    vaultPath = commandOutput[0].decode('utf-8').strip()
    if vaultPath == "/opt/vault":
        return "vault-dcg"
    else:
        return "vault-ha"
