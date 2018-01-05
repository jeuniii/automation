import re
import ast
import json
import time
import requests
import argparse
import jenkinsapi

parser = argparse.ArgumentParser(description='Automatic Jenkins Job Trigger')
parser.add_argument('--username', '-u', help='Jenkins username', type=str, required='true')
parser.add_argument('--token', '-t', help='Jenkins token', type=str, required='true')
parser.add_argument('--url', help='Url of Jenkins node', default="1.1.1.1:8080")
args = parser.parse_args()

def initializeVariables(user, tok, jenkins_url):
    global username, token, url
    username = user
    token    = tok
    url      = jenkins_url

def triggerJenkinsJob(microservice):
    jobs = json.loads(requests.get('http://%s/api/json' %url).text)['jobs']
    for job in jobs:
        if re.match(r'^%s-(ib|master)(.*)-10-(.*)' %microservice, job["name"] ):
            triggerJob(job["name"],getPipelineJobs(microservice))

def getPipelineJobs(microservice):
    children = []
    jobs = json.loads(requests.get('http://%s/api/json' %url).text)['jobs']
    for job in jobs:
        if re.match('^%s-master-[1-3][0-9]-' %microservice, job["name"]) is not None:
            children.append(job["name"])
    return children

def waitForJob(pipelineJobs):
    time.sleep(60)
    jenkinsapi.api.block_until_complete('http://%s' % url,pipelineJobs)

def triggerJob(microservice,childJobs):
    requests.post("http://%s:%s@%s/job/%s/build" % (username , token, url, microservice))
    waitForJob(childJobs)

def invokeTrigger():
    ## TODO :: Need to find mechanism to add new services in proper order.
    microservices = # Add list of job names here.
    for microservice in microservices:
        triggerJenkinsJob(microservice)

if __name__ == "__main__":
    initializeVariables(args.username, args.token, args.url)
    invokeTrigger()
