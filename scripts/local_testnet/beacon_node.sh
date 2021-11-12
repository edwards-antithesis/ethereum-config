
#!/usr/bin/env bash

#
# Starts a beacon node based upon a genesis state created by
# `./setup.sh`.
#
# Usage: ./beacon_node.sh <DATADIR> <NETWORK-PORT> <HTTP-PORT> <ENR-ADDRESS>

source /lighthouse/scripts/local_testnet/vars.env

exec /usr/local/bin/lighthouse \
	--debug-level debug \
	bn \
	--datadir $1 \
	--testnet-dir $TESTNET_DIR \
	--staking \
	--enr-address $4 \
	--enr-udp-port $2 \
	--enr-tcp-port $2 \
	--port $2 \
	--http-port $3 \
	--eth1-endpoints http://10.0.20.2:8545 \
	--http-address 0.0.0.0
	--http-allow-origin "*"