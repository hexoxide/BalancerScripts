#!/usr/bin/env bash

function runForever {
    local LOGFILE=runs.log
    date >> $LOGFILE
    local run=0
    
    while /bin/true;
    do  
        #setting status to run   
        echo $run
        echo $run >> $LOGFILE
        run=$((run+=1)) 
        #starting up
        ansible-playbook ./ansible/start_balancing.yaml
        sleep 4m 
        #killing everything
        ansible-playbook ./ansible/stop_balancing.yaml
        sleep 20s
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
    exit 1
fi

    echo start balancing
    export -f runForever
    nohup bash -c runForever& 
