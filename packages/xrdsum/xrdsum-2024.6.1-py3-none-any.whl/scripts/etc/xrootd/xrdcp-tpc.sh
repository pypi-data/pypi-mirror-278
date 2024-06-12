#!/bin/bash

# from https://github.com/snafus/cephsum/blob/master/scripts/xrdcp-tpc.sh
#Original code
#/usr/bin/xrdcp --server -f $1 root://$XRDXROOTD_PROXY/$2

# Collect all arguments except for the last two
OTHERARGS=("${@:1:$#-2}")

# Get the second-to-last argument
DSTFILE="${*: -2:1}"

# Get the last argument
SRCFILE="${*: -1}"

# Use the arguments in the xrdcp command
# Note: We use "${OTHERARGS[@]}" to correctly handle spaces in arguments
/usr/bin/xrdcp "${OTHERARGS[@]}" --server -f "$SRCFILE" "root://$XRDXROOTD_PROXY/$DSTFILE"
