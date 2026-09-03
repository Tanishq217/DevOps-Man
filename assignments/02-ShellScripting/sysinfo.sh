#!/bin/bash

# ============================================================
# Script Name: sysinfo.sh
# Description: System Information Script - DevOps Assignment 02
# Author: Tanishq
# Date: $(date +%Y-%m-%d)
# ============================================================

echo "=============================================="
echo "       SYSTEM INFORMATION REPORT"
echo "=============================================="
echo ""

# ── 1. Print the Current Date ───────────────────
CURRENT_DATE=$(date)
echo "📅 Current Date & Time:"
echo "   $CURRENT_DATE"
echo ""

# ── 2. Print the Hostname ───────────────────────
HOST_NAME=$(hostname)
echo "🖥️  Hostname:"
echo "   $HOST_NAME"
echo ""

# ── 3. Print the Username ───────────────────────
USER_NAME=$(whoami)
echo "👤 Logged-in User:"
echo "   $USER_NAME"
echo ""

# ── 4. Print Disk Usage ─────────────────────────
echo "💾 Disk Usage:"
df -h
echo ""

# ── 5. Print Running Processes ──────────────────
echo "⚙️  Running Processes (snapshot):"
ps -ax | head -20
echo ""

# ── 6. Take User Input ──────────────────────────
read -p "📁 Enter a name for the project directory to create: " PROJECT_NAME
echo ""

# ── 7. Create a Directory ───────────────────────
DIR_PATH="./$PROJECT_NAME"
mkdir -p "$DIR_PATH"
echo "✅ Directory created: $DIR_PATH"
echo ""

# ── 8. Create a File ────────────────────────────
REPORT_FILE="$DIR_PATH/system_report.txt"
touch "$REPORT_FILE"
echo "✅ File created: $REPORT_FILE"
echo ""

# ── 9. Store Running Processes in the File ──────
echo "📝 Saving running processes to $REPORT_FILE ..."
{
  echo "=============================================="
  echo "  SYSTEM REPORT — Generated on: $CURRENT_DATE"
  echo "  Hostname : $HOST_NAME"
  echo "  User     : $USER_NAME"
  echo "=============================================="
  echo ""
  echo "--- DISK USAGE ---"
  df -h
  echo ""
  echo "--- RUNNING PROCESSES ---"
  ps -ax
} > "$REPORT_FILE"

echo "✅ Process info saved to: $REPORT_FILE"
echo ""
echo "=============================================="
echo "        REPORT COMPLETE — All Done! 🎉"
echo "=============================================="
