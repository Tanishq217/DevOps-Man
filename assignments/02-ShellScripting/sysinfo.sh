#!/bin/bash

# 1. print current date
CURRENT_DATE=$(date)
echo "Date: $CURRENT_DATE"

# 2. print hostname
HOST_NAME=$(hostname)
echo "Hostname: $HOST_NAME"

# 3. print username
USER_NAME=$(whoami)
echo "User: $USER_NAME"

# 4. print disk usage
echo "Disk Usage:"
df -h

# 5. print running processes
echo "Running Processes:"
ps -ax | head -20

# 6. take user input
read -p "Enter directory name: " PROJECT_NAME

# 7. create directory
mkdir -p $PROJECT_NAME
echo "Directory created: $PROJECT_NAME"

# 8. create a file inside it
touch $PROJECT_NAME/system_report.txt
echo "File created: $PROJECT_NAME/system_report.txt"

# 9. store process info into the file using output redirection
ps -ax > $PROJECT_NAME/system_report.txt
echo "Process info saved to system_report.txt"
