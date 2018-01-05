# Example:
# python3.4 health_check.py -ip 172.29.219.19 -ep /cscl_etl/health
#
import time
import requests
import argparse
import logging
import logging.config

parser = argparse.ArgumentParser(description='Health Check')

parser.add_argument('--ipaddress', '-ip', help='IP Address of HA Proxy node', type=str, required='true')
parser.add_argument('--endpoint', '-ep', help='Health Check endpoint', type=str, required='true')
args = parser.parse_args()

logger = logging.getLogger('healthCheck')
logging.config.fileConfig('logging.conf')


def checkHealth(ip,ep):
    SUCCESS = 0
    FAILURE = 0

    while True:
        url = 'http://'+ip+ep
        try:
            result = requests.get(url, timeout=0.5).content.decode('utf-8')
            if result == "{\"status\":\"UP\"}":
                SUCCESS += 1
                logger.info("Endpoint reported : "+result+" Total SUCCESS count is = "+str(SUCCESS))
                time.sleep(0.5)
            else:
                logger.error("No Response Recieved from http://"+ip+ep+" Total FAILURE count is = "+str(FAILURE))
                FAILURE += 1
                time.sleep(0.5)
        except(requests.exceptions.ReadTimeout):
            FAILURE += 1
            logger.error("No Response Recieved from http://"+ip+ep+" Total FAILURE count is = "+str(FAILURE))

if __name__ == "__main__":
    checkHealth(args.ipaddress,args.endpoint)
