#!/bin/bash
#
# ./health_check.sh  -ip "IP Adress of LB"  -e "Health End Point" > out.log 2> /dev/null | tail -f out.log
#

while [[ $# > 0 ]]
do
    key="$1"
    case $key in
        -ip|--ipaddress)
            IP="$2"
            shift
            ;;
        -e|--endpoint)
            ENDPOINT="$2"
            shift
            ;;
        *)
            echo "Unknown argument $1, exiting"
            exit 1
            ;;
    esac
    shift
done

OK_COUNT=0
NOK_COUNT=0

while :
  do
    RESULT=`curl -s http://${IP}${ENDPOINT} --max-time 1`

      if [ $RESULT == '{"status":"UP"}' ]
        then
           (( OK_COUNT+=1 ))
           echo "`date` :: ${ENDPOINT} is OK ! Total count is $OK_COUNT "
        else
           (( NOK_COUNT+=1 ))
           echo "`date` :: ${ENDPOINT} is UNREACHABLE ! Total count is $NOK_COUNT"
      fi

    sleep 0.5
  done
