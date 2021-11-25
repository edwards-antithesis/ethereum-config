#!/bin/bash
set -x

#./netprobe 10.0.20.2 8545
sleep 125
# attempt=0
# success=0
# while [ attempt -lt 5]; do 
#     msg=$(nc -zv 10.0.20.2 8545)
#     if [[ "$msg" == "*succeeded*" ]]; then
#     success=1
#     break
#     else
#     ((attempt++))
#     sleep 10
#     fi
# done
# if [[ success -eq 0 ]]; then
# echo "Couldn't establish Connection"
# exit 11
# fi
echo "Starting setup.sh"
/lighthouse/scripts/local_testnet/setup.sh
echo "Sleeping 100"
sleep 100
echo "Starting bootnode.sh"
/lighthouse/scripts/local_testnet/bootnode.sh
echo "Finished bootnode.sh"
sleep 10