#!/usr/bin/env bash


function runForever {
    local LOGFILE=$(date +"%Y-%m-%d.log")
    echo "Starting to run on $(date)" >> $LOGFILE
    local increment=5
    while /usr/bin/true; do
        for ((j = 0; j < 25; j+=1)); do   
            #setting status to run   
             
            echo "[$(date +'%T')] run : $j with ticktime : $increment" >> $LOGFILE  
            #starting up
            ansible-playbook ./ansible/start_balancing.yaml --extra-vars "zookeeperTick=$increment "
            sleep 7m 
            #killing everything
            ansible-playbook ./ansible/stop_balancing.yaml
            sleep 20s
            

        done
        ansible-playbook ./ansible/get_logs.yaml --extra-vars "flpResult=../res/flp/$increment infoResult=../res/info/$increment epnResult=../res/epn/$increment"
        ansible-playbook ./ansible/purgelogs.yaml
        tar -cvzf ./results/$increment.tar.gz ./res/epn ./res/flp ./res/info/
        rm -rf ./res/
        increment=$((increment+=5))
        echo "Testing tickrate now on $increment"
    done
}

status=`ps -efww | grep -w "runForever" | grep -v grep | grep -v $$ | awk '{ print $2 }'`

if [ ! -z "$status" ]; then
    echo stop balancing
    stat=$(ps aux | grep runForever) 
    pids=$(pgrep bash)
    for i in $pids; do    
        if [[ $stat == *"$i"* ]]; then
            kill -9 $i
        fi
    done
    ansible-playbook ./ansible/stop_balancing.yaml
    exit 1
fi
echo Starting balancing
if [[ $1 == "Debug" ]]; then 
    runForever
else
    export -f runForever
    nohup bash -c runForever & 
fi
#runForever
