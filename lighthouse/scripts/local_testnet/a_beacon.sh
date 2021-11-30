#!/bin/bash
set -x

sleep $1
/lighthouse/scripts/local_testnet/beacon_node.sh $2 $3 $4 $5 &
sleep 51
/lighthouse/scripts/local_testnet/validator_client.sh $2 $6