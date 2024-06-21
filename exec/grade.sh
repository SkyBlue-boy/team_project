#!/bin/bash

LOGFILE="/mnt/c/Users/sasa0/Downloads/team_project-main/team_project-main/exec/grade.log"

echo "Grading submission at $(date)" >> $LOGFILE

for file in /mnt/c/Users/sasa0/Downloads/team_project-main/team_project-main/exec/submissions/*.py; do
    id=$(basename "$file" .py)
    echo "Processing file: $file with id: $id" >> $LOGFILE

    code_file="$file"
    output_file="/mnt/c/Users/sasa0/Downloads/team_project-main/team_project-main/exec/results/${id}.stdout"
    error_file="/mnt/c/Users/sasa0/Downloads/team_project-main/team_project-main/exec/results/${id}.stderr"
    answer_file="/mnt/c/Users/sasa0/Downloads/team_project-main/team_project-main/exec/answer.txt"

    python3 "$code_file" > "$output_file" 2> "$error_file"
    echo "Execution output:" >> $LOGFILE
    cat "$output_file" >> $LOGFILE
    echo "Execution error:" >> $LOGFILE
    cat "$error_file" >> $LOGFILE

    if [ -s "$error_file" ]; then
        status="ERROR"
    elif diff -q "$output_file" "$answer_file"; then
        status="CORRECT"
    else
        status="INCORRECT"
    fi

    # Here, make sure id and status are properly formatted in JSON
    JSON_PAYLOAD=$(jq -n --arg id "$id" --arg status "$status" '{id: $id, status: $status}')
    echo "Sending JSON: $JSON_PAYLOAD" >> $LOGFILE

    response=$(curl -s -o /dev/null -w "%{http_code}" -X PATCH http://172.17.67.79:8000/submission \
        -H "Content-Type: application/json" \
        -d "$JSON_PAYLOAD")

    echo "Server response: $response" >> $LOGFILE
    echo "Graded submission ID $id with status $status at $(date)" >> $LOGFILE
done

