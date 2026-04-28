#!/usr/bin/env bash

#
# Extract data from RDB and output it as Wolfram Language
#

RDB="$(ls -tr ./databases/jumpack*db | tail -1)"

echo "Running with RDB $RDB"

TABLE="readings"

echo "RDB schema:"
sqlite3 "$RDB" ".schema $TABLE"

# Get sample data
echo -e "\nSample data, descending order:"
sqlite3 -separator , "$RDB" "SELECT * FROM readings ORDER BY id DESC LIMIT 3;"

# Get stats
echo -e "\nSummary:"
sqlite3 "$RDB" "SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM readings;"



