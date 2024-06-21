#!/bin/bash

LOGFILE="/mnt/c/Users/sasa0/Downloads/team_project-main/team_project-main/exec/fetch.log"

echo "Fetching new submission at $(date)" >> $LOGFILE
response=$(curl -s -X GET http://172.17.67.79:8000/new)

echo "Response: $response" >> $LOGFILE

# Check if the response contains the "detail" field
if echo "$response" | jq -e '.detail' > /dev/null; then
    echo "No new submissions at $(date)" >> $LOGFILE
else
    id=$(echo "$response" | jq -r '.id')
    code=$(echo "$response" | jq -r '.code')

    echo "Parsed ID: $id" >> $LOGFILE
    echo "Parsed Code: $code" >> $LOGFILE

    if [ ! -z "$id" ] && [ ! -z "$code" ]; then
        echo "$code" > /mnt/c/Users/sasa0/Downloads/team_project-main/team_project-main/exec/submissions/$id.py
        echo "Fetched submission ID $id at $(date)" >> $LOGFILE
    else
        echo "Invalid submission data received at $(date)" >> $LOGFILE
    fi
fi

