#!/usr/bin/env bash

#
# Starts a validator client based upon a genesis state created by
# `./setup.sh`.
#
# Usage: ./validator_client.sh <DATADIR> <BEACON-NODE-HTTP> <OPTIONAL-DEBUG-LEVEL>

source /lighthouse/scripts/local_testnet/vars.env

exec /usr/local/bin/lighthouse \
	--debug-level $DEBUG_LEVEL \
	vc \
	--datadir $1 \
	--testnet-dir $TESTNET_DIR \
	--init-slashing-protection \
	--beacon-nodes $2
