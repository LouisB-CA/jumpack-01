#!/usr/bin/env bash

# ----------------------------------
declare -x RESET_COLOR="\033[00m"
declare -x NOCOLOR="\033[0m"
# ----------------------------------
# Regular Colors
declare -x BLACK="\033[0;30m"
declare -x RED="\033[0;31m"
declare -x GREEN="\033[0;32m"
declare -x ORANGE="\033[0;33m"
declare -x BLUE="\033[0;34m"
declare -x PURPLE="\033[0;35m"
declare -x CYAN="\033[0;36m"
declare -x LIGHTGRAY="\033[0;37m"
# ----------------------------------
# Bold Colors
declare -x DARKGRAY="\033[1;30m"
declare -x BOLDRED="\033[1;31m"
declare -x BOLDGREEN="\033[1;32m"
declare -x YELLOW="\033[1;33m"
declare -x BOLDBLUE="\033[1;34m"
declare -x BOLDPURPLE="\033[1;35m"
declare -x BOLDCYAN="\033[1;36m"
declare -x WHITE="\033[1;37m"
# ----------------------------------

# Check marks and cross marks
# these may require printf to work correctly
declare -x HEAVY_CHECK_MARK="${GREEN}\U2714${RESET_COLOR}"
declare -x HEAVY_BALLOT_X="${RED}\U2718${RESET_COLOR}"
declare -x CROSS_MARK="\U274C"
declare -x CHECK_GREEN_BKGD="\U00002705"
# ----------------------------------

if [[ $# == 1 ]] ; then
	if [[ -f "$1" ]] ; then
		RDB="$1"
	else
		CROSS="[${HEAVY_BALLOT_X}]"
		printf "$CROSS File not found: ${1}\n"
		exit 1
	fi
fi

RDB="$(ls -tr ./Databases/jumpack*db | tail -1)"

echo "Running with RDB $RDB"

# Get schema
echo "RDB schema:"
sqlite3 "$RDB" ".schema"

# Get sample data
echo -e "\nSample data, ascending order:"
sqlite3 "$RDB" "SELECT * FROM readings ORDER BY id LIMIT 3;"
echo -e "\nSample data, descending order:"
sqlite3 "$RDB" "SELECT * FROM readings ORDER BY id DESC LIMIT 3;"

# Get stats
echo -e "\nSummary:"
sqlite3 "$RDB" "SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM readings;"



