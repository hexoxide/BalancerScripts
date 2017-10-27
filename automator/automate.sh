#!/usr/bin/env bash

echo "Starting to run program 2000 times" >> runs.txt

for i in {1..2000}
do  
    #setting status to run  
    echo $i >> runs.txt
    #starting up
    ansible-playbook ../ansibleExp/start_balancing.yaml
    sleep 4m 
    #killing everything
    ansible-playbook ../ansibleExp/stop_balancing.yaml
    sleep 20s
done 

    
